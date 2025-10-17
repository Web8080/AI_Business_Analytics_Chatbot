"""
Data Cleaning Module - Automated data cleaning and preprocessing
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class DataCleaner:
    """Automated data cleaning and preprocessing"""
    
    def __init__(self):
        """Initialize data cleaner"""
        self.cleaning_report = []
    
    def clean_dataframe(self, df: pd.DataFrame, config: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Comprehensive data cleaning pipeline
        
        Args:
            df: Input DataFrame
            config: Cleaning configuration (optional)
            
        Returns:
            Tuple of (cleaned DataFrame, cleaning report)
        """
        if df.empty:
            return df, {'status': 'empty', 'actions': []}
        
        logger.info("Starting data cleaning pipeline")
        self.cleaning_report = []
        original_shape = df.shape
        
        df_clean = df.copy()
        
        # Step 1: Handle duplicates
        df_clean = self._remove_duplicates(df_clean)
        
        # Step 2: Handle missing values
        df_clean = self._handle_missing_values(df_clean, config)
        
        # Step 3: Handle outliers in numeric columns
        df_clean = self._handle_outliers(df_clean, config)
        
        # Step 4: Standardize data types
        df_clean = self._standardize_data_types(df_clean)
        
        # Step 5: Clean text columns
        df_clean = self._clean_text_columns(df_clean)
        
        # Step 6: Standardize column names
        df_clean = self._standardize_column_names(df_clean)
        
        report = {
            'original_shape': original_shape,
            'final_shape': df_clean.shape,
            'rows_removed': original_shape[0] - df_clean.shape[0],
            'actions': self.cleaning_report,
            'status': 'success'
        }
        
        logger.info(f"Data cleaning complete: {original_shape} -> {df_clean.shape}")
        return df_clean, report
    
    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows"""
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            df = df.drop_duplicates()
            self.cleaning_report.append({
                'action': 'remove_duplicates',
                'rows_removed': int(duplicates),
                'message': f'Removed {duplicates} duplicate rows'
            })
            logger.info(f"Removed {duplicates} duplicate rows")
        return df
    
    def _handle_missing_values(self, df: pd.DataFrame, config: Optional[Dict] = None) -> pd.DataFrame:
        """Handle missing values intelligently"""
        missing_threshold = config.get('missing_threshold', 0.5) if config else 0.5
        
        # Remove columns with too many missing values
        cols_to_drop = []
        for col in df.columns:
            missing_pct = df[col].isnull().sum() / len(df)
            if missing_pct > missing_threshold:
                cols_to_drop.append(col)
        
        if cols_to_drop:
            df = df.drop(columns=cols_to_drop)
            self.cleaning_report.append({
                'action': 'remove_high_missing_columns',
                'columns': cols_to_drop,
                'message': f'Removed {len(cols_to_drop)} columns with >{missing_threshold*100}% missing values'
            })
            logger.info(f"Removed columns with high missing values: {cols_to_drop}")
        
        # Fill missing values for remaining columns
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                if pd.api.types.is_numeric_dtype(df[col]):
                    # Use median for numeric columns
                    median_val = df[col].median()
                    df[col].fillna(median_val, inplace=True)
                    self.cleaning_report.append({
                        'action': 'fill_missing_numeric',
                        'column': col,
                        'method': 'median',
                        'value': float(median_val) if not pd.isna(median_val) else None,
                        'count': int(missing_count)
                    })
                else:
                    # Use mode for categorical columns
                    if not df[col].mode().empty:
                        mode_val = df[col].mode()[0]
                        df[col].fillna(mode_val, inplace=True)
                        self.cleaning_report.append({
                            'action': 'fill_missing_categorical',
                            'column': col,
                            'method': 'mode',
                            'value': str(mode_val),
                            'count': int(missing_count)
                        })
                    else:
                        df[col].fillna('Unknown', inplace=True)
                        self.cleaning_report.append({
                            'action': 'fill_missing_categorical',
                            'column': col,
                            'method': 'default',
                            'value': 'Unknown',
                            'count': int(missing_count)
                        })
        
        return df
    
    def _handle_outliers(self, df: pd.DataFrame, config: Optional[Dict] = None) -> pd.DataFrame:
        """Detect and handle outliers using IQR method"""
        outlier_threshold = config.get('outlier_threshold', 3.0) if config else 3.0
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - outlier_threshold * IQR
            upper_bound = Q3 + outlier_threshold * IQR
            
            outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            
            if outliers > 0:
                # Cap outliers instead of removing
                df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
                self.cleaning_report.append({
                    'action': 'cap_outliers',
                    'column': col,
                    'count': int(outliers),
                    'bounds': {'lower': float(lower_bound), 'upper': float(upper_bound)},
                    'message': f'Capped {outliers} outliers in {col}'
                })
                logger.info(f"Capped {outliers} outliers in column: {col}")
        
        return df
    
    def _standardize_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize and convert data types"""
        for col in df.columns:
            # Try to convert to datetime
            if df[col].dtype == 'object':
                try:
                    # Check if it looks like a date
                    sample = df[col].dropna().head(10)
                    if len(sample) > 0:
                        test_conversion = pd.to_datetime(sample, errors='coerce')
                        if test_conversion.notna().sum() / len(sample) > 0.8:
                            df[col] = pd.to_datetime(df[col], errors='coerce')
                            self.cleaning_report.append({
                                'action': 'convert_to_datetime',
                                'column': col,
                                'message': f'Converted {col} to datetime'
                            })
                            logger.info(f"Converted column to datetime: {col}")
                except Exception:
                    pass
                
                # Try to convert to numeric
                try:
                    if df[col].dtype == 'object':
                        cleaned = df[col].astype(str).str.replace(r'[$,€£¥%]', '', regex=True).str.strip()
                        numeric_col = pd.to_numeric(cleaned, errors='coerce')
                        if numeric_col.notna().sum() / len(df) > 0.8:
                            df[col] = numeric_col
                            self.cleaning_report.append({
                                'action': 'convert_to_numeric',
                                'column': col,
                                'message': f'Converted {col} to numeric'
                            })
                            logger.info(f"Converted column to numeric: {col}")
                except Exception:
                    pass
        
        return df
    
    def _clean_text_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean text columns"""
        text_cols = df.select_dtypes(include=['object']).columns
        
        for col in text_cols:
            # Strip whitespace
            df[col] = df[col].astype(str).str.strip()
            
            # Remove multiple spaces
            df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
            
            # Replace common inconsistencies
            df[col] = df[col].replace(['nan', 'NaN', 'null', 'NULL', 'None'], np.nan)
        
        if text_cols.any():
            self.cleaning_report.append({
                'action': 'clean_text',
                'columns': text_cols.tolist(),
                'message': f'Cleaned {len(text_cols)} text columns'
            })
        
        return df
    
    def _standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names"""
        original_cols = df.columns.tolist()
        
        # Convert to snake_case
        new_cols = []
        for col in df.columns:
            # Replace spaces and special characters with underscores
            new_col = str(col).lower()
            new_col = new_col.replace(' ', '_')
            new_col = ''.join(c if c.isalnum() or c == '_' else '_' for c in new_col)
            new_col = '_'.join(filter(None, new_col.split('_')))  # Remove consecutive underscores
            new_cols.append(new_col)
        
        df.columns = new_cols
        
        if original_cols != new_cols:
            self.cleaning_report.append({
                'action': 'standardize_column_names',
                'mapping': dict(zip(original_cols, new_cols)),
                'message': 'Standardized column names to snake_case'
            })
            logger.info("Standardized column names")
        
        return df
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Comprehensive data quality validation
        
        Args:
            df: Input DataFrame
            
        Returns:
            Data quality report
        """
        if df.empty:
            return {'status': 'empty', 'quality_score': 0}
        
        report = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / (1024 * 1024),
            'completeness': {},
            'consistency': {},
            'validity': {},
            'quality_score': 0
        }
        
        # Completeness - check for missing values
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        report['completeness']['missing_percentage'] = round(missing_pct, 2)
        report['completeness']['complete_rows'] = df.dropna().shape[0]
        completeness_score = max(0, 100 - missing_pct)
        
        # Consistency - check for duplicates
        duplicate_pct = (df.duplicated().sum() / len(df)) * 100
        report['consistency']['duplicate_percentage'] = round(duplicate_pct, 2)
        consistency_score = max(0, 100 - duplicate_pct)
        
        # Validity - check data types and ranges
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        invalid_count = 0
        for col in numeric_cols:
            if (df[col] < 0).any():
                # Check if negative values make sense
                invalid_count += (df[col] < 0).sum()
        
        validity_score = max(0, 100 - (invalid_count / len(df) * 100))
        report['validity']['potentially_invalid_values'] = int(invalid_count)
        
        # Calculate overall quality score
        report['quality_score'] = round(
            (completeness_score + consistency_score + validity_score) / 3, 2
        )
        
        report['status'] = 'success'
        
        return report

