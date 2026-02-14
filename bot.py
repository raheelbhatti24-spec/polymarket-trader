import json
import os
from datetime import datetime
from mock_api import MockPolymarketAPI

class PaperTradingBot:
    def __init__(self):
        self.api = MockPolymarketAPI()
        self.buy_threshold = 0.40
        self.sell_threshold = 0.60
        self.position_size = 10.00
        self.max_consecutive_losses = 3
        self.trades = self.load_json('trades.json', [])
        self.positions = self.load_json('positions.json', {})
        self.consecutive_losses = self.calculate_consecutive_losses()
        self.circuit_breaker_active = self.consecutive_losses >= self.max_consecutive_losses
    
    def load_json(self, filename, default):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return default
    
    def save_json(self, filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def calculate_consecutive_losses(self):
        losses = 0
        for trade in reversed(self.trades):
            if trade.get('status') == 'closed' and trade.get('pnl', 0) < 0:
                losses += 1
            else:
                break
        return losses
    
    def check_circuit_breaker(self):
        self.consecutive_losses = self.calculate_consecutive_losses()
        self.circuit_breaker_active = self.consecutive_losses >= self.max_consecutive_losses
        if self.circuit_breaker_active:
            print(f"⚠️ CIRCUIT BREAKER: {self.consecutive_losses} losses")
            return True
        return False
    
    def run(self):
        print(f"\n{'='*60}\nTrading: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'='*60}")
        self.api.update_prices()
        if self.check_circuit_breaker():
            self.save_json('trades.json', self.trades)
            self.save_json('positions.json', self.positions)
            return
        
        markets = self.api.get_markets()
        for market in markets['data']:
            cid = market['condition_id']
            price = market['tokens'][0]['price']
            
            if price < self.buy_threshold and cid not in self.positions:
                trend = self.api.get_market_trend(cid)
                if trend == "up":
                    trade = self.api.execute_trade(cid, 'BUY', self.position_size)
                    if trade:
                        self.positions[cid] = {'entry_price': trade['price'], 'entry_time': trade['timestamp'], 'question': market['question'], 'shares': self.position_size / trade['price']}
                        self.trades.append({'trade_id': len(self.trades) + 1, 'condition_id': cid, 'question': market['question'], 'action': 'BUY', 'entry_price': trade['price'], 'entry_time': trade['timestamp'], 'status': 'open'})
                        print(f"✅ BUY: {market['question'][:40]} @ ${trade['price']:.4f}")
            
            elif price > self.sell_threshold and cid in self.positions:
                trade = self.api.execute_trade(cid, 'SELL', self.position_size)
                if trade:
                    pos = self.positions[cid]
                    pnl = (trade['price'] - pos['entry_price']) * pos['shares']
                    for t in self.trades:
                        if t['condition_id'] == cid and t['status'] == 'open':
                            t.update({'exit_price': trade['price'], 'exit_time': trade['timestamp'], 'pnl': round(pnl, 2), 'status': 'closed'})
                            break
                    del self.positions[cid]
                    print(f"✅ SELL: {market['question'][:40]} @ ${trade['price']:.4f} | P&L: ${pnl:+.2f}")
        
        self.save_json('trades.json', self.trades)
        self.save_json('positions.json', self.positions)
        
        closed = [t for t in self.trades if t['status'] == 'closed']
        if closed:
            total_pnl = sum(t['pnl'] for t in closed)
            wins = len([t for t in closed if t['pnl'] > 0])
            win_rate = round((wins / len(closed)) * 100, 2)
            print(f"\nStats: {len(closed)} trades | P&L: ${total_pnl:+.2f} | Win: {win_rate}%")

if __name__ == "__main__":
    bot = PaperTradingBot()
    bot.run()
