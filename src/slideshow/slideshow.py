from argparse import ArgumentParser
import os
import subprocess
from time import sleep

from countdown import CountdownView

INTERVAL:int = 10
SHOW_RESULT_DELAY:int = 2

def main(group_path:str, timeout:int, show_result_delay:int) -> None:
    image_names:list[str] = os.listdir(group_path)
    image_paths = [os.path.join(group_path, name) for name in image_names]
    n_images:int = len(image_paths) - 1
    image_paths_iter = iter(image_paths)
    countdown_view = CountdownView(n_images * timeout, timeout, lambda: on_interval_elapsed(image_paths_iter), lambda: on_completed(image_paths_iter, show_result_delay))

def on_interval_elapsed(path_iter) -> None:
    open_image(next(path_iter))

def on_completed(path_iter, show_result_delay:int) -> None:
    sleep(show_result_delay)
    open_image(next(path_iter))

def open_image(path:str) -> None:
    print(path)
    subprocess.Popen([path, '-WindowStyle', 'Maximized'], shell=True)

if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument('group', type=str, help='Word group dir path')
    args = arg_parser.parse_args()
    group_path:str = args.group
    main(group_path, INTERVAL, SHOW_RESULT_DELAY)