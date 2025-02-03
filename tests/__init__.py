# tests/__init__.py
# Empty init file to make the directory a Python package

# tests/test_data_processing.py
import pytest
import pandas as pd
import numpy as np
from src.data import DataLoader, DataPreprocessor

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        'customer_id': range(1, 6),
        'total_spent': [1000, 2000, None, 4000, 5000],
        'purchase_frequency': [10, 20, 15, None, 25],
        'avg_transaction': [100, 100, 100, 100, 200],
        'last_purchase_date': ['2023-01-01'] * 5
    })

def test_data_preprocessor_missing_values(sample_data):
    preprocessor = DataPreprocessor()
    processed_data = preprocessor.preprocess_data(sample_data)
    
    assert processed_data['total_spent'].isna().sum() == 0
    assert processed_data['purchase_frequency'].isna().sum() == 0

def test_data_preprocessor_feature_creation(sample_data):
    preprocessor = DataPreprocessor()
    processed_data = preprocessor.preprocess_data(sample_data)
    
    assert 'days_since_last_purchase' in processed_data.columns

# tests/test_models.py
import pytest
import pandas as pd
import numpy as np
from src.models import CustomerSegmentation, PredictionModel, PatternAnalyzer

@pytest.fixture
def sample_customer_data():
    """Create sample customer data for testing."""
    return pd.DataFrame({
        'customer_id': range(1, 101),
        'total_spent': np.random.normal(1000, 200, 100),
        'purchase_frequency': np.random.normal(10, 2, 100),
        'avg_transaction': np.random.normal(100, 20, 100),
        'days_since_last_purchase': np.random.normal(30, 10, 100)
    })

def test_customer_segmentation(sample_customer_data):
    segmentation = CustomerSegmentation(n_clusters=3)
    result = segmentation.fit_predict(sample_customer_data)
    
    assert 'segment' in result.columns
    assert len(result['segment'].unique()) == 3

def test_prediction_model(sample_customer_data):
    # Add target variable for testing
    sample_customer_data['lifetime_value'] = np.random.normal(2000, 400, 100)
    
    model = PredictionModel()
    metrics = model.train(sample_customer_data)
    
    assert 'train_score' in metrics
    assert 'test_score' in metrics
    assert 0 <= metrics['train_score'] <= 1
    assert 0 <= metrics['test_score'] <= 1

# tests/test_analysis.py
import pytest
import pandas as pd
from src.analysis import PerformanceAnalyzer, CustomerInsights

@pytest.fixture
def sample_analysis_data():
    """Create sample data for analysis testing."""
    return pd.DataFrame({
        'customer_id': range(1, 51),
        'segment': ['Segment_1', 'Segment_2'] * 25,
        'total_spent': np.random.normal(1000, 200, 50),
        'purchase_frequency': np.random.normal(10, 2, 50),
        'lifetime_value': np.random.normal(2000, 400, 50),
        'product_category': ['A', 'B', 'C'] * 16 + ['A', 'B']
    })

def test_performance_analyzer(sample_analysis_data):
    analyzer = PerformanceAnalyzer()
    metrics = analyzer.calculate_metrics(sample_analysis_data)
    
    assert isinstance(metrics, dict)
    assert 'allocation_accuracy' in metrics
    assert 'processing_time' in metrics

def test_customer_insights(sample_analysis_data):
    insights = CustomerInsights()
    results = insights.generate_insights(sample_analysis_data)
    
    assert 'segmentation' in results
    assert 'behavior' in results
    assert 'value' in results