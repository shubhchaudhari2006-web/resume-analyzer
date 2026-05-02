class TextParser:
    """Parser for TXT resume files"""
    
    @staticmethod
    def parse(file_path):
        """
        Extract text from TXT file
        
        Args:
            file_path: Path to TXT file
            
        Returns:
            Extracted text as string
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return text.strip()
        except Exception as e:
            raise Exception(f"Error parsing TXT: {str(e)}")
    
    @staticmethod
    def parse_from_bytes(file_bytes):
        """
        Extract text from TXT bytes
        
        Args:
            file_bytes: TXT file as bytes
            
        Returns:
            Extracted text as string
        """
        try:
            text = file_bytes.decode('utf-8')
            return text.strip()
        except Exception as e:
            raise Exception(f"Error parsing TXT: {str(e)}")
