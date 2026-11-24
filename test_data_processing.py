"""
Unit Tests for Data Processing and Preprocessing Pipeline
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_processing.preprocessor import TimeSeriesPreprocessor

def test_feature_engineering_lags():
    # Create synthetic series
    dates = pd.date_range("2023-01-01", periods=30, freq="D")
    df = pd.DataFrame({"daily_sales": np.arange(100.0, 130.0)}, index=dates)
    
    preprocessor = TimeSeriesPreprocessor(lookback_window=7)
    df_feat = preprocessor.generate_features(df)
    
    # Assert lags exist
    assert "lag_1" in df_feat.columns
    assert "lag_7" in df_feat.columns
    assert "rolling_mean_7" in df_feat.columns
    assert "sin_dow" in df_feat.columns
    
    # Assert no nulls after dropna
    assert df_feat.isnull().sum().sum() == 0

def test_chronological_split_ordering():
    dates = pd.date_range("2023-01-01", periods=100, freq="D")
    df = pd.DataFrame({"daily_sales": np.arange(100)}, index=dates)
    
    preprocessor = TimeSeriesPreprocessor()
    train, val, test = preprocessor.chronological_split(df, 0.70, 0.15)
    
    # Check lengths
    assert len(train) == 70
    assert len(val) == 15
    assert len(test) == 15
    
    # Verify strict temporal non-overlap
    assert train.index.max() < val.index.min()
    assert val.index.max() < test.index.min()

def test_sliding_window_dimensions():
    # 50 samples, 5 features
    X_dummy = np.random.randn(50, 5)
    y_dummy = np.random.randn(50, 1)
    
    preprocessor = TimeSeriesPreprocessor(lookback_window=10)
    X_seq, y_seq = preprocessor.create_sliding_windows(X_dummy, y_dummy)
    
    # Output samples should be 50 - 10 = 40
    assert X_seq.shape == (40, 10, 5)
    assert y_seq.shape == (40, 1)
