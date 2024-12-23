import requests
import schedule
import time

# API configuration (for NewsAPI, you can register and get your API key from https://newsapi.org/)
API_KEY = 'b9257503552a4089a862ff6470f9e7e6'
HEADLINES_URL = 'https://newsapi.org/v2/top-headlines'
country = 'de'  # 'de' is the country code for Germany

# Array to store the headlines
headlines_array = []

def fetch_headlines():
    """Fetch top news headlines in German and save them to the array."""
    global headlines_array
    try:
        # Fetch top headlines from NewsAPI
        params = {
            'apiKey': API_KEY,
            'country': country,
            'language': 'de'
        }
        response = requests.get(HEADLINES_URL, params=params)
        news_data = response.json()
        
        if news_data['status'] == 'ok':
            headlines = [article['title'] for article in news_data['articles']]
            headlines_array.extend(headlines)
            print(f"Fetched {len(headlines)} headlines")
        else:
            print("Failed to fetch headlines", news_data)

    except Exception as e:
        print(f"Error fetching headlines: {e}")

# Schedule the job every hour
schedule.every(1).hours.do(fetch_headlines)

# Run the scheduler in a loop
if __name__ == '__main__':
    fetch_headlines()  # Initial run to fetch immediately
    while True:
        schedule.run_pending()
        time.sleep(1)
