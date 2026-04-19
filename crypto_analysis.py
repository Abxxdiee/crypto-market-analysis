import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Fetch BTC and ETH price data from CoinGecko (free, no API key needed)
def get_crypto_data(coin_id, days=90):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    prices = data["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df[["date", "price"]]
    df["coin"] = coin_id
    return df

# Get data for BTC and ETH
btc = get_crypto_data("bitcoin")
eth = get_crypto_data("ethereum")

# Combine into one dataframe
df = pd.concat([btc, eth], ignore_index=True)

# Save to CSV
df.to_csv("crypto_data.csv", index=False)
print("Data saved to crypto_data.csv")
print(df.head(10))

# Plot price trends
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

btc_data = df[df["coin"] == "bitcoin"]
eth_data = df[df["coin"] == "ethereum"]

axes[0].plot(btc_data["date"], btc_data["price"], color="#F7931A", linewidth=2)
axes[0].set_title("Bitcoin (BTC) — 90 Day Price Trend", fontsize=14)
axes[0].set_ylabel("Price (USD)")
axes[0].grid(True, alpha=0.3)

axes[1].plot(eth_data["date"], eth_data["price"], color="#627EEA", linewidth=2)
axes[1].set_title("Ethereum (ETH) — 90 Day Price Trend", fontsize=14)
axes[1].set_ylabel("Price (USD)")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("crypto_trends.png", dpi=150)
print("Chart saved as crypto_trends.png")
