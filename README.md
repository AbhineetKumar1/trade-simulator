# trade-simulator
"A real-time cryptocurrency trade simulator using OKX's L2 order book data. It estimates transaction costs, slippage, market impact, and fees, leveraging models like Almgren-Chriss and regression techniques. Designed for optimal trade execution and real-time performance analysis."
# Crypto Trade Simulator

A real-time cryptocurrency trade simulator that estimates transaction costs, slippage, market impact, and fees using L2 order book data from OKX. The system processes live market data through WebSockets and uses models like Almgren-Chriss for optimal trade execution and regression techniques for slippage and maker/taker role prediction.

## Features

- **Real-time data processing**: Connects to OKX WebSocket API for live L2 order book data.
- **Transaction cost estimation**: Includes slippage, fees, and market impact.
- **Market impact models**: Uses Almgren-Chriss model for optimal execution.
- **Regression models**: Estimates slippage and predicts maker/taker roles.
- **User-friendly interface**: Built with Streamlit for easy interaction and performance tracking.
- Connects to OKX via WebSocket for live orderbook data.
- Estimates slippage, fees, market impact using financial models.
- Visual charts for slippage, latency, and net cost.
- Reconnection and network status indicator.


### Prerequisites

- Python 3.7+
- WebSocket access (requires VPN for OKX)

### Dependencies

1. Clone this repository:
   ```bash
   git clone https://github.com/AbhineetKumar1/crypto-trade-simulator.git
   cd crypto-trade-simulator

## Run Instructions
```bash
pip install -r requirements.txt
python src/main.py
```
