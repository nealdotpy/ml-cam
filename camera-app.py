from picamera import PiCamera
from time import sleep
# gui
from tkinter import *
from tkinter import font

import os, os.path

# fonts
#bFont = font.Font(family='Helvetica', size=36, weight='bold')

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
    sleep(5)
    print("captured pic. saved to 'pwd'")
    cam.capture("/home/pi/Desktop/pi-proj/test_img.jpg")
    cam.stop_preview()
    cam.close()
    googlevision("test_img.jpg")

def exit_app():
    exit(0)
    
root = Tk() # root of application
root.title("PICAMERA by NEALDOTPY")
root.geometry("500x300")
view = Frame(root) # assign to root of application -- master
view.pack()

preview = Button(view, text="PRESS ME", fg="white", bg="black",
#                 width=100, height=50,
                 font=font.Font(family='Helvetica', size=36, weight='bold'),
                 command=cap_preview).pack()
stop = Button(view, text="EXIT", fg="white", bg="red",
#                 width=100, height=50,
                 font=font.Font(family='Helvetica', size=36, weight='bold'),
                 command=exit_app).pack()

root.mainloop()





print("done.")
