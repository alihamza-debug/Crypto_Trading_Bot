# Crypto Trading Bot

An automated cryptocurrency trading bot that uses Simple Moving Average (SMA) strategy to execute buy/sell orders on Binance.

## Features

- **SMA Trading Strategy**: Uses Simple Moving Average crossovers to identify buy/sell signals
- **Binance Integration**: Real-time trading on Binance cryptocurrency exchange
- **Automated Trading**: Automatic buy/sell order execution
- **Configurable Parameters**: Easy configuration for trading pairs, SMA periods, and more
- **Logging**: Detailed logging of all trading activities
- **Risk Management**: Built-in safety checks and error handling

## Requirements

- Python 3.8+
- Binance API keys (with trading permissions)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/alihamza-debug/Crypto_Trading_Bot.git
cd Crypto_Trading_Bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root:
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

2. Edit `config.py` to customize trading parameters:
- `TRADING_PAIR`: Trading pair (e.g., 'BTCUSDT')
- `SMA_SHORT`: Short-term SMA period (default: 12)
- `SMA_LONG`: Long-term SMA period (default: 26)
- `QUANTITY`: Amount to trade per order
- `INTERVAL`: Candle interval for analysis

## Usage

Run the trading bot:
```bash
python main.py
```

## Project Structure

```
Crypto_Trading_Bot/
├── main.py                 # Entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── src/
    ├── __init__.py
    ├── bot.py           # Main trading bot logic
    ├── binance_client.py # Binance API wrapper
    ├── strategy.py      # SMA trading strategy
    └── logger.py        # Logging configuration
```

## Trading Strategy

The bot uses a Simple Moving Average (SMA) crossover strategy:

- **Buy Signal**: When short-term SMA crosses above long-term SMA
- **Sell Signal**: When short-term SMA crosses below long-term SMA

## Important Notes

⚠️ **Risk Warning**: 
- This bot trades with real money. Use at your own risk.
- Start with small amounts while testing.
- Never commit your API keys to the repository.
- Always use API keys with restricted permissions.

## Disclaimer

This trading bot is provided for educational purposes. Cryptocurrency trading carries substantial risk. Past performance does not guarantee future results. Always conduct thorough testing and use proper risk management.

## License

MIT
