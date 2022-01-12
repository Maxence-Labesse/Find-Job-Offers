from tkinter import *
import tkinter.ttk as ttk
import pandas as pd
from tkinter import filedialog

root = Tk()
df = pd.DataFrame.from_dict({"A": [1, 2], "B": [2, 3]})
print(df)


def getFolderPath():
    folder_selected = filedialog.askdirectory()
    folderPath.set(folder_selected)


def doStuff():
    folder = folderPath.get()
    df.to_excel(folder + "/output.xlsx")


folderPath = StringVar()
btnFind = ttk.Button(root, text="Browse Folder", command=getFolderPath)
btnFind.grid(row=0, column=2)

c = ttk.Button(root, text="find", command=doStuff)
c.grid(row=4, column=0)

mainloop()
