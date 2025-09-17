import logging
from ac_workshop.ui.login import LoginWindow
from ac_workshop.database import init_db

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    filename="ac_workshop.log")

def main():
    init_db()
    LoginWindow().mainloop()


if __name__ == "__main__":
    main()
