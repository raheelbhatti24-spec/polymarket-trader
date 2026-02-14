import time
from bot import PaperTradingBot
import os

if os.path.exists('trades.json'):
    os.remove('trades.json')
if os.path.exists('positions.json'):
    os.remove('positions.json')

print("="*60)
print("🚀 SIMULATION STARTING")
print("="*60)

bot = PaperTradingBot()
for i in range(20):
    print(f"\n--- Cycle {i+1}/20 ---")
    bot.run()
    if bot.circuit_breaker_active:
        print("\n⚠️ Circuit breaker activated - stopping")
        break
    time.sleep(0.3)

print("\n" + "="*60)
print("✅ SIMULATION COMPLETE")
print("="*60)

os.system('python dashboard.py')
print("\nOpen dashboard.html in browser to view results!")
