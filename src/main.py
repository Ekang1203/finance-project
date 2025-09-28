import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Télécharger des données financières
ticker = "AAPL"
data = yf.download(ticker, start="2023-01-01", end="2024-01-01")

# Afficher les premières lignes
print(data.head())

# Créer un graphique simple
plt.figure(figsize=(10, 6))
plt.plot(data.index, data['Close'])
plt.title(f'{ticker} Stock Price')
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.show()
