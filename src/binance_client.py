"""
Binance API Client Wrapper
"""

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class BinanceAPIClient:
    """
    Wrapper class for Binance API interactions
    """
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """
        Initialize Binance API client
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Use testnet for testing (default: True)
        """
        self.testnet = testnet
        
        if testnet:
            self.client = Client(api_key, api_secret, testnet=True)
            logger.info("Initialized Binance client in TESTNET mode")
        else:
            self.client = Client(api_key, api_secret)
            logger.warning("Initialized Binance client in REAL TRADING mode")
    
    def get_klines(self, symbol: str, interval: str, limit: int = 100) -> List:
        """
        Get historical klines (candles) data
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            interval: Kline interval (e.g., '15m')
            limit: Number of klines to fetch
        
        Returns:
            List of klines data
        """
        try:
            klines = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
            logger.debug(f"Fetched {len(klines)} klines for {symbol}")
            return klines
        except BinanceAPIException as e:
            logger.error(f"Error fetching klines: {e}")
            return []
    
    def get_balance(self, asset: str = 'USDT') -> Optional[float]:
        """
        Get account balance for a specific asset
        
        Args:
            asset: Asset symbol (e.g., 'USDT', 'BTC')
        
        Returns:
            Balance amount or None if error
        """
        try:
            account = self.client.get_account()
            for balance in account['balances']:
                if balance['asset'] == asset:
                    return float(balance['free'])
            logger.warning(f"Asset {asset} not found in account")
            return None
        except BinanceAPIException as e:
            logger.error(f"Error fetching balance: {e}")
            return None
    
    def create_market_buy_order(self, symbol: str, quantity: float) -> Optional[Dict]:
        """
        Create a market buy order
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            quantity: Quantity to buy
        
        Returns:
            Order result or None if error
        """
        try:
            order = self.client.order_market_buy(symbol=symbol, quantity=quantity)
            logger.info(f"Buy order placed: {symbol} quantity: {quantity}")
            return order
        except BinanceOrderException as e:
            logger.error(f"Order error: {e}")
            return None
        except BinanceAPIException as e:
            logger.error(f"API error: {e}")
            return None
    
    def create_market_sell_order(self, symbol: str, quantity: float) -> Optional[Dict]:
        """
        Create a market sell order
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            quantity: Quantity to sell
        
        Returns:
            Order result or None if error
        """
        try:
            order = self.client.order_market_sell(symbol=symbol, quantity=quantity)
            logger.info(f"Sell order placed: {symbol} quantity: {quantity}")
            return order
        except BinanceOrderException as e:
            logger.error(f"Order error: {e}")
            return None
        except BinanceAPIException as e:
            logger.error(f"API error: {e}")
            return None
    
    def get_symbol_info(self, symbol: str) -> Optional[Dict]:
        """
        Get symbol information
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
        
        Returns:
            Symbol info or None if error
        """
        try:
            exchange_info = self.client.get_symbol_info(symbol)
            return exchange_info
        except BinanceAPIException as e:
            logger.error(f"Error fetching symbol info: {e}")
            return None
