import Tkinter as tk

class CreateWindow:

    def __init__(self):
        self.window = tk.Tk()


    def set_title(self,title):
        self.window.title(title)

    def set_size(self,x,y):
        pass

    def get_parameter(self,parameter_type):

        if parameter_type=='str':
            pass

if __name__ == "__main__":

    app = CreateWindow()
    app.set_title('Beta')


    app.window.mainloop()