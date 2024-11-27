import requests
import pyautogui
import time


API_KEY = "cd962cd17b8a10ee739f170cd13cda5b"
LOCATION = "Ottawa"
WEATHER_URL = f"http://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={API_KEY}"


def get_weather():
    try:    
        response = requests.get(WEATHER_URL)
        response.raise_for_status()
        data = response.json()

        currentWeather = data["weather"][0]["main"].lower()
        temperature = data["main"]["temp"] - 273.15
        return currentWeather, temperature

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None, None 

MACROS = {
    "rain": ["ctrl", "alt", "end"],
    "snow": ["ctrl", "alt", "down"],
    "default": ["ctrl", "alt", "insert"],
    "clouds": ["ctrl", "alt", "home"]
}

def trigger_macro(temperature, condition):
    if temperature is None or condition is None:
        print("Skipping Macro due to missing weather data")

    if temperature < 0:
        print(f"Temperature is below 0°C: {temperature}°C. Triggering 'snowy' macro.")
        pyautogui.hotkey("ctrl", "alt", "down")  # Snowy macro
    else:
        # Use weather condition to determine the macro
        keys = MACROS.get(condition, MACROS["default"])
        print(f"Weather: {condition}, Temperature: {temperature}°C. Triggering macro.")
        pyautogui.hotkey(*keys)

#main
if __name__ == "__main__":
    while True:
        weather, temp = get_weather()
        if weather and temp is not None:
            print(f"Fetched Weather: {weather}, Temperature: {temp:.2f}°C")
            trigger_macro(temp, weather)
        else:
            print("Failed to fetch weather, retrying in an hour")
            
        print("Waiting for one hour")
        time.sleep(3600)




