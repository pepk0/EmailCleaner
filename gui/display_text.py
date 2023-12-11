import tkinter as tk


def print_tw(widget: tk.Text, message: str, error=False,
             susses=False, clear=True) -> None:
    # set message color according to message type
    widget["foreground"] = "black"
    if error:
        widget["foreground"] = "red"
    elif susses:
        widget["foreground"] = "green"
    if clear:
        widget.delete("0.0", tk.END)
    widget.insert("0.0", message)


def print_pbar(iteration: int, total_iterations: int) -> str:
    singe_iteration_progress = 40 / total_iterations
    iteration_progress = iteration * singe_iteration_progress
    iteration_bars = int(iteration_progress // 1)
    leftover_progress = 40 - iteration_bars
    return (f"[{'=' * iteration_bars}{'  ' * leftover_progress}]"
            f" - ({iteration}/{total_iterations})")
