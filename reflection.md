# Reflection: REST-GUI-API

In this project we connect two programs through JSON. The Tkinter form collects a purchase (Product ID, description, price, name, email, and an online/in-store checkbox), then it validates it locally, and sends it with json.dumps as an HTTP POST. The Flask API receives it at /submit, validates it again, and returns JSON that the form shows in a popup.

I adapted the tutorial by swapping the age and newsletter fields for purchase fields and the age check for a $1,000.00 price limit. Working on a MacBook required a few extra changes: I used python3 to build my environment, moved the API from port 5000 to 5001 because macOS uses 5000 for AirPlay, and fixed a blank form caused by Apple's outdated Tk 8.5 by rebuilding the environment with Anaconda's Python and Tk 8.6. I also ignored a Tk deprecation warning after doing some research about it.

I was surprised that most problems came from the environment, not the code. I now better understand client versus server validation and JSON as a contract between components, and I want to learn more about REST design aspect as it could be useful in my current workplace.