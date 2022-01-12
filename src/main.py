"""This is the main script of the job offers collecting software

"""
from src.utils.app_front import open_app


def main():
    root = open_app()
    root.mainloop()


if __name__ == "__main__":
    main()
