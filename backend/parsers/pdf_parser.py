import PyPDF2
import io

class PDFParser:
    """Parser for PDF resume files"""
    
    @staticmethod
    def parse(file_path):
        """
        Extract text from PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text as string
        """
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
                    
            return text.strip()
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    @staticmethod
    def parse_from_bytes(file_bytes):
        """
        Extract text from PDF bytes
        
        Args:
            file_bytes: PDF file as bytes
            
        Returns:
            Extracted text as string
        """
        try:
            text = ""
            pdf_file = io.BytesIO(file_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
                
            return text.strip()
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
