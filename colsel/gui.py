import tkinter as tk
from tkinter.filedialog import askopenfile, askopenfilename

import time
import numpy as np
import queue
import gc
from loop import *

#somewhere accessible to both:
callback_queue = queue.Queue()


# https://stackoverflow.com/questions/18989446/execute-python-function-in-main-thread-from-call-in-dummy-thread

def from_dummy_thread(func_to_call_from_main_thread):
    callback_queue.put(func_to_call_from_main_thread)

def from_main_thread_blocking():
    callback = callback_queue.get() #blocks until an item is available
    callback()

def from_main_thread_nonblocking():
    while True:
        try:
            callback = callback_queue.get(False) #doesn't block
        except queue.Empty: #raised when queue is empty
            break
        callback()

#

class GUI_client(tk.Frame):
    def __init__(self, parent, shared_memory, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        
        self.shared = shared_memory
        
        #!
        self.secret_effect = False
        #!
        
        self.parent = parent

        self.frame_buttons = tk.Frame(self, width=120, height=100)
        self.frame_better_options = tk.Frame(self, width=120, height=100)
        self.frame_sliders = tk.Frame(self, width=120, height=220)
        self.frame_radius = tk.Frame(self.frame_sliders, width=35, height=220)
        self.frame_width = tk.Frame(self.frame_sliders, width=35, height=220)
        self.frame_height = tk.Frame(self.frame_sliders, width=35, height=220)

        self.frame_choose_colour = tk.Frame(self, width=120, height=100)
        self.blue_button = tk.Button(master = self.frame_choose_colour, text = "Blue Colour", command = lambda *args: self.set_colour(np.array([1, 0, 0])) )
        self.green_button = tk.Button(master = self.frame_choose_colour, text = "Green Colour", command = lambda *args: self.set_colour(np.array([0, 1, 0])) )
        self.red_button = tk.Button(master = self.frame_choose_colour, text = "Red Colour", command = lambda *args: self.set_colour(np.array([0, 0, 1])) )

        
        self.open_video_button = tk.Button(master = self.frame_buttons, text = "Video", command = self.start_video)
        self.camera_button = tk.Button(master = self.frame_buttons, text = "Camera", command = self.start_camera)
        self.close_vc = tk.Button(master = self.frame_buttons, text = "Close", command = self.close_all)
        
        self.beuaty_button = tk.Button(master = self.frame_better_options, text = "Beauty", command = self.beuaty_effect)
        
        self.text_cube = tk.StringVar()
        self.cube_sphere = tk.Button(master = self.frame_better_options, textvariable = self.text_cube, command = self.cube_funct)
        self.text_cube.set("Make Cube")
        
        self.text_start = tk.StringVar()
        self.start_button = tk.Button(master = self.frame_better_options, textvariable = self.text_start, command = self.start_process)
        self.text_start.set("Start")


        self.label_radius = tk.Label(self.frame_radius, text ='W / Radius')

        self.radius_scale = tk.Scale(self.frame_radius,
                variable   = self.shared.radius,    # MVC-Model-Part value holder
                from_      = 0.0,       # MVC-Model-Part value-min-limit
                to         =  3.0,       # MVC-Model-Part value-max-limit
                length     = 200,         # MVC-Visual-Part layout geometry [px]
                digits     =   4,         # MVC-Visual-Part presentation trick
                resolution =   0.05       # MVC-Controller-Part stepping
                )
        self.shared.radius.set(0.75)


        self.label_width = tk.Label(self.frame_width, text ='Width')
        if self.shared.width_frame == None:
            self.shared.width_frame = tk.StringVar()
        
        self.width_scale = tk.Scale(self.frame_width,
                variable   = self.shared.width_frame,    # MVC-Model-Part value holder
                from_      = 20,       # MVC-Model-Part value-min-limit
                to         =  1920,       # MVC-Model-Part value-max-limit
                length     = 200,         # MVC-Visual-Part layout geometry [px]
                digits     =   4,         # MVC-Visual-Part presentation trick
                resolution =   10       # MVC-Controller-Part stepping
                )
        self.shared.width_frame.set(1920)

        #!
        self.label_height = tk.Label(self.frame_height, text ='Height')
        if self.shared.height_frame == None:
            self.shared.height_frame = tk.StringVar()
        
        self.height_scale = tk.Scale(self.frame_height,
                variable   = self.shared.height_frame,    # MVC-Model-Part value holder
                from_      = 20,       # MVC-Model-Part value-min-limit
                to         =  1080,       # MVC-Model-Part value-max-limit
                length     = 200,         # MVC-Visual-Part layout geometry [px]
                digits     =   4,         # MVC-Visual-Part presentation trick
                resolution =   10       # MVC-Controller-Part stepping
                )
        self.shared.height_frame.set(1080)


        self.frame_buttons.pack(fill=tk.BOTH, expand = True) 
        self.frame_better_options.pack(fill=tk.X, expand = True) 
        self.frame_sliders.pack(fill=tk.BOTH, expand = True) 
        
        self.frame_radius.pack(side=tk.LEFT, fill=tk.Y, expand = True) 
        self.frame_width.pack(side=tk.LEFT, fill=tk.Y, expand = True) 
        self.frame_height.pack(side=tk.RIGHT, fill=tk.Y, expand = True) 

        self.frame_choose_colour.pack(fill=tk.BOTH, expand = True) 

        self.open_video_button.config(font=("Courier", 14))
        self.camera_button.config(font=("Courier", 14))
        self.close_vc.config(font=("Courier", 14))
        
        self.beuaty_button.config(font=("Courier", 14))
        self.cube_sphere.config(font=("Courier", 14))
        self.start_button.config(font=("Courier", 14))
        

        self.label_radius.config(font=("Courier", 14))
        self.radius_scale.config(font=("Courier", 14))

        self.label_width.config(font=("Courier", 14))
        self.width_scale.config(font=("Courier", 14))

        self.label_height.config(font=("Courier", 14))
        self.height_scale.config(font=("Courier", 14))

        self.blue_button.config(font=("Courier", 14))
        self.green_button.config(font=("Courier", 14))
        self.red_button.config(font=("Courier", 14))



        self.open_video_button.pack(padx=5, pady=5, side=tk.LEFT)
        self.camera_button.pack(padx=5, pady=5, side=tk.LEFT)
        self.close_vc.pack(padx=5, pady=5, side=tk.RIGHT)

        self.beuaty_button.pack(padx=5, pady=5, side=tk.LEFT)
        self.cube_sphere.pack(padx=5, pady=5, side=tk.LEFT)
        self.start_button.pack(padx=5, pady=5, side=tk.RIGHT)

        self.label_radius.pack(padx=5, pady=5, side=tk.TOP)
        self.radius_scale.pack(padx=5, pady=5, side=tk.LEFT)

        self.label_width.pack(padx=5, pady=5, side=tk.TOP)
        self.width_scale.pack(padx=5, pady=5, side=tk.LEFT)

        self.label_height.pack(padx=5, pady=5, side=tk.TOP)
        self.height_scale.pack(padx=5, pady=5, side=tk.LEFT)

        self.blue_button.pack(padx=5, pady=5, side=tk.LEFT)
        self.green_button.pack(padx=5, pady=5, side=tk.LEFT)
        self.red_button.pack(padx=5, pady=5, side=tk.LEFT)

    def set_colour(self, colours):
        self.shared.colours = colours


    def start_process(self):
        self.shared.start = self.shared.start == False
        if self.shared.start:
            self.text_start.set("Stop")
        else:
            self.text_start.set("Start")


    def cube_funct(self):
        self.shared.cube = self.shared.cube == False
        
        if not self.shared.cube:
            self.shared.radius.set(0.65)
            self.text_cube.set("Make Cube")
        else:
            self.shared.radius.set(1.1)
            self.text_cube.set("Make Sphere")

    def beuaty_effect(self):
        self.shared.beautify = self.shared.beautify == False


    def close_all(self):
        self.shared.mode_camera = False
        self.shared.mode_video = False
        #self.stopEvent_camera.set()
        print("closing")

    def start_video(self):
        self.shared.mode_camera = False
        self.shared.mode_video = True
        #self.stopEvent_camera.set()
        path = askopenfilename()
        print(path)
        from_dummy_thread(lambda: video_loop(self.shared, path))
        time.sleep(0.5)

    def start_camera(self):
        self.shared.open_times += 1 
        self.shared.mode_camera = True
        self.shared.mode_video = False
        print("camera")
        #self.stopEvent_camera = threading.Event()
        from_dummy_thread(lambda: camera_loop(self.shared))
        time.sleep(0.5)
        #camera_thread = threading.Thread(target=self.camera_loop, args=())
        #camera_thread.daemon = True
        #camera_thread.start()
