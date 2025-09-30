# config/config.py
"""
Configuration file for the crypto analysis project
"""
import os
from datetime import datetime, timedelta

# API Configuration
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

# Crypto currencies to analyze
CRYPTOCURRENCIES = {
    'bitcoin': 'BTC',
    'ethereum': 'ETH', 
    'cardano': 'ADA',
    'polkadot': 'DOT',
    'solana': 'SOL',
    'chainlink': 'LINK'
}

# Data collection parameters
DEFAULT_VS_CURRENCY = 'usd'
DEFAULT_DAYS = 365  # 1 year of historical data
DEFAULT_INTERVAL = 'daily'  # daily, hourly

# Date ranges
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=DEFAULT_DAYS)

# File paths
DATA_DIR = "data"
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
MODELS_DIR = os.path.join(DATA_DIR, "models")

# Technical Analysis Parameters
TECHNICAL_INDICATORS = {
    'SMA_SHORT': 20,    # Short-term Simple Moving Average
    'SMA_LONG': 50,     # Long-term Simple Moving Average
    'EMA_SHORT': 12,    # Short-term Exponential Moving Average
    'EMA_LONG': 26,     # Long-term Exponential Moving Average
    'RSI_PERIOD': 14,   # RSI calculation period
    'MACD_FAST': 12,    # MACD fast period
    'MACD_SLOW': 26,    # MACD slow period
    'MACD_SIGNAL': 9    # MACD signal period
}

# LSTM Model Parameters
LSTM_CONFIG = {
    'SEQUENCE_LENGTH': 60,    # Number of days to look back
    'PREDICTION_DAYS': 30,    # Number of days to predict forward
    'TRAIN_SPLIT': 0.8,      # 80% for training
    'VALIDATION_SPLIT': 0.1,  # 10% for validation
    'TEST_SPLIT': 0.1,       # 10% for testing
    'BATCH_SIZE': 32,
    'EPOCHS': 100,
    'LEARNING_RATE': 0.001
}

# Visualization settings
PLOT_CONFIG = {
    'TEMPLATE': 'plotly_dark',
    'HEIGHT': 600,
    'WIDTH': 1200,
    'COLORS': {
        'primary': '#1f77b4',
        'secondary': '#ff7f0e',
        'success': '#2ca02c',
        'danger': '#d62728',
        'warning': '#ff7f0e',
        'info': '#17becf'
    }
}

# Create directories if they don't exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR]:
    os.makedirs(directory, exist_ok=True)