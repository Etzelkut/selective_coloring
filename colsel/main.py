import threading
from gui import *
from share_m import Shared_Memory


global close_message
close_message = False

def GUI():
    window = tk.Tk()
    
    def on_closing():
        global close_message
        close_message = True
        print("closed window")
        window.destroy()
        gc.collect()
    
    shared = Shared_Memory(window)
    window.title("GUI CV")
    GUI_client(window, shared).pack(fill=tk.BOTH, expand = True)
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()

# https://pysimplegui.readthedocs.io/en/latest/#multiple-threads


if __name__ == "__main__":
    GUI_thread = threading.Thread(target=GUI, args=[])
    GUI_thread.start()
    
    while not close_message:
        from_main_thread_nonblocking()
    
    GUI_thread.join()
