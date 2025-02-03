# src/data/__init__.py
from .data_loader import DataLoader
from .data_preprocessor import DataPreprocessor

# src/data/data_loader.py
import pandas as pd
import sqlalchemy as db
from typing import Dict, Any
import yaml
from pathlib import Path

class DataLoader:
    def __init__(self, config_path: str = 'config/database.yaml'):
        self.config = self._load_config(config_path)
        self.engine = self._create_engine()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)['development']
    
    def _create_engine(self) -> db.Engine:
        conn_str = f"postgresql://{self.config['user']}:{self.config['password']}@" \
                  f"{self.config['host']}:{self.config['port']}/{self.config['database']}"
        return db.create_engine(conn_str)
    
    def load_customer_data(self) -> pd.DataFrame:
        query = """
        SELECT * FROM customers 
        LEFT JOIN customer_patterns ON customers.customer_id = customer_patterns.customer_id
        """
        return pd.read_sql(query, self.engine)
    
    def load_transactions(self, days: int = 365) -> pd.DataFrame:
        query = f"""
        SELECT * FROM transactions 
        WHERE date >= CURRENT_DATE - INTERVAL '{days} days'
        """
        return pd.read_sql(query, self.engine)

# src/data/data_preprocessor.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Tuple, List

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.numeric_features = [
            'total_spent', 
            'purchase_frequency',
            'avg_transaction',
            'days_since_last_purchase'
        ]
    
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Main preprocessing pipeline."""
        df = self._handle_missing_values(df)
        df = self._create_features(df)
        df = self._scale_numeric_features(df)
        return df
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        # Handle numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        # Handle categorical columns
        cat_cols = df.select_dtypes(include=['object']).columns
        df[cat_cols] = df[cat_cols].fillna(df[cat_cols].mode().iloc[0])
        
        return df
    
    def _create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        
        # Calculate days since last purchase
        if 'last_purchase_date' in df.columns:
            df['days_since_last_purchase'] = (
                pd.Timestamp.now() - pd.to_datetime(df['last_purchase_date'])
            ).dt.days
        
        # Calculate purchase frequency if not exists
        if 'purchase_frequency' not in df.columns and 'transaction_id' in df.columns:
            df['purchase_frequency'] = df.groupby('customer_id')['transaction_id'].transform('count')
        
        return df
    
    def _scale_numeric_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Scale numeric features using StandardScaler."""
        features_to_scale = [f for f in self.numeric_features if f in df.columns]
        if features_to_scale:
            df[features_to_scale] = self.scaler.fit_transform(df[features_to_scale])
        return df