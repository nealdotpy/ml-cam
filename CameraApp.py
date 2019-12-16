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
    def __init__(self, parent, gvo): # 1 param constructor: "parent"
        Frame.__init__(self, parent) # "super" call
        self.gvo = gvo
        self.img = ImageTk.PhotoImage(Image.open("test_img.jpg"))
        self.image_view = Label(self)
        self.image_view.image = self.img
        self.image_view.configure(image=self.img)
        self.image_view.pack(side=LEFT)
        parent.geometry("800x400")

    def tags(self): # add location based tags for each object in the picture (label)
        if (self.gvo.num_obj == 0):
            print("found no objects. sorry :/")
            return
        for obj in self.gvo.found:
            for k in self.gvo.found[obj]:
                print(k, self.gvo.found[obj][k]) # testing line
            label = Label(self, text=self.gvo.found[obj]["name"], font=font.Font(family='Helvetica', size=15, weight='bold'))
            label.place(x=round(800*self.gvo.found[obj]["locx"],0), y=round(400*self.gvo.found[obj]["locy"],0))
            #label.pack()
        

class CameraFrame(Frame): # "extends" Frame
    def __init__(self, parent): # 1 param constructor: "parent"
        Frame.__init__(self, parent) # "super" call
        preview = Button(self, text="TAKE PICTURE", fg="white", bg="green",
                         font=font.Font(family='Helvetica', size=25, weight='bold'),
                         command=cap_preview).pack()
        stop = Button(self, text="EXIT", fg="white", bg="red",
                      font=font.Font(family='Helvetica', size=20, weight='bold'),
                      command=lambda : exit(0)).pack()
        parent.geometry("400x200")

class GVObject(): # GoogleVisionObject
    def __init__(self, path):
        self.google_vision(path)

    def info(self):
        print("FOUND: " + str(self.num_obj))
        if (self.num_obj > 0): # don't try to parse if 0 objects found
            for outer_key in self.found:
                print("\n" + str(self.found[outer_key]["name"]) + ": "
                      + str(round(self.found[outer_key]["score"]*100,2)) + " PERCENT")
                print("N(x,y): (" + str(round(self.found[outer_key]["locx"], 5))
                      + "," + str(round(self.found[outer_key]["locy"], 5)) + ")")

    def google_vision(self, path):
        """
        Localize objects in the local image.
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
#            print('Number of objects found: {}'.format(len(objects)))
            self.num_obj = len(objects) # num of objects
            self.found = {0 : {"test" : 69420}}
            n = 0
            for object_ in objects:
                locx = -1 # can't be negative
                locy = -1 # can't be negative
#                print('\n{} (confidence: {})'.format(object_.name, object_.score))
#                print('Normalized bounding polygon vertices: ')
                i = 0
                for vertex in object_.bounding_poly.normalized_vertices:
                    if (locx < 0 and i % 2 == 0): # grabs vertex one which we want
                        locx = vertex.x
                        locy = vertex.y
                    elif (locx > 0 and i % 2 == 0): # grabs vertex three which we want
                        locx -= vertex.x
                        locy -= vertex.y
#                    print(' - ({}, {})'.format(vertex.x, vertex.y))
                    i += 1
                self.found[n] = {"name" : object_.name,
                                 "score" : object_.score,
                                 "locx" : abs(locx),
                                 "locy" : abs(locy)}
                n += 1

def cap_preview():
    dur = 5
    cam = PiCamera()
    cam.start_preview()
    for i in range(dur):
        cam.annotate_text = str(dur - i)
        sleep(1)
    cam.annotate_text = ""
    print("captured pic. saved to 'pwd' as 'test_img.jpg'")
    cam.capture("/home/pi/Desktop/pi-proj/test_img.jpg")
    cam.stop_preview()
    cam.close()
    gvo = GVObject("test_img.jpg")
    gvo.info()
    display_img(gvo)

def display_img(gvo):
    if (root != None):
        top = Toplevel(root)
        imgFr = ImageFrame(top, gvo)
        imgFr.tags()
        imgFr.pack(side=LEFT)
        
        
def main():
    global root
    root = Tk() # root of application
    root.title("PICAMERA by NEALDOTPY")
    CameraFrame(root).pack(fill="both", expand=True)
    cap_preview()
    root.mainloop()    

if __name__ == "__main__":
    main()
    

