"""
PDF Parsing Module - Intelligent extraction of tables and text from PDF documents
"""
import pandas as pd
import pdfplumber
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class PDFParser:
    """Parse PDF files and extract structured data"""
    
    def __init__(self):
        """Initialize PDF parser"""
        self.supported_formats = ['.pdf']
    
    def parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """
        Parse PDF file and extract tables and text
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Dictionary containing extracted tables and metadata
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"PDF file not found: {file_path}")
            
            logger.info(f"Parsing PDF: {file_path}")
            
            tables = []
            text_content = []
            
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text
                    text = page.extract_text()
                    if text:
                        text_content.append({
                            'page': page_num,
                            'text': text
                        })
                    
                    # Extract tables
                    page_tables = page.extract_tables()
                    for table_num, table in enumerate(page_tables, 1):
                        if table and len(table) > 1:
                            # Convert to DataFrame
                            df = self._table_to_dataframe(table)
                            if not df.empty:
                                tables.append({
                                    'page': page_num,
                                    'table_number': table_num,
                                    'dataframe': df,
                                    'rows': len(df),
                                    'columns': len(df.columns)
                                })
            
            result = {
                'file_name': file_path.name,
                'total_pages': len(pdf.pages) if 'pdf' in locals() else 0,
                'tables_found': len(tables),
                'tables': tables,
                'text_content': text_content,
                'status': 'success'
            }
            
            logger.info(f"Successfully parsed PDF: {len(tables)} tables found")
            return result
            
        except Exception as e:
            logger.error(f"Error parsing PDF {file_path}: {str(e)}")
            return {
                'file_name': str(file_path),
                'status': 'error',
                'error': str(e),
                'tables': [],
                'text_content': []
            }
    
    def _table_to_dataframe(self, table: List[List[str]]) -> pd.DataFrame:
        """
        Convert extracted table to pandas DataFrame
        
        Args:
            table: List of lists representing table rows
            
        Returns:
            Pandas DataFrame
        """
        try:
            if not table or len(table) < 2:
                return pd.DataFrame()
            
            # Use first row as headers
            headers = table[0]
            data = table[1:]
            
            # Create DataFrame
            df = pd.DataFrame(data, columns=headers)
            
            # Clean column names
            df.columns = [str(col).strip() if col else f"Column_{i}" 
                         for i, col in enumerate(df.columns)]
            
            # Remove empty rows
            df = df.dropna(how='all')
            
            # Attempt to infer numeric columns
            df = self._infer_numeric_types(df)
            
            return df
            
        except Exception as e:
            logger.warning(f"Error converting table to DataFrame: {str(e)}")
            return pd.DataFrame()
    
    def _infer_numeric_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Intelligently convert string columns to numeric where appropriate
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with inferred numeric types
        """
        for col in df.columns:
            try:
                # Remove common currency symbols and commas
                cleaned = df[col].astype(str).str.replace(r'[$,€£¥]', '', regex=True)
                cleaned = cleaned.str.strip()
                
                # Try to convert to numeric
                numeric_col = pd.to_numeric(cleaned, errors='coerce')
                
                # If more than 70% of values are numeric, convert the column
                if numeric_col.notna().sum() / len(df) > 0.7:
                    df[col] = numeric_col
                    
            except Exception:
                continue
        
        return df
    
    def extract_text_by_keywords(self, file_path: str, keywords: List[str]) -> Dict[str, List[str]]:
        """
        Extract text sections containing specific keywords
        
        Args:
            file_path: Path to PDF file
            keywords: List of keywords to search for
            
        Returns:
            Dictionary mapping keywords to matching text sections
        """
        result = {keyword: [] for keyword in keywords}
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        for keyword in keywords:
                            if keyword.lower() in text.lower():
                                # Extract paragraph containing keyword
                                paragraphs = text.split('\n\n')
                                for para in paragraphs:
                                    if keyword.lower() in para.lower():
                                        result[keyword].append(para.strip())
        
        except Exception as e:
            logger.error(f"Error extracting text by keywords: {str(e)}")
        
        return result

