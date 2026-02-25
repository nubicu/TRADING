"""
fetch live weather data with requests, or make a colorful terminal menu with colorama. Read the docs and figure it out.
"""

try:
    import requests
except ImportError:
    import sys
    print("Missing dependency: 'requests'. Install it in your environment:\n    python -m pip install requests")
    sys.exit(1)

""" make a colorful terminal menu with colorama. """
try:
    from colorama import init, Fore, Style
    init(autoreset=True) # Initialize colorama
except ImportError:
    import sys
    print("Missing dependency: 'colorama'. Install it in your environment:\n    python -m pip install colorama")
    sys.exit(1)

def fetch_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException:
        return None, "Network error"
    if response.status_code == 200:
        try:
            return response.json(), None
        except ValueError:
            return None, "Invalid JSON response"
    elif response.status_code == 401:
        return None, "Invalid API key"
    elif response.status_code == 404:
        return None, "City not found"
    else:
        return None, f"HTTP {response.status_code}"

def print_weather(data, city):
    weather = data.get('weather', [{}])[0].get('description', 'N/A').capitalize()
    temp = data.get('main', {}).get('temp', 'N/A')
    feels = data.get('main', {}).get('feels_like', 'N/A')
    humidity = data.get('main', {}).get('humidity', 'N/A')
    wind = data.get('wind', {}).get('speed', 'N/A')

    print(Fore.CYAN + Style.BRIGHT + f"\nWeather for {city}")
    print(Fore.YELLOW + f"  Condition: {weather}")
    print(Fore.RED + f"  Temperature: {temp}°C (feels like {feels}°C)")
    print(Fore.MAGENTA + f"  Humidity: {humidity}%")
    print(Fore.GREEN + f"  Wind speed: {wind} m/s\n")

def menu(api_key):
    sample_cities = ["Iasi, RO", "London, UK", "New York, US", "Tokyo, JP", "Sydney, AU"]
    while True:
        print(Style.BRIGHT + Fore.BLUE + "\n=== Live Weather Menu ===")
        print(Fore.WHITE + "1) Enter a city name")
        print(Fore.WHITE + "2) Choose from sample cities")
        print(Fore.WHITE + "3) Quit")
        choice = input(Fore.YELLOW + "Select an option [1-3]: ").strip()
        if choice == '1':
            city = input(Fore.YELLOW + "Enter city (e.g. 'Iasi, RO' or 'London,UK'): ").strip()
            if not city:
                print(Fore.RED + "No city entered.")
                continue
            data, err = fetch_weather(city, api_key)
            if err:
                print(Fore.RED + f"Error: {err}")
            else:
                print_weather(data, city)
        elif choice == '2':
            print(Fore.CYAN + "\nSample cities:")
            for i, c in enumerate(sample_cities, 1):
                print(Fore.WHITE + f"  {i}) {c}")
            sel = input(Fore.YELLOW + f"Choose [1-{len(sample_cities)}] or 'b' to go back: ").strip()
            if sel.lower() == 'b':
                continue
            if not sel.isdigit() or not (1 <= int(sel) <= len(sample_cities)):
                print(Fore.RED + "Invalid selection.")
                continue
            city = sample_cities[int(sel)-1]
            data, err = fetch_weather(city, api_key)
            if err:
                print(Fore.RED + f"Error: {err}")
            else:
                print_weather(data, city)
        elif choice == '3':
            print(Fore.GREEN + "Goodbye.")
            break
        else:
            print(Fore.RED + "Invalid option. Try again.")

def main():
    api_key = "5e82f7194cda9d0127e199fbf419927d"  # Replace with your API key
    menu(api_key)

if __name__ == "__main__":
    main()