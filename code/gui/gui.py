import tkinter as tk
from PIL import Image, ImageTk
import time
from threading import Thread
import depthai as dai
import torch

import sys
sys.path.append("../")
from app.app import Camera, Model


class App(tk.Frame):
    def __init__(self, master=None, classes={}):
        super().__init__(master)
        self.master = master
        self.classes = classes
        self.pack()
        self.create_widgets()
        self.isActive = True


    def create_widgets(self):
        self.labelHeure = tk.Label(self)
        self.labelHeure.pack(side="bottom")

        self.labelNbClass = tk.Label(self)
        self.labelNbClass.pack(side="bottom")

        self.buttonClose = tk.Button(self, text= "Close the Window", command=self.close)
        self.buttonClose.pack(side="bottom")


        # Setup list for the classes choices.
        # If "Toutes les classes" is check other check is discard.
        self.listSelect = tk.Listbox(self, selectmode="multiple")
        self.listSelect.pack(side="right")
        
        for key in self.classes:
            self.listSelect.insert(key, self.classes[key])

        self.listSelect.insert(len(self.classes), "Toutes les classes")
        self.listSelect.select_set(0)

        # Setup image.
        self.img = Image.open("../app/assets/loading.jpg")
        self.photo = ImageTk.PhotoImage(self.img)
        self.image_label = tk.Label(self, image=self.photo)
        self.image_label.pack(side="top")


    def update_image(self, img, classes):
        # Update Hour.
        current_time = time.strftime("%H:%M:%S")
        self.labelHeure.configure(text=current_time)
        self.labelNbClass.configure(text="Nombre de classes détectés: "+str(classes))

        # Update image.
        self.photo = ImageTk.PhotoImage(Image.fromarray(img[:,:,::-1]))
        self.image_label.configure(image=self.photo)


    def close(self):
        self.isActive = False
        self.destroy()
        self.quit()


def thread_cam(app_main, model, camera):

    # Connect to device and start pipeline
    with dai.Device(camera.pipeline) as deviceCamera:

        # Output queue will be used to get the rgb frames from the output defined above
        qRgb = deviceCamera.getOutputQueue(name="rgb", maxSize=4, blocking=False)

        while app_main.isActive:
            # Get an image from the queu.
            inRgb = qRgb.get() 

            # Transform to cv2 image.
            orig_image = inRgb.getCvFrame()

            # Process throw thw model.
            results = model.prediction(orig_image) 
            
            # In case the main application already quit.
            if not app_main.isActive: break

            # Keep only the predictions on the check classes.
            selected_classes = list(app_main.listSelect.curselection())
            if 80 not in selected_classes:
                a = []
                for row in results.pred[0]:
                    if int(row[5]) in selected_classes:
                        a.append(row)
                
                results.pred[0] = torch.Tensor() if a == [] else torch.stack(a)

            # Update the image.
            app_main.update_image(results.render()[0], len(results.pred[0]))
    sys.exit()


if __name__ == "__main__":

    root = tk.Tk()

    model = Model()
    camera = Camera()

    app_main = App(master=root, classes=model.model.names)

    t = Thread(name='camera', target=thread_cam, args=(app_main, model, camera, ))
    t.start()

    app_main.mainloop()