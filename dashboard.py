import json
import os
from datetime import datetime

def load_json(filename, default):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return default

trades = load_json('trades.json', [])
positions = load_json('positions.json', {})
closed = [t for t in trades if t['status'] == 'closed']
total_pnl = sum(t.get('pnl', 0) for t in closed)
wins = len([t for t in closed if t.get('pnl', 0) > 0])
win_rate = round((wins / len(closed)) * 100, 2) if closed else 0
recent = sorted(closed, key=lambda x: x.get('exit_time', ''), reverse=True)[:10]

html = f"""<!DOCTYPE html>
<html><head><title>Polymarket Dashboard</title>
<style>body{{font-family:Arial;background:linear-gradient(135deg,#667eea,#764ba2);padding:20px;color:white;margin:0}}
.container{{max-width:1200px;margin:0 auto}}
.card{{background:white;color:#333;border-radius:12px;padding:25px;margin:20px 0;box-shadow:0 4px 6px rgba(0,0,0,0.1)}}
.stat{{font-size:3em;font-weight:bold;margin:10px 0}}
.positive{{color:#10b981}}.negative{{color:#ef4444}}
table{{width:100%;border-collapse:collapse;margin-top:20px}}
th,td{{padding:12px;text-align:left;border-bottom:1px solid #e0e0e0}}
th{{background:#f5f5f5;font-weight:600}}
.badge{{padding:5px 12px;border-radius:20px;font-size:0.9em;font-weight:600}}
.badge.win{{background:#d1fae5;color:#065f46}}.badge.loss{{background:#fee2e2;color:#991b1b}}
h1{{text-align:center;font-size:2.5em;margin-bottom:10px}}
h2{{margin-top:0}}</style></head>
<body>
<div class="container">
<h1>📊 Polymarket Paper Trading</h1>
<p style="text-align:center;opacity:0.9">Mean Reversion Strategy Dashboard</p>
<div class="card">
<h2>Total P&L</h2>
<div class="stat {'positive' if total_pnl>=0 else 'negative'}">${total_pnl:+.2f}</div>
</div>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px">
<div class="card"><h3>Total Trades</h3><div class="stat">{len(closed)}</div></div>
<div class="card"><h3>Win Rate</h3><div class="stat">{win_rate}%</div></div>
<div class="card"><h3>Open Positions</h3><div class="stat">{len(positions)}</div></div>
</div>
<div class="card">
<h2>Recent Trades</h2>
<table>
<thead><tr><th>ID</th><th>Market</th><th>Entry</th><th>Exit</th><th>P&L</th></tr></thead>
<tbody>
{''.join([f'<tr><td>#{t["trade_id"]}</td><td>{t["question"][:45]}</td><td>${t["entry_price"]:.4f}</td><td>${t.get("exit_price",0):.4f}</td><td><span class="badge {'win' if t.get("pnl",0)>=0 else 'loss'}">${t.get("pnl",0):+.2f}</span></td></tr>' for t in recent]) if recent else '<tr><td colspan="5" style="text-align:center;color:#999">No trades yet</td></tr>'}
</tbody>
</table>
</div>
<p style="text-align:center;opacity:0.8;margin-top:30px">Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</div>
</body></html>"""

with open('dashboard.html', 'w') as f:
    f.write(html)

print("✅ Dashboard generated: dashboard.html")
