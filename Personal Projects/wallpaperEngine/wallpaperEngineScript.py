import requests
import keyboard
import time


API_KEY = "cd962cd17b8a10ee739f170cd13cda5b"
LOCATION = "Ottawa"
WEATHER_URL = f"http://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={API_KEY}"
GREEN = '\033[32m'
RED = '\033[31m'
LTBLUE = '\033[94m'
RESET= '\033[0m'
current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

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
    "drizzle": "ctrl+alt+end",
    "rain": "ctrl+alt+end",
    "snow": "ctrl+alt+down",
    "clear": "ctrl+alt+insert",
    "clouds": "ctrl+alt+home",
    "clouds-cold": "alt+5"
}

def trigger_macro(temperature, condition):
    if temperature is None or condition is None:
        print("Skipping Macro due to missing weather data")
        return

    if temperature < 0 and condition != "clouds":
        print(f"           Triggering 'snowy' macro.")
        keyboard.press_and_release("ctrl+alt+down")  # Snowy macro
        return
    elif temperature < 5 and condition == "clouds":
        print(f"           Triggering 'cloudy-cold' macro.")
        keyboard.press_and_release("alt+5")  # Cloudy-cold macro
        return
    elif temperature > 5 and condition == "clouds":
        print(f"           Triggering 'cloudy' macro.")
        keyboard.press_and_release("ctrl+alt+home")  # Cloudy macro
        return
    else:
        # Use weather condition to determine the macro
        keys = MACROS.get(condition, "ctrl+alt+insert")
        print(f"Weather: {condition}, Temperature: {temperature}°C. Triggering macro.")
        keyboard.press_and_release(*keys)


#main
if __name__ == "__main__":
    while True:
        weather, temp = get_weather()
        if weather and temp is not None:
            print(f"            | The time is {current_time} |       ")
            print(f"{GREEN}| Fetched Weather: {weather}, Temperature: {temp:.2f}°C |   {RESET}")
            trigger_macro(temp, weather)
        else:
            print(f"{RED}      | Failed to fetch weather, retrying in an hour! |    {RESET}")
            
        print(f"{LTBLUE}           | Update Successful - Updating Hourly |      {RESET}")   
        time.sleep(3600)




