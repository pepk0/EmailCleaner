import tkinter as tk
from tkinter import ttk

def print_tw(widget: tk.Label, message: str, error=False, susses=False) -> None:
    # set message color according to message type
    widget["foreground"] = "black"
    if error:
        widget["foreground"] = "red"
    elif susses:
        widget["foreground"] = "green"
    widget["text"] = message


