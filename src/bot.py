"""
Main Trading Bot Logic
"""

import time
import logging
from typing import Optional
from datetime import datetime
from src.binance_client import BinanceAPIClient
from src.strategy import SMAStrategy
import config

logger = logging.getLogger(__name__)


class TradingBot:
    """
    Main trading bot class that orchestrates trading
    """
    
    def __init__(self, api_key: str, api_secret: str, test_mode: bool = True):
        """
        Initialize Trading Bot
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            test_mode: Use testnet (default: True)
        """
        self.binance = BinanceAPIClient(api_key, api_secret, testnet=test_mode)
        self.strategy = SMAStrategy(config.SMA_SHORT, config.SMA_LONG)
        self.test_mode = test_mode
        self.is_running = False
        self.last_signal = None
        self.trade_count = 0
        self.last_trade_time = None
        
        logger.info(f"Trading Bot initialized - Mode: {'TEST' if test_mode else 'REAL'}")
    
    def check_safety(self) -> bool:
        """
        Check safety conditions before trading
        
        Returns:
            True if safe to trade, False otherwise
        """
        if not config.SAFETY_CHECK_ENABLED:
            return True
        
        # Check balance
        usdt_balance = self.binance.get_balance('USDT')
        if usdt_balance is None or usdt_balance < config.MIN_BALANCE_REQUIRED:
            logger.warning(f"Insufficient balance. Required: {config.MIN_BALANCE_REQUIRED} USDT, Available: {usdt_balance}")
            return False
        
        return True
    
    def execute_trade(self, signal: str) -> bool:
        """
        Execute trade based on signal
        
        Args:
            signal: 'BUY' or 'SELL'
        
        Returns:
            True if trade executed successfully
        """
        try:
            if signal == 'BUY':
                logger.info(f"Executing BUY order: {config.TRADING_PAIR} x {config.TRADE_QUANTITY}")
                if not self.test_mode:
                    result = self.binance.create_market_buy_order(
                        config.TRADING_PAIR,
                        config.TRADE_QUANTITY
                    )
                    if result:
                        logger.info(f"Buy order successful: {result.get('orderId')}")
                        self.trade_count += 1
                        self.last_trade_time = datetime.now()
                        return True
                else:
                    logger.info("[TEST MODE] Buy order would be executed")
                    self.trade_count += 1
                    return True
            
            elif signal == 'SELL':
                logger.info(f"Executing SELL order: {config.TRADING_PAIR} x {config.TRADE_QUANTITY}")
                if not self.test_mode:
                    result = self.binance.create_market_sell_order(
                        config.TRADING_PAIR,
                        config.TRADE_QUANTITY
                    )
                    if result:
                        logger.info(f"Sell order successful: {result.get('orderId')}")
                        self.trade_count += 1
                        self.last_trade_time = datetime.now()
                        return True
                else:
                    logger.info("[TEST MODE] Sell order would be executed")
                    self.trade_count += 1
                    return True
            
            return False
        
        except Exception as e:
            logger.error(f"Error executing trade: {e}")
            return False
    
    def process_signal(self, signal: Optional[str]) -> None:
        """
        Process trading signal
        
        Args:
            signal: Trading signal ('BUY', 'SELL', or None)
        """
        if signal is None:
            return
        
        # Only execute if signal is different from last signal
        if signal == self.last_signal:
            logger.debug(f"Signal {signal} already executed. Skipping duplicate.")
            return
        
        # Safety check
        if not self.check_safety():
            logger.warning("Safety check failed. Trade not executed.")
            return
        
        # Execute trade
        if self.execute_trade(signal):
            self.last_signal = signal
    
    def run_once(self) -> None:
        """
        Run one iteration of the trading bot
        """
        try:
            logger.info(f"Analyzing {config.TRADING_PAIR} ({config.INTERVAL})...")
            
            # Fetch klines
            klines = self.binance.get_klines(
                config.TRADING_PAIR,
                config.INTERVAL,
                limit=config.SMA_LONG + 10
            )
            
            if not klines:
                logger.warning("Failed to fetch klines")
                return
            
            # Analyze with strategy
            signal, short_sma, long_sma = self.strategy.analyze(klines)
            logger.info(f"SMA{config.SMA_SHORT}: {short_sma:.2f}, SMA{config.SMA_LONG}: {long_sma:.2f}")
            
            # Process signal
            self.process_signal(signal)
        
        except Exception as e:
            logger.error(f"Error in run_once: {e}")
    
    def start(self, interval: int = 60) -> None:
        """
        Start the trading bot in continuous mode
        
        Args:
            interval: Seconds to wait between iterations
        """
        self.is_running = True
        logger.info(f"Starting trading bot. Interval: {interval}s")
        
        try:
            while self.is_running:
                self.run_once()
                logger.info(f"Next check in {interval} seconds...")
                time.sleep(interval)
        
        except KeyboardInterrupt:
            logger.info("Trading bot stopped by user")
            self.stop()
        
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            self.stop()
    
    def stop(self) -> None:
        """
        Stop the trading bot
        """
        self.is_running = False
        logger.info(f"Bot stopped. Total trades: {self.trade_count}")
    
    def get_status(self) -> dict:
        """
        Get current bot status
        
        Returns:
            Dictionary with bot status information
        """
        return {
            'running': self.is_running,
            'trading_pair': config.TRADING_PAIR,
            'test_mode': self.test_mode,
            'trade_count': self.trade_count,
            'last_signal': self.last_signal,
            'last_trade_time': self.last_trade_time
        }
