
"""
Data collection module for cryptocurrency data from CoinGecko API
"""
import requests
import pandas as pd
import numpy as np 
import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sys
sys.path.append('..')
from config.config import *

class CryptoDataCollector:
    """
    Collector for cryptocurrency data from CoinGecko API
    """
    
    def __init__(self):
        self.base_url = COINGECKO_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_historical_data(self, crypto_id: str, vs_currency: str = 'usd', 
                          days: int = 365) -> pd.DataFrame:
        """
        Récupère les données historiques pour une crypto-monnaie
        
        Args:
            crypto_id: ID de la crypto (ex: 'bitcoin')
            vs_currency: Devise de référence (ex: 'usd')
            days: Nombre de jours d'historique
            
        Returns:
            DataFrame avec les données historiques
        """
        url = f"{self.base_url}/coins/{crypto_id}/market_chart"
        params = {
            'vs_currency': vs_currency,
            'days': days,
            'interval': 'daily'
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Convertir en DataFrame
            df = pd.DataFrame({
                'timestamp': [item[0] for item in data['prices']],
                'price': [item[1] for item in data['prices']],
                'market_cap': [item[1] for item in data['market_caps']],
                'volume': [item[1] for item in data['total_volumes']]
            })
            
            # Convertir timestamp en datetime
            df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
            df = df.drop('timestamp', axis=1)
            df = df.set_index('date')
            
            # Ajouter des colonnes calculées
            df['returns'] = df['price'].pct_change()
            df['log_returns'] = np.log(df['price'] / df['price'].shift(1))
            
            print(f"✅ Données récupérées pour {crypto_id}: {len(df)} jours")
            return df
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur lors de la récupération de {crypto_id}: {e}")
            return pd.DataFrame()
    
    def get_multiple_cryptos(self, crypto_dict: Dict[str, str], 
                           days: int = 365) -> Dict[str, pd.DataFrame]:
        """
        Récupère les données pour plusieurs crypto-monnaies
        
        Args:
            crypto_dict: Dictionnaire {crypto_id: symbol}
            days: Nombre de jours d'historique
            
        Returns:
            Dictionnaire {symbol: DataFrame}
        """
        results = {}
        
        for crypto_id, symbol in crypto_dict.items():
            print(f"📊 Récupération des données pour {symbol} ({crypto_id})...")
            df = self.get_historical_data(crypto_id, days=days)
            
            if not df.empty:
                df['symbol'] = symbol
                results[symbol] = df
            
            # Pause pour éviter le rate limiting
            time.sleep(1)
        
        return results
    
    def save_data(self, data_dict: Dict[str, pd.DataFrame], 
                  filename_prefix: str = "crypto_data") -> None:
        """
        Sauvegarde les données collectées
        
        Args:
            data_dict: Dictionnaire des DataFrames
            filename_prefix: Préfixe pour les noms de fichiers
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for symbol, df in data_dict.items():
            filename = f"{filename_prefix}_{symbol}_{timestamp}.csv"
            filepath = os.path.join(RAW_DATA_DIR, filename)
            df.to_csv(filepath)
            print(f"💾 Données sauvegardées: {filepath}")
        
        # Sauvegarder un fichier combiné
        combined_df = pd.concat(data_dict.values(), keys=data_dict.keys())
        combined_filename = f"{filename_prefix}_combined_{timestamp}.csv"
        combined_filepath = os.path.join(RAW_DATA_DIR, combined_filename)
        combined_df.to_csv(combined_filepath)
        print(f"💾 Données combinées sauvegardées: {combined_filepath}")
    
    def get_current_prices(self, crypto_ids: List[str]) -> pd.DataFrame:
        """
        Récupère les prix actuels
        
        Args:
            crypto_ids: Liste des IDs de crypto-monnaies
            
        Returns:
            DataFrame avec les prix actuels
        """
        ids_string = ','.join(crypto_ids)
        url = f"{self.base_url}/simple/price"
        params = {
            'ids': ids_string,
            'vs_currencies': 'usd',
            'include_market_cap': 'true',
            'include_24hr_vol': 'true',
            'include_24hr_change': 'true'
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            df = pd.DataFrame.from_dict(data, orient='index')
            df.index.name = 'crypto_id'
            df.reset_index(inplace=True)
            
            return df
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur lors de la récupération des prix actuels: {e}")
            return pd.DataFrame()

def main():
    """
    Fonction principale pour tester la collecte de données
    """
    collector = CryptoDataCollector()
    
    print("🚀 Début de la collecte de données crypto...")
    print(f"📅 Période: {DEFAULT_DAYS} derniers jours")
    print(f"💰 Crypto-monnaies: {list(CRYPTOCURRENCIES.values())}")
    
    # Récupérer les données historiques
    data = collector.get_multiple_cryptos(CRYPTOCURRENCIES, days=DEFAULT_DAYS)
    
    if data:
        print(f"\n📊 Données collectées pour {len(data)} crypto-monnaies")
        
        # Afficher un aperçu
        for symbol, df in data.items():
            print(f"\n{symbol}:")
            print(f"  📈 Prix actuel: ${df['price'].iloc[-1]:.2f}")
            print(f"  📊 Variation 30j: {((df['price'].iloc[-1] / df['price'].iloc[-30]) - 1) * 100:.2f}%")
            print(f"  📉 Volatilité (std): {df['returns'].std():.4f}")
        
        # Sauvegarder les données
        collector.save_data(data)
        
        print("\n✅ Collecte de données terminée avec succès!")
    else:
        print("❌ Aucune donnée collectée")

if __name__ == "__main__":
    import numpy as np
    main()