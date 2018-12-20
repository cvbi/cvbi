import Tkinter as tk
import tkFileDialog


def create_window_from_list(object_list, window_title='Select one', w=500, h=800):
    """
    Create a selection window from provided list

    :param object_list: List to create a button selector
    :param window_title: Window title
    :param w: width of the window, default = 500
    :param h: height of the window, default = 800

    :return: Creates a window
    """

    window = tk.Tk()
    window.title(window_title)
    window.geometry(str(w)+"x"+str(h))

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


def create_input_window(default='0', window_title='Provide input', w=400, h=200, window_text=None, valid_range=None):
    """
    Create a selection window from provided list

    :param default: Default value
    :param window_title: Title of the window
    :param w: width of the window, default = 200
    :param h: height of the window, default = 200
    :param window_text: Text to be shown for description
    :param valid_range: Valid range for input

    :return: Creates a window to get input value and returns a string
    """

    window = tk.Tk()
    window.title(window_title)
    window.geometry(str(w)+"x"+str(h))

    def close_window():
        """Close window"""
        window.destroy()

    value = tk.StringVar()
    value.set(default)
    value_entered = tk.Entry(window, textvariable=value, width=w-50, text='Input')
    value_entered.pack()

    closing_button = tk.Button(master=window, text='Input Complete', command=close_window)
    closing_button.pack()

    T = tk.Text(window, height=10, width=w)
    T.pack()

    if valid_range:
        val_min = valid_range[0]
        val_max = valid_range[-1]
        range_text = " For the above parameter, provide a valid value between \n{}".format([val_min, val_max])
    else:
        range_text = ' '

    if window_text:
        window_text = window_text + '\n' + range_text
    else:
        window_text = range_text
    T.insert(tk.END, window_text)

    window.mainloop()

    value_string = value.get()

    return(value_string)


def get_output_dir(window_title="Select Folder", w=200, h=200):
    """
    Get output directory for your file.

    :param window_title: Title of the window
    :param w: Width of the window
    :param h: Height of the window

    :return: Creates a window to get string output directory
    """

    def close_window():

        window.destroy()

    window = tk.Tk()
    window.title(window_title)
    window.geometry(str(w)+"x"+str(h))
    window.directory = tkFileDialog.askdirectory(initialdir="~", title=window_title)
    output_dir = window.directory

    closing_button = tk.Button(master=window, text='Directory Selection Complete', command=close_window)
    closing_button.pack()
    window.mainloop()

    return(output_dir)

