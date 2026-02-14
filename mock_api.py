import random
from datetime import datetime, timedelta

class MockPolymarketAPI:
    def __init__(self):
        self.markets = {
            "btc": {"condition_id": "0x1234567890abcdef", "question": "Will Bitcoin close above $45,000 today?", "outcomes": ["YES", "NO"], "active": True, "closed": False, "end_date_iso": (datetime.now() + timedelta(hours=8)).isoformat(), "current_price_yes": 0.42, "trend": "up", "volatility": 0.08},
            "eth": {"condition_id": "0xabcdef1234567890", "question": "Will Ethereum close above $2,500 today?", "outcomes": ["YES", "NO"], "active": True, "closed": False, "end_date_iso": (datetime.now() + timedelta(hours=8)).isoformat(), "current_price_yes": 0.38, "trend": "up", "volatility": 0.09},
            "sol": {"condition_id": "0x9876543210fedcba", "question": "Will Solana close above $100 today?", "outcomes": ["YES", "NO"], "active": True, "closed": False, "end_date_iso": (datetime.now() + timedelta(hours=8)).isoformat(), "current_price_yes": 0.45, "trend": "up", "volatility": 0.10}
        }
        self.price_history = {m: [] for m in self.markets.keys()}
    
    def get_markets(self):
        return {"data": [{"condition_id": m["condition_id"], "question": m["question"], "outcomes": m["outcomes"], "active": m["active"], "closed": m["closed"], "end_date_iso": m["end_date_iso"], "tokens": [{"outcome": "YES", "price": m["current_price_yes"]}, {"outcome": "NO", "price": 1.0 - m["current_price_yes"]}]} for m in self.markets.values()]}
    
    def get_market_price(self, condition_id):
        for m in self.markets.values():
            if m["condition_id"] == condition_id:
                return m["current_price_yes"]
        return None
    
    def update_prices(self):
        for market in self.markets.values():
            trend_bias = 0.02 if market["trend"] == "up" else -0.02
            change = random.gauss(trend_bias, market["volatility"])
            new_price = max(0.20, min(0.80, market["current_price_yes"] + change))
            if random.random() < 0.1:
                market["trend"] = "down" if market["trend"] == "up" else "up"
            market["current_price_yes"] = round(new_price, 4)
            self.price_history[list(self.markets.keys())[list(self.markets.values()).index(market)]].append({"timestamp": datetime.now().isoformat(), "price": new_price})
            if len(self.price_history[list(self.markets.keys())[list(self.markets.values()).index(market)]]) > 100:
                self.price_history[list(self.markets.keys())[list(self.markets.values()).index(market)]].pop(0)
    
    def get_market_trend(self, condition_id, lookback=5):
        for key, market in self.markets.items():
            if market["condition_id"] == condition_id:
                history = self.price_history[key]
                if len(history) < lookback:
                    return market["trend"]
                recent = [h["price"] for h in history[-lookback:]]
                if len(recent) >= 2:
                    return "up" if recent[-1] > recent[0] else "down"
                return market["trend"]
        return "neutral"
    
    def execute_trade(self, condition_id, side, size):
        price = self.get_market_price(condition_id)
        if not price:
            return None
        execution_price = max(0.01, min(0.99, price + random.uniform(-0.01, 0.01)))
        return {"condition_id": condition_id, "side": side, "size": size, "price": round(execution_price, 4), "timestamp": datetime.now().isoformat(), "status": "filled"}
