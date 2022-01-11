from indeed_scraping import *
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox


def submit():
    """
    when "Get job offers" button is pressed, scrape data according to keyword and period filled by user
    Display a messagebox to notify if scraping succeeded or got blocked by captch
    """
    # get keyword and period filled by user
    keyword = keyword_entry.get()
    depth = depth_corres[var.get()]
    # Scrape offers informations
    captcha = scrape_offers(keyword, int(depth))
    # Notify scraping success or failure
    if captcha:
        messagebox.showerror(title="Captcha limit", message="You should wait some times before using the app :)",
                             )
        root.destroy()
    else:
        messagebox.showinfo(title="All good", message="You can find job offers in Excel file")
        root.destroy()


# Window global settings
root = Tk()
root.title("Find job offers")
style = ttk.Style()
style.theme_use('clam')
root.geometry('300x120')

# keyword label and entry
keyword_label = Label(root, text="Key Word:")
keyword_label.grid(row=0, column=0, pady=(10, 0))
keyword_entry = Entry(root, width=30)
keyword_entry.grid(row=0, column=1, padx=20, pady=(10, 0))

# period options
period_options = ["Today", "1 day ago", "2 days ago", "3 days ago"]
depth_corres = dict(zip(period_options, [0, 1, 2, 3]))
var = StringVar()
var.set(period_options[0])
# period label and dropdown
period_label = Label(root, text="Since:")
period_label.grid(row=1, column=0, pady=(10, 0))
period_dropdown = ttk.Combobox(root, textvariable=var)
period_dropdown['values'] = period_options
period_dropdown['state'] = 'readonly'
period_dropdown.grid(row=1, column=1, padx=20, pady=(10, 0), ipadx=22)

# submit button
Submit_btn = Button(root, text="Get job offers", command=submit)
Submit_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

root.mainloop()
