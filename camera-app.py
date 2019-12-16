from picamera import PiCamera
from time import sleep
# gui
from tkinter import *
from tkinter import font

import os, os.path

from PIL import Image
from PIL import ImageTk

img_view = None

class ImageFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.image_view = Label(self, text="IMAGE HERE", image=ImageTk.PhotoImage(Image.open("test_img.jpg")))
        self.image_view.pack(side="left", fill="both", expand=True)
        self.text = Label(self, text="word goes here").pack(side="left", fill="both", expand=True
        
def main():
    root = Tk() # root of application
    root.title("PICAMERA by NEALDOTPY")
    #root.geometry("750x400")
    ImageFrame(root).pack(fill="both", expand=True)
    for i in range(0):
        top = Toplevel(root)
        ImageFrame(top).pack(fill="both", expand=True)
    '''
    view = Frame(root) # assign to root of application -- master
    view.pack()
    load = Image.open("test_img.jpg")
    image = ImageTk.PhotoImage(load)
    img_view = Label(view, text="IMAGE HERE", image=image)
    preview = Button(view, text="TAKE PICTURE", fg="white", bg="green",
                     #                 width=100, height=50,
                     font=font.Font(family='Helvetica', size=25, weight='bold'),
                     command=cap_preview).pack()
    stop = Button(view, text="EXIT", fg="white", bg="red",
                  #                 width=100, height=50,
                  font=font.Font(family='Helvetica', size=20, weight='bold'),
                  command=exit_app).pack()
    if (img_view != None):
        img_view.pack()        
    '''
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
#    global count_label
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
    update_view()
    sleep(0.000001) # microsecond
    googlevision("test_img.jpg") # analyze

def exit_app():
    #googlevision("test_img_2.jpg") # easy testing
    exit(0)

def update_view():
    print("Updating view. img_view exists: " + str(img_view != None))
    display_out_img()

def display_out_img():
    global img_view
    root = TopLevel()
    root.title("DISPLAY_OUT")
    root.geometry("800x400")
    view = Frame(root) # assign to root of application -- master
    view.pack()
    new_image = ImageTk.PhotoImage(Image.open("test_img.jpg"))
    if (img_view != None):
        img_view.configure(image=new_image)
        img_view.image = new_image
    outimg = Label(view, text="IMAGE HERE",  image=new_image).pack()

if __name__ == "__main__":
    main()
    

