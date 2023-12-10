import tkinter as tk


def print_tw(widget: tk.Text, message: str, error=False, susses=False) -> None:
    # set message color according to message type
    widget["foreground"] = "black"
    if error:
        widget["foreground"] = "red"
    elif susses:
        widget["foreground"] = "green"
    widget.delete("0.0", tk.END)
    widget.insert("0.0", message)
