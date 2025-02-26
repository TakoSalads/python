import tkinter as tk
from datetime import datetime
import requests
import keyboard


#---------------#
#constants

API_KEY = "cd962cd17b8a10ee739f170cd13cda5b"
LOCATION = "Bells Corners"
WEATHER_URL = f"http://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={API_KEY}"

def get_weather():
    try:
        response = requests.get(WEATHER_URL)
        response.raise_for_status()
        data = response.json()

        weather = data["weather"][0]["main"].lower()
        temperature = data["main"]["temp"] - 273.15 #kelvin conversion
        return weather, temperature
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None, None


#----------------#


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather App Example")
        window_width = 400
        window_height = 450

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        taskbar_height = 70  # Adjust if needed

        # Position window in the bottom left
        x = 0  # Left side
        y = screen_height - window_height - taskbar_height  # Above taskbar
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Keep window always on top
        self.attributes('-topmost', True)
        
        # Initialize variables
        self.weather = "Unknown"
        self.temperature = 0.0

        # Create labels
        self.weather_label = tk.Label(self, text="Weather: Loading...", font=("Helvetica", 14))
        self.weather_label.pack(pady=10)

        self.temp_label = tk.Label(self, text="Temperature: --°C", font=("Helvetica", 14))
        self.temp_label.pack(pady=10)

        self.time_label = tk.Label(self, text="", font=("Helvetica", 12))
        self.time_label.pack(pady=10)

        # Start updating data
        self.update_info()

    def update_info(self):
        weather, temp = get_weather()
        current_time = datetime.now().strftime("%H:%M:%S")

        if weather and temp is not None:
            self.weather = weather
            self.temperature = temp
        else:
            self.weather = "Fetch Error"
            self.temperature = 0.0

        self.weather_label.config(text=f"Weather: {self.weather}")
        self.temp_label.config(text=f"Temperature: {self.temperature:.2f}°C") 
        self.time_label.config(text=f"Time: {current_time}")

        self.after(1800000, self.update_info)      

# Run the application
if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
