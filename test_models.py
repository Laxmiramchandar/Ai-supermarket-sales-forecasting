"""
Unit Tests for Deep Learning Model Architectures
"""

import sys
from pathlib import Path
import numpy as np
import pytest
import tensorflow as tf

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.architectures import build_lstm_model, build_gru_model, build_bilstm_model

def test_lstm_model_instantiation_and_shape():
    input_shape = (14, 15)
    model = build_lstm_model(input_shape)
    
    assert model.name == "LSTM_Forecaster"
    # Feedforward test with dummy batch
    dummy_input = np.random.randn(4, 14, 15).astype(np.float32)
    output = model(dummy_input)
    assert output.shape == (4, 1)

def test_gru_model_instantiation_and_shape():
    input_shape = (14, 15)
    model = build_gru_model(input_shape)
    
    assert model.name == "GRU_Forecaster"
    dummy_input = np.random.randn(2, 14, 15).astype(np.float32)
    output = model(dummy_input)
    assert output.shape == (2, 1)

def test_bilstm_model_instantiation():
    input_shape = (14, 15)
    model = build_bilstm_model(input_shape)
    
    assert model.name == "BiLSTM_Forecaster"
    dummy_input = np.random.randn(3, 14, 15).astype(np.float32)
    output = model(dummy_input)
    assert output.shape == (3, 1)
