import Tkinter as tk
import time

def create_window_for_multiple_selection(object_list, window_title='Select Atleast One', w=500, h=800):
    """
    Create a multiple selection window from provided list

    :param object_list: List to create a button selector
    :param window_title: Window title
    :param w: width of the window, default = 500
    :param h: height of the window, default = 800

    :return: Creates a window to select from multiple
    """

    window = tk.Tk()
    window.title(window_title)
    window.geometry(str(w)+"x"+str(h))

    values = {}
    for item in object_list:
        values[item] = tk.IntVar()
        selection_button = tk.Checkbutton(master=window, text=item, variable=values[item], onvalue=item, offvalue=0)
        selection_button.pack()

    closing_button = tk.Button(master=window, text='Selection Complete', command=window.destroy)
    closing_button.pack()

    window.mainloop()

    selection_list = [value.get() for key, value in values.iteritems() if value.get() != 0]
    return(selection_list)


if __name__ == "__main__":
    objects = range(1,6)
    selected = create_window_for_multiple_selection(objects)
    print(selected)
    time.sleep(2)
