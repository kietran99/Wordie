import tkinter as tk
from threading import Thread
from time import sleep
from typing import Callable

class CountdownView:
    def __init__(self, seconds:int, interval:[int|None]=None, interval_callback:Callable[[], None]=lambda:None, complete_callback:Callable[[], None]=lambda:None) -> None:
        self.seconds = seconds
        self.interval:[int|None] = interval
        self.interval_callback:Callable[[], None] = interval_callback
        self.complete_callback:Callable[[], None] = complete_callback

        self.root = tk.Tk()
        self.root.geometry("170x240")
        self.root.title("Wordie")

        self.time_label = tk.Label(self.root, font=('CascadiaCode', 108), text=f'{self.seconds:02d}')
        self.time_label.grid(row=0, column=0, columnspan=2)

        self.start_button = tk.Button(self.root, font=('CascadiaCode', 16), text='Start', command=self.create_countdown_thread)
        self.start_button.grid(row=1, column=0, padx=5, pady=5)

        # self.pause_button = tk.Button(self.root, font=('CascadiaCode', 16), text='Pause', command=self.pause)
        # self.pause_button.grid(row=1, column=1, padx=5, pady=5)

        self.stop_button = tk.Button(self.root, font=('CascadiaCode', 16), text='Stop', command=self.stop)
        self.stop_button.grid(row=1, column=1, padx=5, pady=5)

        self.should_stop = False
        self.should_pause = False

        self.root.mainloop()

    def create_countdown_thread(self):
        t = Thread(target=self.start)
        t.start()

    def start(self):
        print(f'Start total = {self.seconds} interval = {self.interval}')
        self.should_stop = False

        remaining = self.seconds
        elapsed = 0
        while not self.should_stop and remaining > 0:
            # if self.should_pause:
                # continue

            self.time_label.config(text=f'{remaining:02d}')
            if self.interval and elapsed % self.interval == 0:
                self.interval_callback()
            sleep(1)
            remaining -= 1
            elapsed += 1

        self.time_label.config(text='00')
        self.complete_callback()

    # def pause(self):
    #     print('Pause')
    #     self.should_pause = True

    def stop(self):
        print('Stop')
        self.should_stop = True
        self.time_label.config(text='00')
        self.root.destroy()

def test() -> None:
    CountdownView(10, 2, on_interval_elapsed, on_complete)

def on_interval_elapsed() -> None:
    print("Next")

def on_complete() -> None:
    print("Complete")

if __name__ == '__main__':
    test()