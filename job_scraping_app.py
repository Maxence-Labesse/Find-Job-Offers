from indeed_scraping import *
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox

# First widget: global window
root = Tk()
root.title("Find job offers app")
style = ttk.Style()
style.theme_use('clam')
root.geometry('300x120')


def submit():
    keyword = keyword_entry.get()
    depth = depth_entry.get()
    captcha = job_scraping(keyword, int(depth))
    print(captcha)
    if captcha:
        messagebox.showerror(title="Captcha limit", message="You should wait some times before using the app :)",
                             )
        root.destroy()
    else:
        messagebox.showinfo(title="All good", message="You can find job offers in Excel file")
        root.destry()


keyword_label = Label(root, text="Key Word")
keyword_label.grid(row=0, column=0, pady=(10, 0))
keyword_entry = Entry(root, width=30)
keyword_entry.grid(row=0, column=1, padx=20, pady=(10, 0))

depth_label = Label(root, text="Depth")
depth_label.grid(row=1, column=0, pady=(10, 0))
depth_entry = Entry(root, width=30)
depth_entry.grid(row=1, column=1, padx=20, pady=(10, 0))

# Create Submit Button
Submit_btn = Button(root, text="Get job offers", command=submit)
Submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

root.mainloop()
