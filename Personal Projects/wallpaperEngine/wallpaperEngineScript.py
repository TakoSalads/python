import requests
import keyboard
import time


API_KEY = "cd962cd17b8a10ee739f170cd13cda5b"
LOCATION = "Bells Corners"
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
    "drizzle": "ctrl+alt+end",
    "rain": "ctrl+alt+end",
    "snow": "ctrl+alt+down",
    "clear": "ctrl+alt+insert",
    "clouds": "ctrl+alt+home",
    "clouds-cold": "alt+5"
}


def press_macro(condition):
    if condition in MACROS:
        keys = MACROS[condition]
        print(f"   Triggering macro for condition: {condition} --> {keys}")
        keyboard.press_and_release(keys)
    else:
        print(f"   Warning: No macro found for condition: {condition}")
        print(f"   Skipping this weather condition.")



#main
if __name__ == "__main__":
    last_condition = None

    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        weather, temp = get_weather()

        if weather:
            print(f"        | The time is {current_time} |")
            print(f" | Fetched Weather: {weather}, Temperature: {temp:.2f}°C |")
            
            if temp < 0:
                condition = "snow"
                print(f"         Triggering 'snowy' macro.")
            elif weather == "clouds" and temp < 5:
                condition = "clouds-cold"
                print(f"         Triggering 'clouds-cold' macro.")
            else:
                condition = weather

            if condition != last_condition:
                if condition in MACROS:
                    press_macro(condition)
                else:
                    print(f"No macro found for condition: {condition}")
                last_condition = condition
        else:
            print(f"     | Failed to fetch weather, retrying in an hour! |")  

        
        # Timer with countdown
        print(f"     | Update Successful - Updating Hourly |")   
        for i in range(60):  # 60 minutes
            print(f"          {60 - i} minutes remaining...")
            time.sleep(60)




