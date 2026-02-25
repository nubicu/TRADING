"""
fetch live weather data with requests, or make a colorful terminal menu with colorama. Read the docs and figure it out.
"""

try:
    import requests
except ImportError:
    import sys
    print("Missing dependency: 'requests'. Install it in your environment:\n    python -m pip install requests")
    sys.exit(1)

def main():
    city = "London, GB" # input("Enter a city name: ")
    api_key = "5e82f7194cda9d0127e199fbf419927d"  # You need to get an API key from a weather service like OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"Weather in {city}: {data['weather'][0]['description']}")
        print(f"Temperature: {data['main']['temp']}°C")
    else:
        print(f"Could not fetch weather data for {city}. Please check the city name and try again.")

if __name__ == "__main__":
    main()