import pytest
import os
import sys
from PIL import Image

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.NMIS_Ecopass.utils.utils import QRCodeGenerator

@pytest.fixture
def qr_generator():
    return QRCodeGenerator(module_size_mm=0.35)

@pytest.fixture
def test_output_path(tmp_path):
    return str(tmp_path / "test_qr.png")

def test_init_with_valid_module_size():
    """Test initialization with valid module size"""
    generator = QRCodeGenerator(module_size_mm=0.5)
    assert generator.module_size_mm == 0.5

def test_init_with_small_module_size():
    """Test initialization enforces minimum module size"""
    generator = QRCodeGenerator(module_size_mm=0.2)
    assert generator.module_size_mm == 0.25  # Should be adjusted to minimum

def test_validate_il_string_valid(qr_generator):
    """Test validation of valid IL strings"""
    valid_strings = [
        "https://example.com/product/123",
        "http://test.org/path?param=value",
        "https://api.example.com/v1/products/123#section",
        "https://example.com/path-with-special-chars/~._-:/?#[]@!$&'()*+,;="
    ]
    
    for il_string in valid_strings:
        assert qr_generator.validate_il_string(il_string) is True

def test_validate_il_string_invalid(qr_generator):
    """Test validation of invalid IL strings"""
    invalid_strings = [
        "",  # Empty string
        "a" * 256,  # Too long
        "https://UPPERCASE.com",  # Uppercase in host
        "https://example.com/<invalid>",  # Invalid characters
        "https://example.com/path with spaces",  # Spaces
    ]
    
    for il_string in invalid_strings:
        with pytest.raises(ValueError):
            qr_generator.validate_il_string(il_string)

def test_create_qr_code_basic(qr_generator, test_output_path):
    """Test basic QR code creation"""
    il_string = "https://example.com/product/123"
    image = qr_generator.create_qr_code(il_string, test_output_path)
    
    # Verify image was created
    assert os.path.exists(test_output_path)
    
    # Verify it's a valid image
    assert isinstance(image, Image.Image)
    assert image.mode == "RGB"
    
    # Load and verify the saved image
    saved_image = Image.open(test_output_path)
    assert saved_image.mode == "RGB"

def test_create_qr_code_dimensions(qr_generator, test_output_path):
    """Test QR code dimensions and frame"""
    il_string = "https://example.com/product/123"
    image = qr_generator.create_qr_code(il_string, test_output_path)
    
    # Image should be square
    width, height = image.size
    assert width == height
    
    # Size should be sufficient for QR code plus frame
    assert width > 100  # Minimum size for readable QR code with frame

def test_create_qr_code_invalid_string(qr_generator, test_output_path):
    """Test QR code creation with invalid IL string"""
    invalid_il_string = "https://UPPERCASE.com"
    
    with pytest.raises(ValueError):
        qr_generator.create_qr_code(invalid_il_string, test_output_path)

def test_create_qr_code_invalid_path(qr_generator):
    """Test QR code creation with invalid output path"""
    il_string = "https://example.com/product/123"
    invalid_path = "/nonexistent/directory/qr.png"
    
    with pytest.raises(Exception):
        qr_generator.create_qr_code(il_string, invalid_path)

def test_qr_code_frame_elements(qr_generator, test_output_path):
    """Test QR code frame elements are present"""
    il_string = "https://example.com/product/123"
    image = qr_generator.create_qr_code(il_string, test_output_path)
    
    # Get image data
    pixels = image.load()
    width, height = image.size
    
    # Check frame corners (should be black)
    assert pixels[0, 0] == (0, 0, 0)  # Top-left
    assert pixels[width-1, 0] == (0, 0, 0)  # Top-right
    assert pixels[0, height-1] == (0, 0, 0)  # Bottom-left
    
    # Check triangle in bottom-right corner
    bottom_right_area = [
        pixels[width-1, height-1],
        pixels[width-2, height-1],
        pixels[width-1, height-2]
    ]
    assert all(pixel == (0, 0, 0) for pixel in bottom_right_area)  # Should be black

def test_create_qr_code_with_long_content(qr_generator, test_output_path):
    """Test QR code creation with long content"""
    long_il_string = "https://example.com/" + "a" * 100  # Long but valid URL
    image = qr_generator.create_qr_code(long_il_string, test_output_path)
    
    # Verify the image was created successfully
    assert isinstance(image, Image.Image)
    assert os.path.exists(test_output_path)

def test_create_multiple_qr_codes(qr_generator, tmp_path):
    """Test creating multiple QR codes"""
    il_strings = [
        "https://example.com/product/1",
        "https://example.com/product/2",
        "https://example.com/product/3"
    ]
    
    for i, il_string in enumerate(il_strings):
        output_path = str(tmp_path / f"qr_{i}.png")
        image = qr_generator.create_qr_code(il_string, output_path)
        assert os.path.exists(output_path)
        assert isinstance(image, Image.Image) 