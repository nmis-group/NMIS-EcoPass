from datetime import datetime
import uuid

from NMIS_Ecopass.models.digitalProductPassport import DigitalProductPassport
from NMIS_Ecopass.models.metadata import Metadata, StatusEnum
from NMIS_Ecopass.models.productIdentifier import ProductIdentifier, ProductStatus
from NMIS_Ecopass.models.remanufacture import RepairModel, ComponentCondition, RepairType, RepairHistory, QIFDocument, ProcessCategory, DefectInformation, TestResult, ProcessStep
from NMIS_Ecopass.models.circularity import Circularity, RecycledContent, RecycledMaterialInfo, RecycledMaterial, DismantlingAndRemovalDocumentation, ResourcePath, EndOfLifeInformation, SupplierInformation, MimeType, AddressOfSupplier, DocumentType
from NMIS_Ecopass.models.carbonFootprint import CarbonFootprint, LifecycleStageCarbonFootprint, LifecycleStage
from NMIS_Ecopass.models.materialComposition import ProductMaterial, MaterialStandard, MaterialInformation, MaterialTraceability
from NMIS_Ecopass.models.additionalData import AdditionalData


def test_create_default_passport():
    """Test creating a passport with default values"""
    passport = DigitalProductPassport()
    
    # All main sections should exist with default values
    assert isinstance(passport.metadata, Metadata)
    assert isinstance(passport.productIdentifier, ProductIdentifier)
    assert isinstance(passport.circularity, Circularity)
    assert isinstance(passport.carbonFootprint, CarbonFootprint)
    assert isinstance(passport.reManufacture, RepairModel)
    assert isinstance(passport.productMaterial, ProductMaterial)
    
    # Only additionalData should be None
    assert passport.additionalData is None

def test_create_minimal_passport():
    """Test creating a passport with minimal required fields"""
    passport = DigitalProductPassport(
        # All sections are required but can have minimal internal data
        metadata=Metadata(
            economic_operator_id="ECO-001"  # Only required field in Metadata
        ),
        productIdentifier=ProductIdentifier(
            serialID="SN-001"  # Only required field in ProductIdentifier
        ),
        # Other sections will use their defaults
    )
    
    assert passport.metadata.economic_operator_id == "ECO-001"
    assert passport.productIdentifier.serialID == "SN-001"
    # Verify other sections exist with defaults
    assert isinstance(passport.circularity, Circularity)
    assert isinstance(passport.carbonFootprint, CarbonFootprint)

def test_create_complete_passport():
    """Test creating a fully populated digital product passport"""
    current_time = datetime.now()
    
    passport = DigitalProductPassport(
        metadata=Metadata(
            economic_operator_id="company.com",
            registration_identifier="https://www.eco123.company.com",
            issue_date=current_time,
            status=StatusEnum.ACTIVE,
            version="1.0.0",
            passport_identifier=uuid.uuid4(),
            expiration_date="2030-01-01"
        ),
        productIdentifier=ProductIdentifier(
            batchID="BATCH-001",
            serialID="SN-001",
            productStatus=ProductStatus.ORIGINAL,
            productName="NMIS reference product",
            productDescription="A test product for DPP"
        ),
        circularity=Circularity(
            recycledContent=[RecycledContent(
                preConsumerShare=45.0,
                recycledMaterial=RecycledMaterialInfo(
                    material=RecycledMaterial.ALUMINUM,
                    materialInfoURL="https://example.com/materials/aluminum-info"
                ),
                postConsumerShare=30.5
        )],
            dismantlingAndRemovalInformation=[DismantlingAndRemovalDocumentation(
                documentType=DocumentType.DISMANTLINGMANUAL,
                mimeType=MimeType.PDF,
                documentURL=ResourcePath(
                    resourcePath="https://example.com/documents/dismantling-manual.pdf"
                )
            )],
            endOfLifeInformation=EndOfLifeInformation(
                wastePrevention=ResourcePath(
                    resourcePath="https://example.com/waste-prevention"
                ),
                separateCollection=ResourcePath(
                    ResourcePath= "https://example.com/separate-collection"
                ),
                informationOnCollection=ResourcePath(
                    ResourcePath= "https://example.com/separate-collection"
                ),
            ),
            supplierInformation=SupplierInformation(
                name="Eco Parts Ltd.",
                address=AddressOfSupplier(
                    addressCountry="Germany",
                    postalCode="DE-10719",
                    streetAddress="Kurfürstendamm 21"
                ),
                email="contact@ecopartsltd.com",
                supplierWebaddress=ResourcePath(
                    resourcePath="https://ecopartsltd.com"
                )
            )
        ),
        carbonFootprint=CarbonFootprint(
            carbonFootprintPerLifecycleStage=[LifecycleStageCarbonFootprint(
                lifecycleStage=LifecycleStage.RAWMATERIALEXTRACTION,
                carbonFootprint=20.0
            )],
            carbonFootprintStudy="https://example.com/carbon-footprint-study",
        ),
        reManufacture=RepairModel(
            repairId="REP-001",
            currentCondition=ComponentCondition.SERVICEABLE,
            defects=[DefectInformation(
                defectId="DEF-001",
                description="Tip wear",
                location="blade_tip",
                dimensions={"length": 25.0, "width": 3.0, "depth": 1.5},
                severity=3,
            )],
            repairHistory=[RepairHistory(
                repairId="RH-001",
                repairDate=current_time,
                repairType=RepairType.SURFACE_TREATMENT,
                facility="Main Service Center",
                description="Initial inspection",
                technician="John Doe"
            )],
            qifDocuments=[QIFDocument(
                documentId="QIF-2024-001",
                version=1,
                storage_path="qif/QIF-2024-001/1/measurement.qif",
                uri="https://example.com/documents/remanufacture-manual.pdf",
                hash="sha256_hash",
                timestamp=current_time
            )],
            processSteps=[ProcessStep(
                stepId="STEP-001",
                processCategory=ProcessCategory.INSPECTION,
                processType=RepairType.MATERIAL_ADDITION,
                startTime=current_time,
                endTime=current_time,
                operators=["INSP-TECH-001"],
                documentation=["https://nmis.scot/repairs/TB-2024-001/inspection.pdf"]
            )],
            testResults=[TestResult(
                testId="TEST-001",
                testType="fluorescent_penetrant_inspection",
                testDate=current_time,
                results={"indicationFound": False},
                conformity=True,
                testResults=["https://nmis.scot/repairs/TB-2024-001/test-results.pdf"]
            )],
            approvals={
                "inspector": {
                    "name": "John Smith",
                    "id": "INSP-001",
                    "date": current_time.isoformat()
                }
            },
            nextMaintenanceDue="2025-01-01",
        ),
        productMaterial=ProductMaterial(
            productId="PROD-001",
            components={
                "main_body": MaterialInformation(
                    materialId="MAT-001",
                    tradeName="Eco-Aluminum",
                    materialCategory="metal",
                    materialStandard=MaterialStandard.ISO,
                    standardDesignation="AL6061-T6",
                    composition=[
                        {"element": "Al", "percentage": 97.5, "unit": "weight_percent"},
                        {"element": "Mg", "percentage": 1.0, "unit": "weight_percent"},
                        {"element": "Si", "percentage": 0.6, "unit": "weight_percent"}
                    ],
                    properties=[
                        {"propertyName": "density", "value": 2.7, "unit": "g/cm3"},
                        {"propertyName": "tensile_strength", "value": 310, "unit": "MPa"}
                    ],
                    traceability=MaterialTraceability(
                        batchNumber="BATCH-001",
                        url="https://example.com/traceability/BATCH-001"
                    )
                )
             },
            totalMass=2.5,
            materialBreakdown={
                "metal": 97.5,
                "plastic": 2.5
            }
        ),
        additionalData=AdditionalData(
            data_type="quality_metrics",
            data={
                "quality_score": 95,
                "durability_rating": "A+",
                "test_results": {
                    "impact_resistance": "Passed",
                    "weather_resistance": "Passed",
                    "chemical_resistance": "Passed"
                },
                "certifications": [
                    "ISO 9001",
                    "ISO 14001",
                    "CE Mark"
                ]
            }
        )
    )
    
    # Test all main sections exist and are properly populated
    assert isinstance(passport.metadata, Metadata)
    assert isinstance(passport.productIdentifier, ProductIdentifier)
    assert isinstance(passport.circularity, Circularity)
    assert isinstance(passport.carbonFootprint, CarbonFootprint)
    assert isinstance(passport.reManufacture, RepairModel)
    assert isinstance(passport.productMaterial, ProductMaterial)
    assert isinstance(passport.additionalData, AdditionalData)
    
    # Test specific fields in each section
    assert passport.metadata.economic_operator_id == "company.com"
    assert passport.metadata.status == StatusEnum.ACTIVE
    assert passport.productIdentifier.serialID == "SN-001"
    assert len(passport.circularity.recycledContent) == 1
    assert passport.circularity.recycledContent[0].preConsumerShare == 45.0
    assert passport.circularity.recycledContent[0].postConsumerShare == 30.5
    assert passport.carbonFootprint.productCarbonFootprint == None
    assert passport.reManufacture.currentCondition == ComponentCondition.SERVICEABLE
    assert passport.productMaterial.totalMass == 2.5
    assert passport.additionalData.data_type == "quality_metrics"
    assert passport.additionalData.data["quality_score"] == 95
    
    
    # Test serialization
    passport_dict = passport.model_dump()
    assert isinstance(passport_dict, dict)
    assert all(section in passport_dict for section in [
        "metadata", "productIdentifier", "circularity", "carbonFootprint",
        "reManufacture", "productMaterial", "additionalData"
    ])

    # Update the assertions
    assert passport.productMaterial.productId == "PROD-001"
    assert passport.productMaterial.totalMass == 2.5
    # Access components properly through the model
    main_body = passport.productMaterial.components["main_body"]
    assert main_body.materialId == "MAT-001"
    assert main_body.materialStandard == MaterialStandard.ISO
    assert len(main_body.composition) == 3

def test_incremental_passport_creation():
    """Test creating a passport by incrementally adding data"""
    current_time = datetime.now()
    
    # Create empty instances
    DPP_instance = DigitalProductPassport()
    
    # Populate metadata
    DPP_instance.metadata = Metadata()
    DPP_instance.metadata.economic_operator_id = "company.com"
    DPP_instance.metadata.registration_identifier = "https://www.eco123.company.com"
    DPP_instance.metadata.issue_date = current_time
    DPP_instance.metadata.status = StatusEnum.ACTIVE
    DPP_instance.metadata.version = "1.0.0"
    DPP_instance.metadata.passport_identifier = uuid.uuid4()
    DPP_instance.metadata.expiration_date = "2030-01-01"

    # Populate product identifier
    DPP_instance.productIdentifier = ProductIdentifier()
    DPP_instance.productIdentifier.batchID = "BATCH-001"
    DPP_instance.productIdentifier.serialID = "SN-001"
    DPP_instance.productIdentifier.productStatus = ProductStatus.ORIGINAL
    DPP_instance.productIdentifier.productName = "NMIS reference product"
    DPP_instance.productIdentifier.productDescription = "A test product for DPP"

    # Populate circularity
    DPP_instance.circularity = Circularity()
    recycled_content = RecycledContent(
        preConsumerShare=45.0,
        recycledMaterial=RecycledMaterialInfo(
            material=RecycledMaterial.ALUMINUM,
            materialInfoURL="https://example.com/materials/aluminum-info"
        ),
        postConsumerShare=30.5
    )
    DPP_instance.circularity.recycledContent = [recycled_content]
    
    # Add dismantling information
    dismantling_doc = DismantlingAndRemovalDocumentation(
        documentType=DocumentType.DISMANTLINGMANUAL,
        mimeType=MimeType.PDF,
        documentURL=ResourcePath(
            resourcePath="https://example.com/documents/dismantling-manual.pdf"
        )
    )
    DPP_instance.circularity.dismantlingAndRemovalInformation = [dismantling_doc]

    # Populate carbon footprint
    DPP_instance.carbonFootprint = CarbonFootprint()
    lifecycle_footprint = LifecycleStageCarbonFootprint(
        lifecycleStage=LifecycleStage.RAWMATERIALEXTRACTION,
        carbonFootprint=20.0
    )
    DPP_instance.carbonFootprint.carbonFootprintPerLifecycleStage = [lifecycle_footprint]
    DPP_instance.carbonFootprint.carbonFootprintStudy = "https://example.com/carbon-footprint-study"

    # Populate remanufacture information
    DPP_instance.reManufacture = RepairModel()
    DPP_instance.reManufacture.repairId = "REP-001"
    DPP_instance.reManufacture.currentCondition = ComponentCondition.SERVICEABLE
    
    # Add defect information
    defect = DefectInformation(
        defectId="DEF-001",
        description="Tip wear",
        location="blade_tip",
        dimensions={"length": 25.0, "width": 3.0, "depth": 1.5},
        severity=3
    )
    DPP_instance.reManufacture.defects = [defect]
    
    # Add repair history
    repair = RepairHistory(
        repairId="RH-001",
        repairDate=current_time,
        repairType=RepairType.SURFACE_TREATMENT,
        facility="Main Service Center",
        description="Initial inspection",
        technician="John Doe"
    )
    DPP_instance.reManufacture.repairHistory = [repair]

    # Populate material information
    DPP_instance.productMaterial = ProductMaterial()
    DPP_instance.productMaterial.productId = "PROD-001"
    
    material_info = MaterialInformation(
        materialId="MAT-001",
        tradeName="Eco-Aluminum",
        materialCategory="metal",
        materialStandard=MaterialStandard.ISO,
        standardDesignation="AL6061-T6",
        composition=[
            {"element": "Al", "percentage": 97.5, "unit": "weight_percent"},
            {"element": "Mg", "percentage": 1.0, "unit": "weight_percent"},
            {"element": "Si", "percentage": 0.6, "unit": "weight_percent"}
        ],
        properties=[
            {"propertyName": "density", "value": 2.7, "unit": "g/cm3"},
            {"propertyName": "tensile_strength", "value": 310, "unit": "MPa"}
        ],
        traceability=MaterialTraceability(
            batchNumber="BATCH-001",
            url="https://example.com/traceability/BATCH-001"
        )
    )
    DPP_instance.productMaterial.components = {"main_body": material_info}
    DPP_instance.productMaterial.totalMass = 2.5
    DPP_instance.productMaterial.materialBreakdown = {
        "metal": 97.5,
        "plastic": 2.5
    }

    # Add additional data
    DPP_instance.additionalData = AdditionalData(
        data_type="quality_metrics",
        data={
            "quality_score": 95,
            "durability_rating": "A+",
            "test_results": {
                "impact_resistance": "Passed",
                "weather_resistance": "Passed",
                "chemical_resistance": "Passed"
            },
            "certifications": [
                "ISO 9001",
                "ISO 14001",
                "CE Mark"
            ]
        }
    )

    # Verify all sections are properly populated
    assert DPP_instance.metadata.economic_operator_id == "company.com"
    assert DPP_instance.productIdentifier.serialID == "SN-001"
    assert DPP_instance.circularity.recycledContent[0].preConsumerShare == 45.0
    assert DPP_instance.carbonFootprint.carbonFootprintPerLifecycleStage[0].carbonFootprint == 20.0
    assert DPP_instance.reManufacture.currentCondition == ComponentCondition.SERVICEABLE
    assert DPP_instance.productMaterial.totalMass == 2.5
    assert DPP_instance.additionalData.data["quality_score"] == 95
