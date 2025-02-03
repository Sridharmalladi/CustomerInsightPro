# src/models/__init__.py
from .customer_segmentation import CustomerSegmentation
from .pattern_analyzer import PatternAnalyzer
from .prediction_model import PredictionModel

# src/models/customer_segmentation.py
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from typing import Dict, List

class CustomerSegmentation:
    def __init__(self, n_clusters: int = 5):
        self.n_clusters = n_clusters
        self.model = KMeans(n_clusters=n_clusters, random_state=42)
        self.feature_columns = [
            'total_spent',
            'purchase_frequency',
            'avg_transaction',
            'days_since_last_purchase'
        ]
    
    def fit_predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """Segment customers and return labeled data."""
        features = self._prepare_features(data)
        data['segment'] = self.model.fit_predict(features)
        data['segment'] = data['segment'].map(
            lambda x: f'Segment_{x+1}'
        )
        return data
    
    def _prepare_features(self, data: pd.DataFrame) -> np.ndarray:
        return data[self.feature_columns].values

# src/models/pattern_analyzer.py
import pandas as pd
import numpy as np
from typing import Dict, Any
from datetime import datetime

class PatternAnalyzer:
    def __init__(self):
        self.metrics = {}
    
    def analyze_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze customer consumption patterns."""
        return {
            'temporal': self._analyze_temporal_patterns(data),
            'categorical': self._analyze_categorical_patterns(data),
            'monetary': self._analyze_monetary_patterns(data)
        }
    
    def _analyze_temporal_patterns(self, data: pd.DataFrame) -> Dict[str, float]:
        """Analyze time-based patterns."""
        daily_stats = data.groupby(
            pd.Grouper(key='date', freq='D')
        )['amount'].agg(['count', 'sum'])
        
        return {
            'avg_daily_transactions': daily_stats['count'].mean(),
            'avg_daily_revenue': daily_stats['sum'].mean(),
            'peak_day_transactions': daily_stats['count'].max()
        }
    
    def _analyze_categorical_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze category-based patterns."""
        category_stats = data.groupby('product_category').agg({
            'amount': ['count', 'sum', 'mean'],
            'customer_id': 'nunique'
        })
        
        return {
            'top_categories': category_stats.nlargest(3, ('amount', 'count')),
            'highest_value_categories': category_stats.nlargest(3, ('amount', 'sum'))
        }
    
    def _analyze_monetary_patterns(self, data: pd.DataFrame) -> Dict[str, float]:
        """Analyze spending patterns."""
        return {
            'avg_transaction_value': data['amount'].mean(),
            'median_transaction_value': data['amount'].median(),
            'spending_std': data['amount'].std()
        }

# src/models/prediction_model.py
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from typing import Dict, Tuple

class PredictionModel:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.features = [
            'purchase_frequency',
            'avg_transaction',
            'days_since_last_purchase',
            'total_spent'
        ]
    
    def train(self, data: pd.DataFrame) -> Dict[str, float]:
        """Train the model and return performance metrics."""
        X = data[self.features]
        y = data['lifetime_value']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        return {
            'train_score': self.model.score(X_train, y_train),
            'test_score': self.model.score(X_test, y_test)
        }
    
    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """Make predictions for new data."""
        return self.model.predict(data[self.features])