import tkinter as tk
import numpy as np

class Shared_Memory():
    
    def __init__(self, root):
        self.mode_camera, self.mode_video = False, False
        self.open_times = 0
        self.beautify = True
        self.colours = np.array([1, 0, 0])
        self.radius = tk.StringVar(root)

        self.cube =  False

        self.start = False
        #!
        self.width_frame = None
        self.height_frame = None
        #!
        self.position_click = None 
    
    def data_get(self):
        print(self.radius.get(), self.cube)