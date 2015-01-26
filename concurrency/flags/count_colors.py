import tkinter

class Test:
    def __init__(self, master):

        canvas = tkinter.Canvas(master)

        canvas.image = tkinter.PhotoImage(file = 'img/br.gif')
        print(vars(canvas.image))

        canvas.create_image(0,0, image=canvas.image, anchor=tkinter.NW)
        canvas.bind('<Button-2>', self.right_click)

        canvas.grid(row=0, column=0)

    def right_click(self, event):
        print(vars(event))
        raise SystemExit()

root = tkinter.Tk()
test = Test(root)
root.mainloop()
