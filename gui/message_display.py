from tkinter import Frame, Label


class MessageDisplay(Frame):

    def __init__(self, font: str) -> None:
        super().__init__()
        self.text_output_field = Label(self, font=(font, 18),
                                       wraplength=750)

        self.text_output_field.grid(row=0, column=0)

    @staticmethod
    def progress_tracker(curr_iteration: int, total_iterations: int) -> str:
        """Formats the progress as a text
        Returns:
            str: A formatted text representing the progress
        """
        # percent = (curr_iteration / total_iterations) * 100
        return f"({curr_iteration} out of {total_iterations})"

    def display_text(self, text: str, color: str = "black") -> None:
        """Changes the text of the widget to display a message.
        Args:
            text: (str) the text that will be displayed on the widget
            color: (str) the color of the above text
        """
        self.text_output_field["foreground"] = color
        self.text_output_field["text"] = text
        self.text_output_field.update()
