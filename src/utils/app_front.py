""" This module provides functions to build the app interface

function
--------
open_app:
    open app interface
submit_offer_search:
    collect offers when button is pressed
"""
from src.utils.offers_scraping import collect_offers
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox

# days depth searching options
offers_depth_options = ["Today", "1 day ago", "2 days ago", "3 days ago"]
d_depth_days_nb = dict(zip(offers_depth_options, [0, 1, 2, 3]))


def open_app(time_between_requests):
    """build app interface

    this window contains a textfield for the job keyword to search
    and a dropdown menu for the days_depth options

    Parameters
    ----------
    time_between_requests: bool
        If True, wait a random time [2-3s] between webpage requests

    Returns
    -------
    root: tkinter.Tk
        built app
    """
    # Window global settings
    root = Tk()
    root.title("Find job offers")
    style = ttk.Style()
    style.theme_use('clam')
    root.geometry('300x120')

    # job to search label and entry
    job_label = Label(root, text="Key Word:")
    job_label.grid(row=0, column=0, pady=(10, 0))
    job_entry = Entry(root, width=30)
    job_entry.grid(row=0, column=1, padx=20, pady=(10, 0))

    # depth options, label and dropdown
    selected_depth = StringVar()
    selected_depth.set(offers_depth_options[0])
    # period label and dropdown
    period_label = Label(root, text="Since:")
    period_label.grid(row=1, column=0, pady=(10, 0))
    period_dropdown = ttk.Combobox(root, textvariable=selected_depth)
    period_dropdown['values'] = offers_depth_options
    period_dropdown['state'] = 'readonly'
    period_dropdown.grid(row=1, column=1, padx=20, pady=(10, 0), ipadx=22)

    # search submit button
    search_submit_btn = Button(root, text="Get job offers",
                               command=lambda: submit_offer_search(root, job_entry, selected_depth,
                                                                   time_between_requests))
    search_submit_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    return root


def submit_offer_search(root, job_to_search, selected_depth, time_between_requests):
    """when "Get job offers" button is pressed, scrape data according to
    job_searched and period filled by user.

    Display a messagebox to notify if scraping succeeded or got blocked
    by captch

    Parameters
    ----------
    root: tkinter.Tk
        inteface main window
    job_to_search:
    selected_depth

    Returns
    -------

    """
    # get job_searched and period filled by user
    job_to_search = job_to_search.get()
    days_depth = d_depth_days_nb[selected_depth.get()]
    # Scrape offers information
    request_got_blocked = collect_offers(job_to_search, int(days_depth), time_between_requests=time_between_requests)
    # Notify scraping success or failure
    if request_got_blocked:
        messagebox.showerror(title="Captcha limit", message="You should wait some times before using the app :)",
                             )
        root.destroy()
    else:

        messagebox.showinfo(title="All good", message="You can find job offers in Excel file")
        root.destroy()
