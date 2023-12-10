from gui.window import MainWindow
from src.auth import gmail_authenticate
from src.email_handler import get_user_email


def main() -> None:

    # run the main frame window
    root = MainWindow()
    root.mainloop()


if __name__ == "__main__":
    main()
