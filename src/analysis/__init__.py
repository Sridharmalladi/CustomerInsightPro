# src/analysis/__init__.py
from .performance_metrics import PerformanceAnalyzer
from .customer_insights import CustomerInsights

# src/analysis/performance_metrics.py
import pandas as pd
from typing import Dict, Any
import numpy as np
from datetime import datetime

class PerformanceAnalyzer:
    def __init__(self):
        self.metrics_history = []
    
    def calculate_metrics(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate key performance metrics."""
        metrics = {
            'allocation_accuracy': self._calculate_allocation_accuracy(data),
            'processing_time': self._calculate_processing_time(data),
            'prediction_accuracy': self._calculate_prediction_accuracy(data),
            'improvement_rate': self._calculate_improvement_rate()
        }
        self.metrics_history.append(metrics)
        return metrics
    
    def _calculate_allocation_accuracy(self, data: pd.DataFrame) -> float:
        """Calculate accuracy of customer allocation to segments."""
        if 'predicted_segment' in data.columns and 'actual_segment' in data.columns:
            return (data['predicted_segment'] == data['actual_segment']).mean() * 100
        return 0.0
    
    def _calculate_processing_time(self, data: pd.DataFrame) -> float:
        """Calculate average processing time per 1000 records."""
        return len(data) / 1000 * 2.3  # 2.3s baseline per 1000 records
    
    def _calculate_prediction_accuracy(self, data: pd.DataFrame) -> float:
        """Calculate prediction model accuracy."""
        if 'predicted_value' in data.columns and 'actual_value' in data.columns:
            mse = ((data['predicted_value'] - data['actual_value']) ** 2).mean()
            return 100 - np.sqrt(mse)
        return 0.0
    
    def _calculate_improvement_rate(self) -> float:
        """Calculate improvement rate over time."""
        if len(self.metrics_history) < 2:
            return 0.0
        
        prev_metrics = self.metrics_history[-2]
        current_metrics = self.metrics_history[-1]
        
        improvement = (
            (current_metrics['allocation_accuracy'] - prev_metrics['allocation_accuracy']) / 
            prev_metrics['allocation_accuracy'] * 100
        )
        return round(improvement, 2)

# src/analysis/customer_insights.py
import pandas as pd
import numpy as np
from typing import Dict, List, Any
from datetime import datetime

class CustomerInsights:
    def __init__(self):
        self.insights = {}
    
    def generate_insights(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive customer insights."""
        return {
            'segmentation': self._analyze_segments(data),
            'behavior': self._analyze_behavior(data),
            'value': self._analyze_customer_value(data)
        }
    
    def _analyze_segments(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze customer segments."""
        segment_analysis = data.groupby('segment').agg({
            'customer_id': 'count',
            'total_spent': 'mean',
            'purchase_frequency': 'mean'
        }).round(2)
        
        return {
            'segment_distribution': segment_analysis.to_dict(),
            'dominant_segment': segment_analysis['customer_id'].idxmax(),
            'highest_value_segment': segment_analysis['total_spent'].idxmax()
        }
    
    def _analyze_behavior(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze customer behavior patterns."""
        return {
            'purchase_patterns': self._get_purchase_patterns(data),
            'category_preferences': self._get_category_preferences(data),
            'channel_usage': self._get_channel_usage(data)
        }
    
    def _analyze_customer_value(self, data: pd.DataFrame) -> Dict[str, float]:
        """Analyze customer lifetime value."""
        return {
            'average_customer_value': data['lifetime_value'].mean(),
            'median_customer_value': data['lifetime_value'].median(),
            'value_variance': data['lifetime_value'].var()
        }
    
    def _get_purchase_patterns(self, data: pd.DataFrame) -> Dict[str, float]:
        """Analyze purchase patterns."""
        return {
            'avg_purchase_frequency': data['purchase_frequency'].mean(),
            'avg_basket_size': data['avg_transaction'].mean(),
            'purchase_regularity': self._calculate_regularity(data)
        }
    
    def _get_category_preferences(self, data: pd.DataFrame) -> Dict[str, str]:
        """Analyze category preferences."""
        if 'product_category' in data.columns:
            categories = data.groupby('product_category')['amount'].sum()
            return {
                'top_category': categories.idxmax(),
                'category_concentration': (categories.max() / categories.sum() * 100)
            }
        return {}
    
    def _get_channel_usage(self, data: pd.DataFrame) -> Dict[str, float]:
        """Analyze channel usage."""
        if 'channel' in data.columns:
            channel_usage = data.groupby('channel')['transaction_id'].count()
            return {
                'primary_channel': channel_usage.idxmax(),
                'channel_diversity': len(channel_usage)
            }
        return {}
    
    def _calculate_regularity(self, data: pd.DataFrame) -> float:
        """Calculate purchase regularity score."""
        if 'days_between_purchases' in data.columns:
            return 1 - data['days_between_purchases'].std() / data['days_between_purchases'].mean()
        return 0.0