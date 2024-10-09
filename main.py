import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import requests
import os
import geocoder

# API details
api_key = '5597e9850c26a219a20422af2315097d'
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Define the path to your weather images
image_path = "weather_images"

# Function to update the background based on weather
def update_background(condition):
    global bg_image_tk  # Declare it global to modify the label later

    # Map conditions to corresponding image filenames
    condition_map = {
        "Clear": "sunny.jpg",
        "Clouds": "cloudy.jpg",
        "Rain": "rainy.jpg",
        "Drizzle": "drizzle.jpg",
        "Thunderstorm": "stormy.jpg",
        "Snow": "snow.jpg",
        "Mist": "misty.jpg",
        # Add more conditions as needed
    }

    # Get the corresponding image file for the condition
    image_file = condition_map.get(condition, "default.jpg")  # Fallback to a default image

    # Load the image
    bg_image = Image.open(os.path.join(image_path, image_file))
    bg_image = bg_image.resize((900, 600), Image.LANCZOS)
    bg_image_tk = ImageTk.PhotoImage(bg_image)

    # Update the background label
    bg_label.configure(image=bg_image_tk)
    bg_label.image = bg_image_tk  # Keep a reference to avoid garbage collection

# Function to get weather
def get_weather(city=None):
    if city is None:
        city = city_entry.get()  # Get city from input box
    if city:
        url = base_url + "q=" + city + "&appid=" + api_key + "&units=metric"
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != "404":
            main = data["main"]
            weather = data["weather"][0]
            temperature = main["temp"]
            humidity = main["humidity"]
            description = weather["description"]
            weather_result.set(f"Weather in {city.capitalize()}:\n"
                               f"Temperature: {temperature}°C\n"
                               f"Humidity: {humidity}%\n"
                               f"Description: {description.capitalize()}")

            # Update background based on weather condition
            update_background(weather["main"])
        else:
            messagebox.showerror("Error", "City not found.")
    else:
        messagebox.showwarning("Input Error", "Please enter a city name.")

# Initialize window
root = tk.Tk()
root.title("Weather App")
root.geometry("900x600+300+200")

# Background image
bg_image = Image.open("bg.jpg")  # Change to your image filename
bg_image = bg_image.resize((900, 600), Image.LANCZOS)  # Resize image to fit window
bg_image_tk = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_image_tk)
bg_label.place(relwidth=1, relheight=1)

# Heading
heading_label = tk.Label(root, text="Weather", font=("Georgia", 24), fg="#dfe2e8", bg="#5899ca")
heading_label.pack(pady=20)

# Frame for search box with shadow effect
shadow_frame = tk.Frame(root, bg="darkgray", bd=0)
shadow_frame.pack(pady=10, padx=5)

frame = tk.Frame(shadow_frame, bg="white", bd=5)  # Main frame with white background
frame.pack(pady=5, padx=5)

# Search box (Entry widget)
city_entry = tk.Entry(frame, font=("Arial", 14), width=30)
city_entry.grid(row=0, column=0, padx=10)

# Function to search weather
def search_weather():
    get_weather()

# Search button
search_icon = Image.open("search_symbol.png")
search_icon = search_icon.resize((40, 40), Image.LANCZOS)  # Adjust size as needed
search_icon_tk = ImageTk.PhotoImage(search_icon)

# Create a button with the search icon
search_button = tk.Button(frame, image=search_icon_tk, command=search_weather, bg="lightblue", borderwidth=0)
search_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Result label for displaying weather info
weather_result = tk.StringVar()
result_label = tk.Label(root, textvariable=weather_result, font=("Arial", 16), bg="lightblue", fg="white")
result_label.pack(pady=20)

def get_current_location_weather():
    g = geocoder.ip('me')  # Get current location based on IP
    if g.ok:
        current_city = g.city  # Get city name
        get_weather(current_city)
    else:
        messagebox.showwarning("Location Error", "Could not get the current location.")
# Get the weather for the user's current location by default (you may implement a function for this)
def  get_default_weather():
    # You can hardcode a location for testing purposes or implement geolocation functionality
    default_city = "YourCity"  # Replace with a default city
    get_weather(default_city)

get_current_location_weather()

# Start the Tkinter loop
root.mainloop()
