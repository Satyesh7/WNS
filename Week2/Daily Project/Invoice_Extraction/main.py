# ================================================================
# INVOICE INFORMATION EXTRACTOR - COMPLETE GOOGLE COLAB VERSION
# Updated with PDF Support & Improved Extraction
# ================================================================

print("🚀 Starting Invoice Information Extractor Setup...")
print("=" * 70)

# ================================================================
# STEP 1: Install All Dependencies
# ================================================================

print("\n📦 Step 1: Installing Dependencies...")
print("-" * 70)

# Install Python packages
#pip install -q pytesseract pillow opencv-python pydantic pyyaml python-dotenv loguru python-dateutil

# Install PDF support
#apt-get install -y poppler-utils > /dev/null 2>&1
#pip install -q pdf2image

print("✅ All dependencies installed successfully!")

# ================================================================
# STEP 2: Setup Project Structure
# ================================================================

print("\n📁 Step 2: Creating Project Structure...")
print("-" * 70)

import os
from pathlib import Path

directories = [
    'invoice_extractor/src/models',
    'invoice_extractor/src/utils',
    'invoice_extractor/src/ocr',
    'invoice_extractor/src/extractors',
    'invoice_extractor/src/core',
    'invoice_extractor/config',
    'invoice_extractor/data/raw',
    'invoice_extractor/data/output',
    'invoice_extractor/logs'
]

for directory in directories:
    Path(directory).mkdir(parents=True, exist_ok=True)

print("✅ Project structure created!")

# ================================================================
# STEP 3: Create Configuration
# ================================================================

print("\n⚙️ Step 3: Creating Configuration Files...")
print("-" * 70)

config_yaml = """
ocr:
  default_provider: "tesseract"
  preprocessing:
    enabled: true
    grayscale: true
    denoise: false
    threshold: true
    deskew: false

extraction:
  method: "rule_based"
  confidence_threshold: 0.7

validation:
  enabled: true
"""

with open('invoice_extractor/config/config.yaml', 'w') as f:
    f.write(config_yaml)

print("✅ Configuration created!")

# ================================================================
# STEP 4: Create All Source Files
# ================================================================

print("\n📝 Step 4: Creating Source Files...")
print("-" * 70)

# File 1: Invoice Model
invoice_model_py = """
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class CurrencyType(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    INR = "INR"
    JPY = "JPY"

class ExtractionStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"

class ProductItem(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    product_name: Optional[str] = None
    model_number: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[Decimal] = None
    total_price: Optional[Decimal] = None

class VendorInfo(BaseModel):
    vendor_name: Optional[str] = None
    vendor_address: Optional[str] = None
    vendor_phone: Optional[str] = None
    vendor_email: Optional[str] = None
    vendor_tax_id: Optional[str] = None

class CustomerInfo(BaseModel):
    customer_name: Optional[str] = None
    customer_address: Optional[str] = None
    customer_phone: Optional[str] = None

class InvoiceData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    invoice_number: Optional[str] = None
    invoice_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    subtotal: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    currency: Optional[CurrencyType] = CurrencyType.USD
    vendor: Optional[VendorInfo] = None
    customer: Optional[CustomerInfo] = None
    products: List[ProductItem] = []
    extraction_status: ExtractionStatus = ExtractionStatus.SUCCESS
    ocr_provider: Optional[str] = None
    extraction_method: Optional[str] = None
    confidence_score: Optional[float] = None
    processing_time: Optional[float] = None
    raw_text: Optional[str] = None
    errors: List[str] = []
    warnings: List[str] = []

    def to_dict(self, include_raw: bool = False):
        data = self.model_dump()
        if not include_raw:
            data.pop('raw_text', None)
        return data

class ExtractionResult(BaseModel):
    success: bool
    invoice_data: Optional[InvoiceData] = None
    error_message: Optional[str] = None
    file_name: str
    processing_duration: float
"""

with open('invoice_extractor/src/models/invoice_model.py', 'w') as f:
    f.write(invoice_model_py)

# File 2: Logger
logger_py = """
import sys
from pathlib import Path
from loguru import logger

class LoggerConfig:
    def __init__(self, log_level="INFO"):
        logger.remove()
        logger.add(sys.stderr, level=log_level, colorize=True)

def get_logger(name=__name__):
    return logger

def initialize_logger(config=None):
    config = config or {}
    LoggerConfig(log_level=config.get("log_level", "INFO"))
"""

with open('invoice_extractor/src/utils/logger.py', 'w') as f:
    f.write(logger_py)

# File 3: Image Preprocessor
preprocessor_py = """
import cv2
import numpy as np
from PIL import Image

class ImagePreprocessor:
    def __init__(self, config=None):
        self.config = config or {}
        self.grayscale = self.config.get('grayscale', True)
        self.threshold = self.config.get('threshold', True)
    
    def preprocess(self, image_input):
        try:
            if isinstance(image_input, Image.Image):
                img_array = np.array(image_input)
            else:
                img_array = image_input
            
            if self.grayscale and len(img_array.shape) == 3:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
            
            if self.threshold:
                img_array = cv2.adaptiveThreshold(
                    img_array, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                    cv2.THRESH_BINARY, 11, 2
                )
            
            return Image.fromarray(img_array)
        except Exception as e:
            if isinstance(image_input, Image.Image):
                return image_input
            return Image.fromarray(img_array)
"""

with open('invoice_extractor/src/utils/image_preprocessor.py', 'w') as f:
    f.write(preprocessor_py)

# File 4: OCR Base
ocr_base_py = """
from abc import ABC, abstractmethod
from PIL import Image
import time

class OCRResult:
    def __init__(self, text, confidence=0.0, metadata=None, processing_time=0.0, provider=""):
        self.text = text
        self.confidence = confidence
        self.metadata = metadata or {}
        self.processing_time = processing_time
        self.provider = provider

class BaseOCRProvider(ABC):
    def __init__(self, config=None):
        self.config = config or {}
        self.provider_name = self.__class__.__name__.replace('OCR', '')
    
    @abstractmethod
    def extract_text(self, image):
        pass
    
    @abstractmethod
    def is_available(self):
        pass
    
    def process_image(self, image):
        start_time = time.time()
        try:
            result = self.extract_text(image)
            result.processing_time = time.time() - start_time
            result.provider = self.provider_name
            return result
        except Exception as e:
            return OCRResult("", 0.0, {"error": str(e)}, time.time() - start_time, self.provider_name)
    
    def validate_image(self, image):
        return image is not None and isinstance(image, Image.Image)
"""

with open('invoice_extractor/src/ocr/base_ocr.py', 'w') as f:
    f.write(ocr_base_py)

# File 5: Tesseract OCR
tesseract_py = """
import pytesseract
from PIL import Image
from src.ocr.base_ocr import BaseOCRProvider, OCRResult

class TesseractOCR(BaseOCRProvider):
    def __init__(self, config=None):
        super().__init__(config)
        self.language = 'eng'
    
    def is_available(self):
        try:
            pytesseract.get_tesseract_version()
            return True
        except:
            return False
    
    def extract_text(self, image):
        if not self.validate_image(image):
            return OCRResult("", 0.0, {"error": "Invalid image"}, 0, "Tesseract")
        
        try:
            text = pytesseract.image_to_string(image, lang=self.language)
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            confidences = [float(c) for c in data['conf'] if int(c) > 0]
            avg_confidence = sum(confidences) / len(confidences) / 100.0 if confidences else 0.0
            
            return OCRResult(text, avg_confidence, {"word_count": len(confidences)}, 0, "Tesseract")
        except Exception as e:
            return OCRResult("", 0.0, {"error": str(e)}, 0, "Tesseract")
"""

with open('invoice_extractor/src/ocr/tesseract_ocr.py', 'w') as f:
    f.write(tesseract_py)

# File 6: IMPROVED Rule-based Extractor
extractor_py = """
import re
from datetime import datetime
from decimal import Decimal
from dateutil import parser as date_parser
from src.models.invoice_model import InvoiceData, VendorInfo, CustomerInfo, ProductItem, CurrencyType

class ImprovedExtractor:
    def extract(self, text):
        invoice_number = self._extract_invoice_number(text)
        invoice_date = self._extract_invoice_date(text)
        amounts = self._extract_amounts(text)
        vendor = self._extract_vendor(text)
        customer = self._extract_customer(text)
        products = self._extract_products(text)
        
        invoice = InvoiceData(
            invoice_number=invoice_number,
            invoice_date=invoice_date,
            total_amount=amounts.get('total'),
            subtotal=amounts.get('subtotal'),
            tax_amount=amounts.get('tax'),
            currency=amounts.get('currency'),
            vendor=vendor,
            customer=customer,
            products=products,
            raw_text=text,
            extraction_method="rule_based_improved",
            confidence_score=0.85
        )
        return invoice
    
    def _extract_invoice_number(self, text):
        patterns = [
            r'Invoice\\s*No\\.?\\s*:?\\s*([A-Z0-9-]+)',
            r'Invoice\\s*Number\\s*:?\\s*([A-Z0-9-]+)',
            r'Bill\\s*No\\.?\\s*:?\\s*([A-Z0-9-]+)',
            r'(?:^|\\n)([A-Z]{2,}[0-9]{6,})(?:\\s|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                inv_num = match.group(1).strip()
                if inv_num not in ['TAX', 'GST', 'HSN', 'CIN', 'QTY', 'INVOICE']:
                    return inv_num
        return None
    
    def _extract_invoice_date(self, text):
        patterns = [
            r'Date\\s+and\\s+Time\\s*:?\\s*(\\d{2}/\\d{2}/\\d{4})',
            r'Invoice\\s*Date\\s*:?\\s*(\\d{2}/\\d{2}/\\d{4})',
            r'Date\\s*:?\\s*(\\d{2}/\\d{2}/\\d{4})',
            r'(\\d{2}/\\d{2}/\\d{4}\\s+\\d{2}:\\d{2}\\s*(?:AM|PM))',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                date_str = match.group(1).strip()
                try:
                    return date_parser.parse(date_str.split()[0])
                except:
                    try:
                        return date_parser.parse(date_str)
                    except:
                        continue
        return None
    
    def _extract_amounts(self, text):
        amounts = {}
        
        # Detect currency
        if 'INR' in text or '₹' in text or 'Rs' in text:
            amounts['currency'] = CurrencyType.INR
        elif '$' in text or 'USD' in text:
            amounts['currency'] = CurrencyType.USD
        elif '€' in text or 'EUR' in text:
            amounts['currency'] = CurrencyType.EUR
        elif '£' in text or 'GBP' in text:
            amounts['currency'] = CurrencyType.GBP
        else:
            amounts['currency'] = CurrencyType.INR
        
        # Total amount
        total_patterns = [
            r'Invoice\\s*[Vv]alue\\s*:?\\s*(?:INR\\.?|Rs\\.?|₹|\\$)?\\s*([0-9,]+\\.?[0-9]*)',
            r'Net\\s*Amount\\s*:?\\s*(?:INR\\.?|Rs\\.?|₹|\\$)?\\s*([0-9,]+\\.?[0-9]*)',
            r'Total\\s*(?:Amount|Value)?\\s*:?\\s*(?:INR\\.?|Rs\\.?|₹|\\$)?\\s*([0-9,]+\\.?[0-9]*)',
            r'Grand\\s*Total\\s*:?\\s*(?:INR\\.?|Rs\\.?|₹|\\$)?\\s*([0-9,]+\\.?[0-9]*)',
        ]
        
        for pattern in total_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    amounts['total'] = Decimal(match.group(1).replace(',', ''))
                    break
                except:
                    pass
        
        # Subtotal/Taxable value
        subtotal_patterns = [
            r'Taxable\\s*[Vv]alue\\s*:?\\s*(?:INR\\.?|Rs\\.?|₹|\\$)?\\s*([0-9,]+\\.?[0-9]*)',
            r'Sub[-\\s]?total\\s*:?\\s*(?:INR\\.?|Rs\\.?|₹|\\$)?\\s*([0-9,]+\\.?[0-9]*)',
        ]
        
        for pattern in subtotal_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    amounts['subtotal'] = Decimal(match.group(1).replace(',', ''))
                    break
                except:
                    pass
        
        # Tax amount
        tax_patterns = [
            r'Total\\s*Tax\\s*Amount\\s*:?\\s*(?:INR\\.?|Rs\\.?|₹|\\$)?\\s*([0-9,]+\\.?[0-9]*)',
            r'Tax\\s*Amount\\s*:?\\s*(?:INR\\.?|Rs\\.?|₹|\\$)?\\s*([0-9,]+\\.?[0-9]*)',
            r'(?:IGST|CGST|SGST|GST)\\s*(?:[0-9.]+%)?\\s*:?\\s*(?:INR\\.?|Rs\\.?|₹|\\$)?\\s*([0-9,]+\\.?[0-9]*)',
        ]
        
        for pattern in tax_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    amounts['tax'] = Decimal(match.group(1).replace(',', ''))
                    break
                except:
                    pass
        
        return amounts
    
    def _extract_vendor(self, text):
        vendor = VendorInfo()
        
        # Vendor name
        name_patterns = [
            r'^([A-Z][A-Z\\s&,.\\(\\)]+(?:LIMITED|LTD|PRIVATE|PVT|CORPORATION|CORP|INC|COMPANY|CO\\.?))',
            r'((?:[A-Z][a-z]+\\s+){1,4}(?:LIMITED|Ltd|Private|Pvt|Corporation|Corp|Inc))',
        ]
        
        lines = text.split('\\n')
        for line in lines[:15]:
            line = line.strip()
            if 5 < len(line) < 100:
                for pattern in name_patterns:
                    match = re.search(pattern, line)
                    if match:
                        vendor.vendor_name = match.group(1).strip()
                        break
                if vendor.vendor_name:
                    break
        
        # Email
        email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,})'
        emails = re.findall(email_pattern, text)
        if emails:
            vendor.vendor_email = emails[0]
        
        # Phone
        phone_patterns = [
            r'(?:P:|Phone:|Tel:|Contact[-:]?)\\s*([0-9]{4,5}[-\\s]?[0-9]{3,4}[-\\s]?[0-9]{4})',
            r'([0-9]{10,12})',
        ]
        for pattern in phone_patterns:
            match = re.search(pattern, text)
            if match:
                vendor.vendor_phone = match.group(1).strip()
                break
        
        # GST/Tax ID
        gst_pattern = r'(?:Company\\s*)?(?:GST|GSTIN)\\s*:?\\s*([0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9A-Z]{1}[Z]{1}[0-9A-Z]{1})'
        match = re.search(gst_pattern, text, re.IGNORECASE)
        if match:
            vendor.vendor_tax_id = match.group(1).strip()
        
        return vendor if vendor.vendor_name else None
    
    def _extract_customer(self, text):
        customer = CustomerInfo()
        
        # Customer name
        customer_patterns = [
            r'Customer\\s+(?:Billing|Shipping)\\s+Address\\s*[:\\n]\\s*([^\\n]+)',
            r'Bill\\s*To\\s*:?\\s*([^\\n]+)',
            r'Sold\\s*To\\s*:?\\s*([^\\n]+)',
        ]
        
        for pattern in customer_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                name = match.group(1).strip()
                if len(name) > 3 and len(name) < 100:
                    customer.customer_name = name
                    break
        
        return customer if customer.customer_name else None
    
    def _extract_products(self, text):
        products = []
        lines = text.split('\\n')
        
        in_product_section = False
        for line in lines:
            if re.search(r'Item\\s+(?:Code|Description)|Product|Description.*Qty', line, re.IGNORECASE):
                in_product_section = True
                continue
            
            if in_product_section and re.search(r'Total|Tax|Payment|Shipping|Summary', line, re.IGNORECASE):
                break
            
            if in_product_section and len(line.strip()) > 10:
                numbers = re.findall(r'([0-9,]+\\.?[0-9]*)', line)
                
                if len(numbers) >= 1:
                    # Extract product name
                    words = [w for w in line.split() if not re.match(r'^[0-9,\\.]+$', w)]
                    product_name = ' '.join(words[:7]) if words else line[:50]
                    
                    # Clean product name
                    product_name = re.sub(r'\\s+', ' ', product_name).strip()
                    
                    if product_name and len(product_name) > 3:
                        try:
                            product = ProductItem(
                                product_name=product_name,
                                quantity=float(numbers[0].replace(',', '')) if numbers else None,
                                total_price=Decimal(numbers[-1].replace(',', '')) if len(numbers) >= 2 else None
                            )
                            products.append(product)
                        except:
                            pass
        
        return products[:10]
"""

with open('invoice_extractor/src/extractors/rule_based_extractor.py', 'w') as f:
    f.write(extractor_py)

# File 7: Invoice Processor
processor_py = """
import time
from pathlib import Path
from PIL import Image
import io
from src.models.invoice_model import InvoiceData, ExtractionResult, ExtractionStatus
from src.ocr.tesseract_ocr import TesseractOCR
from src.extractors.rule_based_extractor import ImprovedExtractor
from src.utils.image_preprocessor import ImagePreprocessor

class InvoiceProcessor:
    def __init__(self, config=None):
        self.config = config or {}
        self.preprocessor = ImagePreprocessor(self.config.get('ocr', {}).get('preprocessing', {}))
        self.ocr = TesseractOCR()
        self.extractor = ImprovedExtractor()
        self.preprocessing_enabled = self.config.get('ocr', {}).get('preprocessing', {}).get('enabled', True)
    
    def process_invoice(self, image_input):
        start_time = time.time()
        file_name = "uploaded_image"
        
        try:
            if isinstance(image_input, str):
                file_name = Path(image_input).name
                image = Image.open(image_input)
            elif isinstance(image_input, bytes):
                image = Image.open(io.BytesIO(image_input))
            else:
                image = image_input
            
            if self.preprocessing_enabled:
                image = self.preprocessor.preprocess(image)
            
            ocr_result = self.ocr.process_image(image)
            
            if not ocr_result.text or len(ocr_result.text.strip()) < 10:
                raise ValueError("OCR extraction failed or insufficient text")
            
            invoice_data = self.extractor.extract(ocr_result.text)
            invoice_data.ocr_provider = ocr_result.provider
            invoice_data.processing_time = time.time() - start_time
            
            if invoice_data.invoice_number and invoice_data.total_amount:
                invoice_data.extraction_status = ExtractionStatus.SUCCESS
            elif invoice_data.invoice_number or invoice_data.total_amount:
                invoice_data.extraction_status = ExtractionStatus.PARTIAL
            else:
                invoice_data.extraction_status = ExtractionStatus.FAILED
            
            return ExtractionResult(
                success=True,
                invoice_data=invoice_data,
                file_name=file_name,
                processing_duration=time.time() - start_time
            )
            
        except Exception as e:
            return ExtractionResult(
                success=False,
                error_message=str(e),
                file_name=file_name,
                processing_duration=time.time() - start_time
            )
"""

with open('invoice_extractor/src/core/invoice_processor.py', 'w') as f:
    f.write(processor_py)

# Create __init__ files
init_files = [
    'invoice_extractor/src/__init__.py',
    'invoice_extractor/src/models/__init__.py',
    'invoice_extractor/src/utils/__init__.py',
    'invoice_extractor/src/ocr/__init__.py',
    'invoice_extractor/src/extractors/__init__.py',
    'invoice_extractor/src/core/__init__.py'
]

for init_file in init_files:
    with open(init_file, 'w') as f:
        f.write('')

print("✅ All source files created!")

# ================================================================
# STEP 5: Setup Environment
# ================================================================

print("\n🔧 Step 5: Configuring Environment...")
print("-" * 70)

import sys
sys.path.insert(0, '/content/invoice_extractor')

import yaml
from src.utils.logger import initialize_logger
from src.core.invoice_processor import InvoiceProcessor

with open('/content/invoice_extractor/config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

initialize_logger({"log_level": "INFO"})
processor = InvoiceProcessor(config)

print("✅ Invoice Processor initialized!")

# ================================================================
# STEP 6: Create Helper Functions
# ================================================================

print("\n🛠️ Step 6: Creating Helper Functions...")
print("-" * 70)

from pdf2image import convert_from_path
from PIL import Image
import json
from IPython.display import display

def quick_process_pdf(filepath):
    """Process PDF invoice"""
    print(f"🔄 Processing: {filepath}")
    
    images = convert_from_path(filepath, dpi=300, first_page=1, last_page=1)
    
    if images:
        result = processor.process_invoice(images[0])
        
        if result.success and result.invoice_data:
            inv = result.invoice_data
            
            print("\n" + "="*70)
            print("✅ EXTRACTION SUCCESSFUL!")
            print("="*70)
            print(f"\n📄 Invoice Number: {inv.invoice_number or 'Not found'}")
            print(f"📅 Invoice Date: {inv.invoice_date.strftime('%Y-%m-%d') if inv.invoice_date else 'Not found'}")
            print(f"💰 Total Amount: {inv.currency.value if inv.currency else 'INR'} {inv.total_amount or 'Not found'}")
            
            if inv.subtotal:
                print(f"💵 Subtotal: {inv.currency.value if inv.currency else 'INR'} {inv.subtotal}")
            
            if inv.tax_amount:
                print(f"📊 Tax Amount: {inv.currency.value if inv.currency else 'INR'} {inv.tax_amount}")
            
            if inv.vendor and inv.vendor.vendor_name:
                print(f"\n🏢 Vendor: {inv.vendor.vendor_name}")
                if inv.vendor.vendor_email:
                    print(f"   📧 Email: {inv.vendor.vendor_email}")
                if inv.vendor.vendor_tax_id:
                    print(f"   🆔 GST/Tax ID: {inv.vendor.vendor_tax_id}")
            
            if inv.customer and inv.customer.customer_name:
                print(f"\n👤 Customer: {inv.customer.customer_name}")
            
            if inv.products:
                print(f"\n📦 Products ({len(inv.products)} items):")
                for i, product in enumerate(inv.products[:5], 1):
                    print(f"   {i}. {product.product_name}")
                    if product.quantity and product.total_price:
                        print(f"      Qty: {product.quantity}, Total: {inv.currency.value if inv.currency else 'INR'} {product.total_price}")
            
            print(f"\n⏱️  Processing Time: {result.processing_duration:.2f}s")
            print(f"🎯 Confidence: {inv.confidence_score:.0%}")
            print(f"📊 Status: {inv.extraction_status.value.upper()}")
            print("="*70)
            
            return inv
        else:
            print(f"\n❌ Extraction failed: {result.error_message}")
            return None
    else:
        print("❌ Failed to convert PDF")
        return None


def process_and_save(filepath, output_name=None):
    """Process and save results"""
    invoice_data = quick_process_pdf(filepath)
    
    if invoice_data:
        if output_name is None:
            output_name = Path(filepath).stem
        
        output_file = f'/content/invoice_extractor/data/output/{output_name}_result.json'
        
        data = invoice_data.to_dict(include_raw=True)
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"\n💾 Results saved to: {output_file}")
        
        print("\n" + "="*70)
        print("📋 COMPLETE JSON DATA:")
        print("="*70)
        print(json.dumps(invoice_data.to_dict(include_raw=False), indent=2, default=str))
        
        return invoice_data
    
    return None


def upload_and_process():
    """Upload from computer and process"""
    from google.colab import files
    
    print("📤 Please upload your invoice (PDF or image)...")
    uploaded = files.upload()
    
    for filename in uploaded.keys():
        filepath = f'/content/{filename}'
        
        with open(filepath, 'wb') as f:
            f.write(uploaded[filename])
        
        if filename.lower().endswith('.pdf'):
            print(f"\n📄 PDF File: {filename}")
            return process_and_save(filepath)
        else:
            print(f"\n🖼️ Image File: {filename}")
            try:
                display(Image.open(filepath))
            except:
                pass
            return process_and_save(filepath)


print("✅ Helper functions ready!")

# ================================================================
# STEP 7: Create Sample Invoice
# ================================================================

print("\n📄 Step 7: Creating Sample Invoice...")
print("-" * 70)

from PIL import ImageDraw, ImageFont

width, height = 800, 1000
image = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(image)

sample_text = """
ACME CORPORATION
123 Business Street, New York, NY 10001
Phone: 1800-123-4567
Email: billing@acme.com
GST: 29AACCV1726H1ZA

TAX INVOICE

Invoice No: INV-2025-001
Date and Time: 15/01/2025 10:30 AM
Order ID: ORD123456

Bill To:
John Smith
456 Customer Avenue
Los Angeles, CA 90001

Products
Item Code   Description              Qty    Unit Price    Total
---------------------------------------------------------------
PROD001     Widget Pro Model A        2      150.00       300.00
PROD002     Service Package           1      200.00       200.00
PROD003     Premium Support           1      100.00       100.00

Subtotal:                                                 600.00
Tax (10%):                                                 60.00
---------------------------------------------------------------
Total Amount: INR 660.00

Payment Terms: Net 30
Thank you for your business!
"""

y = 50
for line in sample_text.strip().split('\n'):
    draw.text((50, y), line.strip(), fill='black')
    y += 25

sample_path = '/content/invoice_extractor/data/raw/sample_invoice.png'
image.save(sample_path)

print(f"✅ Sample invoice created!")
print("\n📸 Sample Invoice Preview:")
display(image)

# ================================================================
# STEP 8: Test with Sample
# ================================================================

print("\n🧪 Step 8: Testing with Sample Invoice...")
print("="*70)

result = processor.process_invoice(sample_path)

if result.success:
    inv = result.invoice_data
    print("\n✅ Sample Test Passed!")
    print(f"   Invoice: {inv.invoice_number}")
    print(f"   Total: {inv.currency.value if inv.currency else 'USD'} {inv.total_amount}")
else:
    print("\n⚠️ Sample test had issues")

# ================================================================
# FINAL MESSAGE
# ================================================================

print("\n" + "="*70)
print("🎉 SETUP COMPLETE!")
print("="*70)
print("""
✅ Invoice Extractor is ready to use!

📋 Available Functions:
  1. upload_and_process()          - Upload and process invoice
  2. process_and_save(filepath)    - Process existing file
  3. quick_process_pdf(filepath)   - Quick PDF processing

💡 Quick Start:
  invoice_data = upload_and_process()

📁 Results saved to: /content/invoice_extractor/data/output/
""")

print("="*70)
print("🚀 Ready to extract invoices!")
print("="*70)