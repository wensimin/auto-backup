import threading
import tkinter as tk

import time


class Job(threading.Thread):
    def __init__(self, console):
        super().__init__()
        self.console = console
        self.running = True
        self.count = 0

    def run(self):
        while self.running:
            self.count = self.count + 1
            self.console.set(self.count)
            time.sleep(1)

    def stop(self):
        self.running = False


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.console = tk.StringVar()
        self.pack()
        self.hi_there = tk.Button(self)
        self.quit = tk.Button(self, text="QUIT", fg="red")
        self.job = Job(self.console)
        self.quit["command"] = lambda: exit()
        self.consoleLabel = tk.Label(self, textvariable=self.console)
        self.create_widgets()

    def exit(self):
        if self.job.is_alive():
            self.job.stop() & self.job.join()
        exit(0)

    def create_widgets(self):
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="left")
        self.quit.pack(side="right")
        self.consoleLabel.pack(side="bottom")

    def say_hi(self):
        if self.job.is_alive():
            self.job.stop()
            self.job.join()
            self.job = Job(self.console)
        else:
            self.job.start()


root = tk.Tk()
app = Application(root)
app.mainloop()
