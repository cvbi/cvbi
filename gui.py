import Tkinter as tk
import tkFileDialog


def create_window_from_list(object_list, window_title='Select one'):

    window = tk.Tk()
    window.title(window_title)

    def close_window():
        """Close window"""
        window.destroy()

    object_select = tk.StringVar()
    object_select.set(object_list[0])

    tk.Label(window, textvariable=object_select).pack()

    for item in object_list:
        selection_button = tk.Radiobutton(window, text=item, variable=object_select, value=item)
        selection_button.pack()

    closing_button = tk.Button(master=window, text='Selection Complete', command=close_window)
    closing_button.pack()

    window.mainloop()

    object_string = object_select.get()

    return(object_string)


def get_output_dir(window_header="Select Folder"):

    def close_window():

        window.destroy()

    window = tk.Tk()
    window.dirpath = tkFileDialog.askdirectory(initialdir = "~", title = window_header)
    output_dir = window.dirpath

    closing_button = tk.Button(master=window, text='Selection Complete', command=close_window)
    closing_button.pack()
    window.mainloop()

    #output_dir = output_dir.replace(':','-')

    return output_dir

