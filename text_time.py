import time
from rich import print
from rich.console import Console
console = Console()

def text_chunk(text, delay):
    lines = text.split('\n')
    for line in lines:
        print(line)
        time.sleep(delay)

def text_slow(text, char_delay):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(char_delay)
     
def text_slow_with_delay(text, char_delay, line_delay):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(char_delay)
    time.sleep(line_delay)