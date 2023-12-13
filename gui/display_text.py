import tkinter as tk


def print_tw(widget: tk.Label, message: str, error: bool = False,
             susses: bool = False) -> None:
    """ Displays text on a tkinter Label widget
    Args:
        widget (Label) reference to the widget that will display the text
        message (str) the message that is to be displayed
        error (bool) if True text is displayed with red
        susses (bool) if True, text is displayed with green
    Returns:
        None
    """
    widget["foreground"] = "black"
    if error:
        widget["foreground"] = "red"
    elif susses:
        widget["foreground"] = "green"
    widget["text"] = message
