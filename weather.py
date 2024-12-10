import requests

class WeatherData:
    """
    Class to handle fetching and storing weather data from OpenWeatherMap.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def fetch_data(self, city, unit='metric'):
        """
        Fetches weather data for a given city and unit.
        """
        params = {
            "q": city,
            "appid": self.api_key,
            "units": unit
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error while fetching data: {e}")
            return None

class WeatherReport:
    """
    Class to process and display weather information.
    """
    def __init__(self, data):
        self.data = data

    def display_report(self, unit):
        """
        Displays the weather report based on the provided data and unit type.
        """
        if not self.data:
            print("No data available to display.")
            return

        if 'main' in self.data and 'weather' in self.data:
            temperature = self.data['main']['temp']
            feels_like = self.data['main']['feels_like']
            weather_description = self.data['weather'][0]['description']
            humidity = self.data['main']['humidity']
            pressure = self.data['main']['pressure']
            wind_speed = self.data['wind']['speed']
            visibility = self.data['visibility'] / 1000  # Convert to kilometers

            unit_symbol = '°C' if unit == 'metric' else '°F' if unit == 'imperial' else 'K'
            feels_unit_symbol = '°C' if unit == 'metric' else '°F' if unit == 'imperial' else 'K'

            print(f"\nWeather in {self.data['name'].capitalize()}:")
            print(f"Temperature: {temperature}{unit_symbol}")
            print(f"Feels like: {feels_like}{feels_unit_symbol}")
            print(f"Condition: {weather_description}")
            print(f"Humidity: {humidity}%")
            print(f"Pressure: {pressure} hPa")
            print(f"Visibility: {visibility:.2f} km")
            print(f"Wind Speed: {wind_speed} m/s")
        else:
            print(f"Error: Unable to retrieve weather data for {self.data.get('name', 'unknown')}.")
    
class WeatherApp:
    """
    Class that manages the weather application logic and user interaction.
    """
    def __init__(self):
        self.api_key = None
        self.weather_data = None

    def get_user_api_key(self):
        """
        Prompts the user to input their API key and stores it.
        """
        self.api_key = input("Enter your OpenWeatherMap API key: ")
        if not self.api_key:
            print("Error: API key cannot be empty.")
            exit()

    def get_city_input(self):
        """
        Prompts the user for a city name and validates the input.
        """
        city = input("Enter the name of the city: ").strip()
        if not city:
            print("Error: City name cannot be empty.")
            exit()
        return city

    def get_unit_choice(self):
        """
        Prompts the user to select a unit for temperature display.
        """
        print("\nChoose a unit type for temperature:")
        print("1. Celsius (Metric)")
        print("2. Fahrenheit (Imperial)")
        print("3. Kelvin (Standard)")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            return 'metric'
        elif choice == '2':
            return 'imperial'
        elif choice == '3':
            return 'standard'
        else:
            print("Invalid choice. Defaulting to Celsius.")
            return 'metric'

    def run(self):
        """
        Runs the main application logic.
        """
        print("Welcome to the Enhanced Weather App!")

        # Step 1: Get the API key from the user
        self.get_user_api_key()

        # Step 2: Get the city name from the user
        city = self.get_city_input()

        # Step 3: Get the temperature unit from the user
        unit = self.get_unit_choice()

        # Step 4: Fetch weather data
        weather_data_instance = WeatherData(self.api_key)
        weather_data = weather_data_instance.fetch_data(city, unit)

        # Step 5: Process and display the weather report
        weather_report_instance = WeatherReport(weather_data)
        weather_report_instance.display_report(unit)

# Run the application
if __name__ == "__main__":
    app = WeatherApp()
    app.run()
