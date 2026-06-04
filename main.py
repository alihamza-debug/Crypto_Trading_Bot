#!/usr/bin/env python3
"""
Crypto Trading Bot - Main Entry Point

A Python-based automated cryptocurrency trading bot that uses
Simple Moving Average (SMA) strategy to execute trades on Binance.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import configuration and modules
import config
from src.logger import setup_logger
from src.bot import TradingBot

# Setup logging
logger = setup_logger(
    __name__,
    log_file=config.LOG_FILE,
    level=getattr(logging, config.LOG_LEVEL)
)


def main():
    """
    Main function to run the trading bot
    """
    
    logger.info("="*50)
    logger.info("Crypto Trading Bot Started")
    logger.info("="*50)
    
    # Validate API keys
    api_key = config.BINANCE_API_KEY
    api_secret = config.BINANCE_API_SECRET
    
    if not api_key or not api_secret:
        logger.error("API keys not found. Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env file")
        sys.exit(1)
    
    # Log configuration
    logger.info(f"Trading Pair: {config.TRADING_PAIR}")
    logger.info(f"SMA Short Period: {config.SMA_SHORT}")
    logger.info(f"SMA Long Period: {config.SMA_LONG}")
    logger.info(f"Interval: {config.INTERVAL}")
    logger.info(f"Trade Quantity: {config.TRADE_QUANTITY}")
    logger.info(f"Test Mode: {config.TEST_MODE}")
    
    # Initialize bot
    bot = TradingBot(
        api_key=api_key,
        api_secret=api_secret,
        test_mode=config.TEST_MODE
    )
    
    # Run bot
    try:
        # Calculate interval from candle interval
        interval_seconds = 60  # Default to 60 seconds for 15m candles
        if '1h' in config.INTERVAL:
            interval_seconds = 300  # 5 minutes
        elif '4h' in config.INTERVAL:
            interval_seconds = 600  # 10 minutes
        elif '1d' in config.INTERVAL:
            interval_seconds = 3600  # 1 hour
        
        # Start continuous trading
        bot.start(interval=interval_seconds)
    
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
        bot.stop()
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
    
    logger.info("="*50)
    logger.info("Bot Status:")
    logger.info(bot.get_status())
    logger.info("="*50)


if __name__ == '__main__':
    main()
