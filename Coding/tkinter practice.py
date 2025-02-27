from customtkinter import *
from PIL import Image

app = CTk()
app.geometry("500x400")

set_appearance_mode("dark")

img = Image.open("C:/Users/amaan/Desktop/Coding/makima.png")

btn = CTkButton(master=app, text="Click Me", corner_radius=32, fg_color="transparent",
                hover_color="#4158D0", border_color="#FFCC70",
                border_width=2, image=CTkImage(dark_image=img, light_image=img))

btn.place(relx=0.5, rely=0.5, anchor="center")

app.mainloop()
