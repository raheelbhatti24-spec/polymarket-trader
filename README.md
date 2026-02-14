# Polymarket Paper Trading Bot

Automated mean reversion trading bot for Polymarket prediction markets.

## Quick Start
```bash
python simulate.py
```

Open `dashboard.html` in browser to view results.

## Deploy

### GitHub Actions (Runs every 15 min)
1. Upload all files to GitHub
2. Enable GitHub Actions
3. Set permissions to "Read and write"

### Vercel (Dashboard hosting)
1. Connect repository to Vercel
2. Deploy
3. Dashboard at: `https://your-project.vercel.app/dashboard.html`

## Strategy

- **Buy**: YES price < $0.40 in uptrend
- **Sell**: YES price > $0.60  
- **Risk**: $10 per trade
- **Safety**: Circuit breaker after 3 losses

## Files

- `bot.py` - Main trading logic
- `mock_api.py` - Simulated market data
- `dashboard.py` - Generates HTML dashboard
- `simulate.py` - Run 20 trading cycles
- `trade.yml` - GitHub Actions automation
