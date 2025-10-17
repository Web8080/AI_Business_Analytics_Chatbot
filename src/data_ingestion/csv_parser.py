"""
CSV Parsing Module - Intelligent CSV file parsing with validation
"""
import pandas as pd
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import chardet

logger = logging.getLogger(__name__)


class CSVParser:
    """Parse and validate CSV files"""
    
    def __init__(self):
        """Initialize CSV parser"""
        self.supported_formats = ['.csv', '.tsv', '.txt']
    
    def parse_csv(self, file_path: str, **kwargs) -> Dict[str, Any]:
        """
        Parse CSV file with intelligent delimiter detection
        
        Args:
            file_path: Path to CSV file
            **kwargs: Additional pandas read_csv arguments
            
        Returns:
            Dictionary containing DataFrame and metadata
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"CSV file not found: {file_path}")
            
            logger.info(f"Parsing CSV: {file_path}")
            
            # Detect encoding
            encoding = self._detect_encoding(file_path)
            
            # Detect delimiter if not provided
            delimiter = kwargs.get('delimiter') or kwargs.get('sep')
            if not delimiter:
                delimiter = self._detect_delimiter(file_path, encoding)
            
            # Read CSV
            df = pd.read_csv(
                file_path,
                encoding=encoding,
                sep=delimiter,
                **{k: v for k, v in kwargs.items() if k not in ['delimiter', 'sep']}
            )
            
            # Validate and analyze
            validation_results = self._validate_dataframe(df)
            
            result = {
                'file_name': file_path.name,
                'dataframe': df,
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': df.columns.tolist(),
                'encoding': encoding,
                'delimiter': delimiter,
                'validation': validation_results,
                'status': 'success'
            }
            
            logger.info(f"Successfully parsed CSV: {len(df)} rows, {len(df.columns)} columns")
            return result
            
        except Exception as e:
            logger.error(f"Error parsing CSV {file_path}: {str(e)}")
            return {
                'file_name': str(file_path),
                'status': 'error',
                'error': str(e),
                'dataframe': pd.DataFrame()
            }
    
    def _detect_encoding(self, file_path: Path) -> str:
        """
        Detect file encoding
        
        Args:
            file_path: Path to file
            
        Returns:
            Detected encoding
        """
        try:
            with open(file_path, 'rb') as f:
                result = chardet.detect(f.read(10000))
                encoding = result['encoding'] or 'utf-8'
                logger.debug(f"Detected encoding: {encoding} (confidence: {result['confidence']})")
                return encoding
        except Exception:
            return 'utf-8'
    
    def _detect_delimiter(self, file_path: Path, encoding: str) -> str:
        """
        Detect CSV delimiter
        
        Args:
            file_path: Path to file
            encoding: File encoding
            
        Returns:
            Detected delimiter
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                first_line = f.readline()
                
                # Count common delimiters
                delimiters = {
                    ',': first_line.count(','),
                    ';': first_line.count(';'),
                    '\t': first_line.count('\t'),
                    '|': first_line.count('|')
                }
                
                # Return delimiter with highest count
                delimiter = max(delimiters, key=delimiters.get)
                logger.debug(f"Detected delimiter: '{delimiter}'")
                return delimiter
                
        except Exception:
            return ','
    
    def _validate_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate DataFrame and provide quality metrics
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with validation results
        """
        validation = {
            'is_empty': df.empty,
            'duplicate_rows': df.duplicated().sum(),
            'duplicate_percentage': (df.duplicated().sum() / len(df) * 100) if len(df) > 0 else 0,
            'columns_with_nulls': {},
            'total_null_percentage': 0,
            'data_types': {},
            'numeric_columns': [],
            'categorical_columns': [],
            'date_columns': []
        }
        
        if df.empty:
            return validation
        
        # Check for nulls
        for col in df.columns:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                null_pct = (null_count / len(df)) * 100
                validation['columns_with_nulls'][col] = {
                    'count': int(null_count),
                    'percentage': round(null_pct, 2)
                }
        
        # Total null percentage
        total_nulls = df.isnull().sum().sum()
        total_cells = len(df) * len(df.columns)
        validation['total_null_percentage'] = round((total_nulls / total_cells * 100), 2)
        
        # Data types
        for col in df.columns:
            dtype = str(df[col].dtype)
            validation['data_types'][col] = dtype
            
            if pd.api.types.is_numeric_dtype(df[col]):
                validation['numeric_columns'].append(col)
            elif pd.api.types.is_object_dtype(df[col]):
                # Check if it might be a date
                try:
                    pd.to_datetime(df[col].dropna().head(10), errors='raise')
                    validation['date_columns'].append(col)
                except Exception:
                    validation['categorical_columns'].append(col)
        
        return validation
    
    def parse_excel(self, file_path: str, sheet_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse Excel file
        
        Args:
            file_path: Path to Excel file
            sheet_name: Specific sheet name to read (None = all sheets)
            
        Returns:
            Dictionary containing DataFrame(s) and metadata
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"Excel file not found: {file_path}")
            
            logger.info(f"Parsing Excel: {file_path}")
            
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                validation_results = self._validate_dataframe(df)
                
                result = {
                    'file_name': file_path.name,
                    'sheet_name': sheet_name,
                    'dataframe': df,
                    'rows': len(df),
                    'columns': len(df.columns),
                    'validation': validation_results,
                    'status': 'success'
                }
            else:
                # Read all sheets
                excel_file = pd.ExcelFile(file_path)
                sheets = {}
                
                for sheet in excel_file.sheet_names:
                    df = pd.read_excel(file_path, sheet_name=sheet)
                    validation_results = self._validate_dataframe(df)
                    sheets[sheet] = {
                        'dataframe': df,
                        'rows': len(df),
                        'columns': len(df.columns),
                        'validation': validation_results
                    }
                
                result = {
                    'file_name': file_path.name,
                    'sheet_names': excel_file.sheet_names,
                    'sheets': sheets,
                    'status': 'success'
                }
            
            logger.info(f"Successfully parsed Excel file")
            return result
            
        except Exception as e:
            logger.error(f"Error parsing Excel {file_path}: {str(e)}")
            return {
                'file_name': str(file_path),
                'status': 'error',
                'error': str(e),
                'dataframe': pd.DataFrame()
            }

