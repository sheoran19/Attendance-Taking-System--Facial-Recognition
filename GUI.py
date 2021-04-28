import Attendance
from Attendance import *
from tkinter import *
from PIL import ImageTk, Image

window = Tk()
window.geometry("600x450")
window.title("Attendance Taking System")
canvas = Canvas(window,width = 1000, height = 1000)

#icon


#background

image = ImageTk.PhotoImage(Image.open(r"C:\Users\djkde\PycharmProjects\Deepak_attend\student.png"))

canvas.create_image(0, 0, anchor = NW, image = image)
canvas.place(x = 50,y =0)




label1 = Label(window, text = "Attendance Taking System Using Face Recognition",relief = "solid",
               fg = "white", bg = "grey", font = ("ariel", 16, "bold"))
label1.pack()


#buttons

# automatic attendance

button1 = Button(window, text = "Automatic Attendance",command = popup_window, fg = "white",
                 bg = "brown", relief = GROOVE, font = ("ariel", 12, "bold"))
button1.place(x = 80, y = 80)


# manually fill attendance

button2 = Button(window, text = "Manually Fill Attendance",command = manually_window, fg = "white",
                 bg = "brown", relief = GROOVE, font = ("ariel", 12, "bold"))
button2.place(x = 350, y = 80)

# open sheet

button3 = Button(window, text = "View Monthly Stats",command = monthly_stats, fg = "white",
                 bg = "brown", relief = GROOVE, font = ("ariel", 12, "bold"))
button3.place(x = 230, y = 220)

# exit button

button4 = Button(window, text = "EXIT",command = exitcode , fg = "white", bg = "brown",
                 relief = GROOVE, font = ("ariel", 12, "bold"))
button4.place(x = 280, y = 350)





window.mainloop()