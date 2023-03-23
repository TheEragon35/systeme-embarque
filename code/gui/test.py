import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import time
from threading import Thread
import depthai as dai

import sys
sys.path.append("../")
from app.app import Camera, Model


# Global variable
isActive = True

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.isActive = True

    def create_widgets(self):

        # Créer un label pour afficher le temps écoulé depuis le lancement de l'application
        self.labelHeure = tk.Label(self)
        self.labelHeure.pack(side="bottom")

        self.labelNbClass = tk.Label(self)
        self.labelNbClass.pack(side="bottom")

        self.buttonClose = tk.Button(self)
        self.buttonClose = tk.Button(self, text= "Close the Window", command=self.close).pack(side="bottom")

        # Charger une image d'un site web
        self.img = Image.open("../app/assets/loading.jpg")
        self.photo = ImageTk.PhotoImage(self.img)
        self.image_label = tk.Label(self, image=self.photo)
        self.image_label.pack(side="top")

    def update_image(self, img, classes):
        # Mettre à jour l'heure affichée dans le label
        current_time = time.strftime("%H:%M:%S")
        self.labelHeure.configure(text=current_time)
        self.labelNbClass.configure(text="Nombre de classes détectés: "+str(classes))


        self.photo = ImageTk.PhotoImage(Image.fromarray(img[:,:,::-1]))
        self.image_label.configure(image=self.photo)

    def close(self):
        self.isActive = False
        self.destroy()
        self.quit()

# Créer une fenêtre Tkinter
root = tk.Tk()

# Créer une instance de la classe App
app_main = App(master=root)


def thread_cam():
    model = Model()
    model.loadModel()

    camera = Camera()
    camera.setup()

    # Connect to device and start pipeline
    with dai.Device(camera.pipeline) as deviceCamera:

        # Output queue will be used to get the rgb frames from the output defined above
        qRgb = deviceCamera.getOutputQueue(name="rgb", maxSize=4, blocking=False)

        while app_main.isActive:
            inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived

            orig_image = inRgb.getCvFrame() #store frame

            results = model.prediction(orig_image)
            # print(type(results.render()[0]), results.__dict__)
            app_main.update_image(results.render()[0], len(results.pred[0]))


    sys.exit()

t = Thread(name='camera', target=thread_cam)
t.start()

# Lancer l'application Tkinter en boucle d'événements
app_main.mainloop()