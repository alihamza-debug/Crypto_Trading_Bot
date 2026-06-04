"""
SMA (Simple Moving Average) Trading Strategy
"""

import numpy as np
import logging
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)


class SMAStrategy:
    """
    Simple Moving Average (SMA) Crossover Strategy
    
    Buy Signal: Short-term SMA crosses above long-term SMA
    Sell Signal: Short-term SMA crosses below long-term SMA
    """
    
    def __init__(self, short_period: int = 12, long_period: int = 26):
        """
        Initialize SMA Strategy
        
        Args:
            short_period: Period for short-term SMA
            long_period: Period for long-term SMA
        """
        self.short_period = short_period
        self.long_period = long_period
        self.previous_crossover = None
        
        if short_period >= long_period:
            raise ValueError("Short period must be less than long period")
        
        logger.info(f"SMA Strategy initialized: short={short_period}, long={long_period}")
    
    def calculate_sma(self, prices: List[float], period: int) -> List[float]:
        """
        Calculate Simple Moving Average
        
        Args:
            prices: List of prices
            period: SMA period
        
        Returns:
            List of SMA values
        """
        if len(prices) < period:
            return []
        
        return np.convolve(prices, np.ones(period) / period, mode='valid').tolist()
    
    def analyze(self, klines: List) -> Tuple[Optional[str], float, float]:
        """
        Analyze klines and generate trading signal
        
        Args:
            klines: List of kline data from Binance
        
        Returns:
            Tuple of (signal, short_sma, long_sma)
            signal: 'BUY', 'SELL', or None
        """
        try:
            # Extract closing prices
            closing_prices = [float(kline[4]) for kline in klines]
            
            if len(closing_prices) < self.long_period:
                logger.warning(f"Not enough data. Need {self.long_period}, got {len(closing_prices)}")
                return None, 0, 0
            
            # Calculate SMAs
            short_sma = self.calculate_sma(closing_prices, self.short_period)
            long_sma = self.calculate_sma(closing_prices, self.long_period)
            
            if not short_sma or not long_sma:
                return None, 0, 0
            
            # Get the most recent values
            current_short = short_sma[-1]
            current_long = long_sma[-1]
            
            # Check for crossover
            if len(short_sma) > 1 and len(long_sma) > 1:
                prev_short = short_sma[-2]
                prev_long = long_sma[-2]
                
                # Buy signal: short SMA crosses above long SMA
                if prev_short <= prev_long and current_short > current_long:
                    logger.info(f"BUY signal generated: SMA{self.short_period}({current_short:.2f}) > SMA{self.long_period}({current_long:.2f})")
                    return 'BUY', current_short, current_long
                
                # Sell signal: short SMA crosses below long SMA
                elif prev_short >= prev_long and current_short < current_long:
                    logger.info(f"SELL signal generated: SMA{self.short_period}({current_short:.2f}) < SMA{self.long_period}({current_long:.2f})")
                    return 'SELL', current_short, current_long
            
            return None, current_short, current_long
        
        except Exception as e:
            logger.error(f"Error in strategy analysis: {e}")
            return None, 0, 0
