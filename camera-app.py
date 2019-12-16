from picamera import PiCamera
from time import sleep
# gui
from tkinter import *
from tkinter import font

import os, os.path

from PIL import Image
from PIL import ImageTk

root = None # global scope

class ImageFrame(Frame): # "extends" Frame
    def __init__(self, parent): # 1 param constructor: "parent"
        Frame.__init__(self, parent) # "super" call
        self.img = ImageTk.PhotoImage(Image.open("test_img.jpg"))
        self.image_view = Label(self)
        self.image_view.image = self.img
        self.image_view.configure(image=self.img)
        self.image_view.pack(side=LEFT)
        parent.geometry("800x400")

class CameraFrame(Frame): # "extends" Frame
    def __init__(self, parent): # 1 param constructor: "parent"
        Frame.__init__(self, parent) # "super" call
        preview = Button(self, text="TAKE PICTURE", fg="white", bg="green",
                         font=font.Font(family='Helvetica', size=25, weight='bold'),
                         command=cap_preview).pack()
        stop = Button(self, text="EXIT", fg="white", bg="red",
                      font=font.Font(family='Helvetica', size=20, weight='bold'),
                      command=lambda : exit(0)).pack()
        parent.geometry("800x400")

def display_img():
    if (root != None):
        print("root is not None")
        top = Toplevel(root)
        ImageFrame(top).pack(side=LEFT)
        
def main():
    global root
    root = Tk() # root of application
    root.title("PICAMERA by NEALDOTPY")
    CameraFrame(root).pack(fill="both", expand=True)
#    for i in range(0):
#        print("instantiated a new toplevel.")
#        top = Toplevel(root)
#        ImageFrame(top).pack(fill="both", expand=True)
    root.mainloop()

def googlevision(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))

def cap_preview():
    cam = PiCamera()
    cam.start_preview()
    for i in range(5):
        cam.annotate_text = str(5 - i)
        sleep(1)
    cam.annotate_text = ""
    print("captured pic. saved to 'pwd'")
    cam.capture("/home/pi/Desktop/pi-proj/test_img.jpg")
    cam.stop_preview()
    cam.close()
    display_img()
#    googlevision("test_img.jpg") # analyze

if __name__ == "__main__":
    main()
    

