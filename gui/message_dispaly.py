from tkinter import Frame, Label


class MessageDisplay(Frame):
    FONT = "Helvetica"

    def __init__(self) -> None:
        super().__init__()
        self.text_output_field = Label(self, font=(self.FONT, 18),
                                       wraplength=750)

        self.text_output_field.grid(row=0, column=0)

    @staticmethod
    def status_bar(curr_iteration: int, total_iterations: int) -> str:
        percent = (curr_iteration / total_iterations) * 100
        return f"{percent:.2f}%"

    def display_text(self, text: str, color: str = "black") -> None:
        self.text_output_field["foreground"] = color
        self.text_output_field["text"] = text
        self.text_output_field.update()
