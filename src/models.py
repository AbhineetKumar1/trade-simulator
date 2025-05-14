def estimate_slippage(asks, bids, qty_usd):
    if not asks or not bids:
        return 0.0
    best_ask = float(asks[0][0])
    best_bid = float(bids[0][0])
    mid_price = (best_ask + best_bid) / 2
    slippage = (best_ask - best_bid) / mid_price * qty_usd / 1000
    return slippage

def estimate_fees(qty_usd, fee_rate=0.001):
    return qty_usd * fee_rate

def estimate_market_impact(qty_usd, alpha=0.0005):
    return alpha * qty_usd ** 0.5
