"""
Crypto Trading Bot Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Binance API Configuration
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')

# Trading Configuration
TRADING_PAIR = 'BTCUSDT'  # Trading pair
TRADE_QUANTITY = 0.001     # Amount to trade per order
INTERVAL = '15m'           # Candle interval (1m, 5m, 15m, 1h, etc.)

# SMA Strategy Configuration
SMA_SHORT = 12             # Short-term SMA period
SMA_LONG = 26              # Long-term SMA period

# Risk Management
MAX_ORDERS_PER_HOUR = 10   # Maximum orders per hour
TEST_MODE = True           # Set to False for real trading

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/trading_bot.log'

# Safety Settings
SAFETY_CHECK_ENABLED = True
MIN_BALANCE_REQUIRED = 10  # Minimum balance in USDT before trading
