import qrcode
from qrcode.constants import ERROR_CORRECT_Q
from PIL import Image, ImageDraw
import re

class QRCodeGenerator:
    def __init__(self, module_size_mm=0.35):
        """
        Initialize QR generator with IEC 61406 specifications
        Default module size is 0.35mm (recommended minimum)
        """
        self.module_size_mm = max(0.25, module_size_mm)  # Ensure minimum 0.25mm
        
    def validate_il_string(self, il_string):
        """
        Validate IL string according to IEC 61406 requirements
        """
        if not il_string or len(il_string) > 255:
            raise ValueError("IL string must not exceed 255 characters")
            
        # Check for valid URL characters per RFC 3986
        allowed_chars = re.compile(r'^[a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=]+$')
        if not allowed_chars.match(il_string):
            raise ValueError("IL string contains invalid characters")
            
        # Validate no uppercase in scheme and host parts
        if "://" in il_string:
            scheme_host = il_string.split("/")[0:3]
            if any(c.isupper() for c in "/".join(scheme_host)):
                raise ValueError("Uppercase not allowed in scheme and host components")
                
        return True
        
    def create_qr_code(self, il_string, output_path):
        """
        Create an IEC 61406 compliant QR code with frame
        """
        # Validate IL string
        self.validate_il_string(il_string)
        
        # Create QR code with Error Correction Level Q (recommended by IEC 61406)
        qr = qrcode.QRCode(
            version=None,
            error_correction=ERROR_CORRECT_Q,
            box_size=10,  # Will be scaled to meet module size requirement
            border=4      # Quiet zone of 4 modules as required
        )
        
        qr.add_data(il_string)
        qr.make(fit=True)
        
        # Create QR code image (positive image as required)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to RGB mode
        qr_image = qr_image.convert('RGB')
        
        # Calculate frame dimensions
        qr_size = qr_image.size[0]
        frame_distance = 40  # 4 modules * 10 pixels per module
        frame_thickness = 10  # 1 module * 10 pixels per module
        triangle_size = 60    # 6 modules * 10 pixels per module
        
        # Create new image with space for frame
        total_size = qr_size + 2 * (frame_distance + frame_thickness)
        final_image = Image.new('RGB', (total_size, total_size), 'white')
        
        # Paste QR code in center
        qr_position = frame_distance + frame_thickness
        final_image.paste(qr_image, (qr_position, qr_position))
        
        # Draw frame
        draw = ImageDraw.Draw(final_image)
        
        # Outer frame
        draw.rectangle(
            [(frame_thickness, frame_thickness),
             (total_size - frame_thickness, total_size - frame_thickness)],
            outline='black',
            width=frame_thickness
        )
        
        # Draw triangle in lower right corner
        bottom_right = (total_size - frame_thickness, total_size - frame_thickness)
        triangle_points = [
            bottom_right,
            (bottom_right[0] - triangle_size, bottom_right[1]),
            (bottom_right[0], bottom_right[1] - triangle_size)
        ]
        draw.polygon(triangle_points, fill='black')
        
        # Save the image
        final_image.save(output_path, 'PNG')
        return final_image

    def get_physical_size_mm(self):
        """
        Calculate physical size of the QR code in millimeters
        """
        # Total modules = QR modules + 2 * (quiet zone + frame distance + frame thickness)
        total_modules = self.qr_size + 2 * (4 + 4 + 1)
        return total_modules * self.module_size_mm