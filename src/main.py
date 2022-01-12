"""This is the main script of the job offers collecting software

"""
import argparse
from src.utils.app_front import open_app


def main(args):
    root = open_app(time_between_requests=args.time_between_offers)
    root.mainloop()


parser = argparse.ArgumentParser()
parser.add_argument('time_between_offers', nargs='?', const=False, type=bool)
args = parser.parse_args()

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)  # call the default function
