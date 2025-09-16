import logging
from .ui.login import LoginWindow
from .database import init_db

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    filename="ac_workshop.log")

def main():
    init_db()
    LoginWindow().mainloop()


if __name__ == "__main__":
    main()
