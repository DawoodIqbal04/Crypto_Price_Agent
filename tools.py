from agents import function_tool
import requests

@function_tool
def get_crypto_price(coin: str = 'bitcoin', currency: str = 'usd') -> str :
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin.lower()}&vs_currencies={currency.lower()}"
    data = requests.get(url).json()
    
    if coin.lower() in data:
        price = data[coin.lower()][currency.lower()]
        return f"{coin.capitalize()}/{currency.upper()} : {price}"
    
    else:
        'No data availale for this coin OR coin doesnot exist'