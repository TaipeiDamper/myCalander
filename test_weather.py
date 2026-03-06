import tkinter as tk
from weather.weather_widget import HiddenWeatherWidget

root = tk.Tk()
widget = HiddenWeatherWidget(root, mode='header')
widget.pack()
root.after(3000, root.destroy)
root.mainloop()
