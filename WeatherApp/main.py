import requests
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import random

API_KEY = "3d13ff01fc35a1d60da31f4f410e8e7f"

class WeatherApp:
    # Weather icons
    weather_icons = {
        "clear sky": "clear_sky.png",
        "few clouds": "few_clouds.png",
        "scattered clouds": "scatd_clouds.png",
        "broken clouds": "brok_clouds.png",
        "shower": "shower_rain.png",
        "rain": "rainy.png",
        "thunderstorm": "thunder.png",
        "snow": "snow.png",
        "mist": "mist.png",
        "fog": "fogg.png",
        "light rain": "light_rain.png",
        "haze": "haze.png",
        "overcast clouds": "overcast.png",
        "smoke": "smoke.png",
        "heavy rain": "heavy_rain.png",
        "drizzle": "drizzle.png",
        "tornado": "tornado.png",
        "freezing rain": "freezing.png",
        "blizzard": "bliz.png",
        "frost": "frost.png",
        "dust storm": "dust.png",
        "sandstorm": "sand.png",
        "heavy intensity rain": "intense_raining.png",
        "moderate rain": "mod_rain.png"
    }

    def __init__(self, root):
        """
        Initialize the WeatherApp.
        """
        self.root = root
        self.root.geometry("500x630")
        self.root.maxsize(500, 630)
        self.root.minsize(500, 630)
        self.root.title("Weather-App")

        # creating references
        self.images = ["bgs/bg1.png", "bgs/bg2.png", "bgs/bg6.png", "bgs/bg8.png", "bgs/bg9.png", "bgs/bg10.png","bgs/bg11.png", "bgs/bg12.png", "bgs/bg13.png", "bgs/bg14.png", "bgs/bg15.png", "bgs/bg16.png"]

        self.bg = None
        self.canv = None
        self.weather_icon_reference = None
        self.temp_icon_reference = None
        self.temp_gifs_reference = None
        self.humid_icon_reference = None
        self.entry = None
        self.gif_frames = None
        
        self.load_background()  # Load background image before creating the canvas
        self.create_canvas()         
        self.get_city()
        self.root.after(2000, self.delay_entry) # Schedule the delay_entry method to be called after 7000 milliseconds

    def load_background(self):
        """
        load and display a random background image.
        """
        image = random.choice(self.images)
        im = Image.open(image)
        im = im.resize((500, 630))
        self.bg = ImageTk.PhotoImage(im)

    def create_canvas(self):
        """
        create a Canvas widget and display the background image.
        """
        self.canv = Canvas(self.root)
        self.canv.pack(fill=BOTH, expand=True)
        self.canv.create_image(0, 0, image=self.bg, anchor="nw")
        self.clear_prev_gif()

    def get_weather_by_city(self, city):
        """
        Get weather information for a given city and display it on the canvas.
        """
        self.clear_weather_display()  # Clear any previous weather details
        self.load_background()
        self.redraw_background()  # Redraw the background
        self.clear_prev_gif()

        if self.entry:
            self.entry.delete(0, END)  # Clear entry widget if it exists

        # Fetch weather data and display it
        try:
            # API request URL
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

            # Send API request
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:  # Check if the request was successful
                # Extract relevant weather info
                weather_description = data["weather"][0]["description"]
                temperature = data["main"]["temp"]
                humidity = data["main"]["humidity"]

                icon_file = self.weather_icons.get(weather_description.lower())

                try:
                    # Load and display icons
                    icon_path = f"weather_icons/{icon_file}"
                    icon = Image.open(icon_path)
                    icon = icon.resize((150, 150))
                    weather_icon = ImageTk.PhotoImage(icon)
                    self.weather_icon_reference = weather_icon
                    
                    # Display weather icon on the canvas and animate its position
                    weather_icon_canvas = self.canv.create_image(self.root.winfo_screenwidth(), 138, image=weather_icon, anchor=CENTER)
                    self.animate(weather_icon_canvas, end_x=240, end_y=138)

                except FileNotFoundError:
                    messagebox.showinfo("No Image", f"No image regarding the current weather description at {city} is in the system\napollogies for a less amusing output")
                except Exception as e:
                    messagebox.showerror("Error", f"{e}")
                
                # Determine temperature icon
                if temperature >= 45:
                    temp_icon = "broken_thermo.png"
                    temp_gif = "toohot.gif"
                elif (temperature >= 40) and (temperature < 45):
                    temp_icon = "hott.png"
                    temp_gif = "too_hot.gif"
                elif (temperature >= 34) and (temperature < 40):
                    temp_icon = "hot.png"
                    temp_gif = "alsohot.gif"
                elif (temperature >= 24) and (temperature < 34):
                    temp_icon = "warm.png"
                    temp_gif = "warmhot.gif"
                elif (temperature >= 15) and (temperature < 24):
                    temp_icon = "moderate.png"
                    temp_gif = "about_right.gif"
                elif (temperature >= 1) and (temperature < 15):
                    temp_icon = "cold.png"
                    temp_gif = "alright_cold.gif"
                else:
                    temp_icon = "coldd.png"
                    temp_gif = "too_cold.gif"

                try:
                    temp_icon_path = f"temp_icons/{temp_icon}"
                    temp_icon_img = Image.open(temp_icon_path)
                    temp_icon_img = temp_icon_img.resize((100, 100))
                    temp_icon_tk = ImageTk.PhotoImage(temp_icon_img)
                    self.temp_icon_reference = temp_icon_tk

                    # display temperature icon and animate it
                    temp_icon_canvas = self.canv.create_image(self.root.winfo_screenwidth(), 317, image=temp_icon_tk, anchor=CENTER)
                    self.animate(temp_icon_canvas, end_x=216, end_y=317)

                except Exception as e:
                    messagebox.showerror("Error", f"{e}")

                try:
                    # now loading temperature_gifs
                    gif_path = f"temp_gifs/{temp_gif}"
                    gif_fames = self.load_gif_frames(gif_path)

                    # display GIF frames and start animation
                    self.display_gif_frames(gif_fames)

                    # Add logic to clear previous GIF frames after displaying new ones
                    self.root.after(5000, self.clear_prev_gif)  # Clear previous GIF frames after 5 seconds

                except Exception as e:
                    messagebox.showerror("Error", e)
                    print(e)

                # Determine humidity icon
                if humidity <= 39:
                    humidity_icon = "low.png"
                elif humidity <= 60:
                    humidity_icon = "mod.png"
                else:
                    humidity_icon = "high_pic.png"
                try:
                    humidity_icon_path = f"humid_icons/{humidity_icon}"
                    humidity_icon_img = Image.open(humidity_icon_path)
                    humidity_icon_img = humidity_icon_img.resize((130, 130))
                    humidity_icon_tk = ImageTk.PhotoImage(humidity_icon_img)
                    self.humid_icon_reference = humidity_icon_tk

                    # Display humidity icon and animate it
                    humidity_icon_canvas = self.canv.create_image(self.root.winfo_screenwidth(), 483, image=humidity_icon_tk, anchor=CENTER)
                    self.animate(humidity_icon_canvas, end_x=240, end_y=483)

                except Exception as e:
                    messagebox.showerror("Error", "{e}")

                # Display weather data in text
                self.canv.create_text(247, 20, text=f"\nWeather at '{city.title()}' reads:", font=("verdana", 11, "bold italic"), fill="cyan")
                self.canv.create_text(239, 219, text=f"{weather_description.title()}", font=("Helvetic", 12, "bold italic"), fill="cyan")
                self.canv.create_text(252, 381, text=f"Temperature at: {temperature}°c", font=("Helvetic", 12, "bold italic"), fill="cyan")
                self.canv.create_text(248, 554, text=f"Humidity around: {humidity}%", font=("Helvetic", 12, "bold italic"), fill="cyan")
            else:
                messagebox.showinfo("Invalid Input", "Please enter a valid location")

        except requests.ConnectionError:
            messagebox.showerror("Connection Error", "Failed to connect to the weather service. Please check your internet connection and try again.")
        except Exception as e:
            messagebox.showerror("Error", f"An Error occurred: {e}")

    def delay_entry(self):
        """
        create a entry widget and delay its appearance on the canvas.
        """
        self.entry = Entry(self.root, relief="ridge", bd=2, bg="darkgrey", fg="black",
                           font=("comic sans ms", 10, "bold italic"), width=23)
        self.entry.insert(0, "Try out a different location")
        self.canv.create_window(248, 605, window=self.entry)

        # binding entry widget to clear text using focus in allows the instructory text to be cleared upon user's click
        self.entry.bind("<FocusIn>", self.clear_text)
        # the usual return key bind to entry widget allows get weather by city to recieve city's name from the user
        self.entry.bind("<Return>", lambda event: self.get_weather_by_city(self.entry.get()))

    def get_city(self):
        """
        Automatically retrieve the location of the user.
        """
        try:
            ip_request = requests.get('https://ipinfo.io/json') #sending a req to ipinfo to retrieve user's ip address
            ip_address = ip_request.json() #converting the retrieved ip address to json format
            city = ip_address.get("city", "") #extracting exact location through the retrieved ip address
            if city:
                self.get_weather_by_city(city)
            else:
                messagebox.showerror("Error", "Could not extract the city's name")
        except requests.ConnectionError:
            messagebox.showerror("Connection Error", "Could not connect to the server to fetch required location data")
        except Exception as e:
            messagebox.showerror("Error", f"{e}")

    def animate(self, icon_id, end_x, end_y, slide_step=25):
        """
        Animate the movement of weather icons on the canvas.
        Icon id is for the specific icon that the animation is being called for
        End_x and End_y are the final coordinates of the icons on the screen
        Slide_step is basically the speed at which the slide in effect is going to take place
        """
        x, y = self.root.winfo_screenwidth(), end_y #first we set the initial pos of the icons outside the canvas/screen
        # root.winfo_screenwidth is giving us the num of pixels in the screenwidth of the widget
        while x > end_x: #we continue the loop till current x coordinate bcomes equal to the final x coordinate
            self.canv.coords(icon_id, x, y) #move the icons to the current pos through canv.coords method
            self.root.update()
            x -= slide_step #decreese the current x coordinate by slide step
            self.root.after(10) #added a delay of 10 miliseconds to try n smooth out the animation

    def clear_weather_display(self, ):
        """
        Clear weather details from the canvas.
        """

        if self.canv: #if the canvas previously isnt empty
            # get all widgets present on it
            all_widgets = self.canv.find_all()

            #initalize variables to store widget ids
            background_im_id = None
            entry_widget_id = None
            
            # filter out bg_id and entry_widg_id from all widgets
            for widget_id in all_widgets:
                # if isinstance of canv, is a string and is an image
                if isinstance(self.canv.type(widget_id), str) and "image" in self.canv.type(widget_id):
                    background_im_id = widget_id #keep id

                # if is an instance of canv, a string and is a window
                elif isinstance(self.canv.type(widget_id), str) and "window" in self.canv.type(widget_id):
                    entry_widget_id = widget_id #means its the entry widget, assign its id

            for widget_id in all_widgets:
                if widget_id != background_im_id and widget_id != entry_widget_id: #if ids to b removed arent the background image or entry widget
                    self.canv.delete(widget_id) # delete em

    def clear_text(self, event):
        """
        clears the entry widget text upon focus.
        """
        if self.entry and self.entry.get() == "Try out a different location":
            self.entry.delete(0, END)

    def redraw_background(self):
        """
        Redraw the background image on the canvas.
        We needed to redraw the canvas after a specific point.
        Becuz of all different functions that were added, our background image was being cleared unexpectedly
        """
        self.canv.create_image(0, 0, image=self.bg, anchor="nw")

    def load_gif_frames(self, gif_path):
        """
        we extract each frame from the gifs and then append them
        into gif_frames after converting each of those frames to imtk-photoim object
        """
        gif_frames = [] #initalizing a list to store each frame from a gif

        gif = Image.open(gif_path)

        # iterating through each frame of the gif using image.sequence.iterator
        for frame in ImageSequence.Iterator(gif):
            # resizeing each frame, we had to cause resizing the whole gif doesnt work
            resized_frame = frame.resize((140, 165))

            # convert it to the photoimage object of tk
            tk_resized_frame = ImageTk.PhotoImage(resized_frame)
            # and then simply return the gif_frames after appending each frame wev just iterated through
            gif_frames.append(tk_resized_frame)

        return gif_frames

    def display_gif_frames(self, gif_frames):
        self.clear_prev_gif()

        # create an image object for frames and display them on the canvas
        self.temp_gifs_reference = self.canv.create_image(83, 290, image=gif_frames[0]) ##start at the 1st index
        self.update_gif_frames(gif_frames, 0)

    def update_gif_frames(self, gif_frames, idx):
        # updates the image displayed on the canvas with the current frame
        self.canv.itemconfig(self.temp_gifs_reference, image=gif_frames[idx])

        # incrementing the index 
        idx = (idx + 1) % len(gif_frames) #so that we dont go out of range while incrementing the index
        self.root.after(55, self.update_gif_frames, gif_frames, idx) #adding a slight delay

    def clear_prev_gif(self):
       # Check if there are frames to delete
       if self.gif_frames:
        for frame in self.gif_frames:
            self.canv.delete(frame)  # Delete each frame from the canvas

def main():
    root = Tk()
    WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
