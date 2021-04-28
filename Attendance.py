import os
from PIL import ImageTk, Image
import csv
import tensorflow as tf
from functools import partial
from tkinter import *
import numpy as np
import pandas as pd
import paramiko
from scp import SCPClient
import time
from sklearn.preprocessing import Normalizer
import mtcnn
from PIL import Image
from os import listdir
from os.path import isdir, isfile
from keras.models import load_model
import joblib
from datetime import date
from tkinter import messagebox

global model

model = tf.keras.models.load_model(r'C:\\Users\djkde\PycharmProjects\Deepak_attend\model\facenet_keras.h5', compile=False)     #loading te saved facenet model
print("model loaded")
in_encoder = Normalizer(norm='l2')


def Detect_face():  # extraction and recognition of face

    def Copy_Image(server, port, user, password):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server, port, user, password)
        scp = SCPClient(client.get_transport())
        scp.get("/home/pi/cam.jpg", local_path="C:/Users/Kunal/Desktop/image")
        scp.close()

    def Capture_Image(server, port, user, password):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server, port, user, password)
        stdin, cpu, stderr = client.exec_command("raspistill -o cam.jpg")

    def extract_face(filename, required_size=(160, 160)):  # extraction of face

        image = Image.open(filename)  # loading image from directory
        image = image.convert("RGB")

        pixels = np.asarray(image)

        detector = mtcnn.mtcnn.MTCNN()
        results = detector.detect_faces(pixels)  # detecting face using MTCNN Model

        x1, y1, width, height = results[0]['box']  # getting box coordinates
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height

        face = pixels[y1:y2, x1:x2]  # extracting face using those coordinates

        image = Image.fromarray(face)
        image = image.resize(required_size)
        face_array = np.asarray(image)  # converting image back to numpy array

        return face_array

    def get_face_embedding(face_pixels, model):  # getting the face embeddings using facenet model

        face_pixels = face_pixels.astype('float32')

        mean, std = face_pixels.mean(), face_pixels.std()  # normalizing the face pixels
        face_pixels = (face_pixels - mean) / std

        samples = np.expand_dims(face_pixels, axis=0)

        yhat = model.predict(samples)

        return yhat

    def face_predict(face_array, model_file_path):

        model_learn = joblib.load(model_file_path)

        y_predict_class = model_learn.predict(face_array)

        y_predict_prob = model_learn.predict_proba(face_array)

        return y_predict_class[0]

    def Red_led(server, port, user, password):

        client = paramiko.SSHClient()

        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(server, port, user, password)

        stdin, cpu, stderr = client.exec_command("python RED.py")

    def Green_led(server, port, user, password):

        client = paramiko.SSHClient()

        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(server, port, user, password)

        stdin, cpu, stderr = client.exec_command("python Green.py")

    Capture_Image("192.168.43.248", 22, "pi", "4489Dma3")

    time.sleep(7)

    Copy_Image("192.168.43.248", 22, "pi", "4489Dma3")

    time.sleep(3)
    print('image copied')
    face = extract_face("C:/Users/djkde/Desktop/image/cam.jpg")  # calling extract_face()

    face_embedding = get_face_embedding(face, model)  # calling get_face_embedding()

    face_arr = np.asarray(face_embedding)
    face_array = in_encoder.transform(face_arr)

    name = face_predict(face_array, r'C:\Users\djkde\PycharmProjects\Deepak_attend\model\Attendance_model.pkl')
    today = date.today()
    if not isfile(r'C:\Users\djkde\Desktop\file' + r'\y' + str(today.year) + r'\at' + str(today.month) + '_' + str(
            today.year) + '.csv'):
        f = open(r'C:\Users\djkde\Desktop\file' + r'\y' + str(today.year) + r'\at' + str(today.month) + '_' + str(
            today.year) + '.csv', "w")
        writer = csv.DictWriter(
            f, fieldnames=["AdmissionNo", "Name", "Date"])
        writer.writeheader()
        f.close()

    if name < 4:

        data = pd.read_csv(r'C:\Users\djkde\Desktop\file\y' + str(today.year) + r'\StudentDetails.csv')

        fieldnames = ['AdmissionNo', 'Name', 'Date']

        info = {'AdmissionNo': data.loc[name].AdmissionNo, 'Name': data.loc[name].Name, 'Date': today}

        with open(r'C:\Users\djkde\Desktop\file\y' + str(today.year) + r'\at' + str(today.month) + '_' + str(
                today.year) + '.csv', 'a', newline='') as csvfile:

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writerow(info)

        Green_led("192.168.43.248", 22, "pi", "4489Dma3")

        messagebox.showinfo("Attendance System", "Attendance of " + data['Name'][name] + " taken")

    else:
        Red_led("192.168.43.248", 22, "pi", "4489Dma3")
        messagebox.showinfo("Attendance System", "Another Face Detected")


# opens csv file

def open_file():
    os.startfile(r"C:\Users\djkde\Desktop\file\at.csv")


# opens capture window

def popup_window():
    window = Toplevel()
    window.title("Attendance Taking System")
    window.geometry("400x200")
    window.configure(background="grey")

    label = Label(window, text="Take Attendance", relief="solid", fg="white", bg="red",
                  font=("ariel", 16, "bold")).pack()

    button1 = Button(window, text="Capture", command=Detect_face, fg="white", bg="brown", relief=GROOVE,
                     font=("ariel", 12, "bold"))
    button1.place(x=160, y=100)

    exit_b = Button(window, text="Exit", command=window.destroy, fg="white", bg="brown", relief=GROOVE,
                    font=("ariel", 12, "bold"))
    exit_b.place(x=174, y=150)


# opens manually attendance window

def manually_window():
    def Red_led(server, port, user, password):

        client = paramiko.SSHClient()

        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(server, port, user, password)

        stdin, cpu, stderr = client.exec_command("python RED.py")

    def Green_led(server, port, user, password):

        client = paramiko.SSHClient()

        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(server, port, user, password)

        stdin, cpu, stderr = client.exec_command("python Green.py")

    def call_result(n1, n2):
        today = date.today()
        name = (n1.get())
        roll = (n2.get())
        name = str(name)
        roll = str(roll)

        if not isfile(r'C:\Users\djkde\Desktop\file\y' + str(today.year) + r'\at' + str(today.month) + '_' + str(
                today.year) + '.csv'):
            f = open(r'C:\Users\djkde\Desktop\file\y' + str(today.year) + r'\at' + str(today.month) + '_' + str(
                today.year) + '.csv', "w")
            writer = csv.DictWriter(
                f, fieldnames=["AdmissionNo", "Name", "Date"])
            writer.writeheader()
            f.close()

        data = pd.read_csv(r'C:\Users\djkde\Desktop\file\y' + str(today.year) + '\StudentDetails.csv')
        if roll in list(data['AdmissionNo']):

            fieldnames = ['AdmissionNo', 'Name', 'Date']

            info = {'AdmissionNo': roll, 'Name': data['Name'][data['AdmissionNo'] == roll][
                list(data['SNo.'][data['AdmissionNo'] == roll])[0]], 'Date': today}

            with open(r'C:\Users\djkde\Desktop\file' + r'\y' + str(today.year) + r'\at' + str(today.month) + '_' + str(
                    today.year) + '.csv', 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writerow(info)

            Green_led("192.168.43.248", 22, "pi", "4489Dma3")

            messagebox.showinfo("Attendance System", "Attendance of " + data['Name'][data['AdmissionNo'] == roll][
                list(data['SNo.'][data['AdmissionNo'] == roll])[0]] + " taken")
        else:

            Red_led("192.168.43.248", 22, "pi", "4489Dma3")
            messagebox.showinfo("Attendance System", "Wrong Admission No.!!!")

        return

    window = Toplevel()
    window.title("Attendance Taking System")
    window.geometry("600x450")
    window.configure(background="grey")

    number1 = StringVar()
    number2 = StringVar()

    label1 = Label(window, text="Manually Fill Attendance", relief="solid", fg="white", bg="red",
                   font=("ariel", 16, "bold")).pack()

    label2 = Label(window, text="Enter Name", width=15, height=1, fg="white", bg="blue2",
                   font=('times', 15, ' bold '))
    label2.place(x=70, y=100)

    label3 = Label(window, text="Enter Enrollment", width=15, height=1, fg="white", bg="blue2",
                   font=('times', 15, ' bold '))
    label3.place(x=70, y=200)

    entry_name = Entry(window, textvar=number1, width=15, fg="black", font=('times', 13, ' bold '))
    entry_name.place(x=350, y=105)

    entry_rollno = Entry(window, textvar=number2, width=15, fg="black", font=('times', 13, ' bold '))
    entry_rollno.place(x=350, y=200)

    call_result = partial(call_result, number1, number2)

    b1 = Button(window, text="Enter", command=call_result, width=10, height=1, fg="white", bg="blue2",
                font=('times', 12, ' bold '))
    b1.place(x=250, y=280)

    b2 = Button(window, text="Exit", command=window.destroy, width=10, height=1, fg="white", bg="blue2",
                font=('times', 12, ' bold '))
    b2.place(x=250, y=350)


def monthly_stats():
    today = date.today()


    def monthly(roll,m):


        if not isfile(r'C:\Users\djkde\Desktop\file' + r'\y' + str(today.year) + r'\at' + str(m) + '_' + str(
                today.year) + '.csv'):

            messagebox.showinfo("Attendance System", "File Not Found")

        else:

            data = pd.read_csv(r'C:\Users\djkde\Desktop\file\y' + str(today.year) + r'\at' + str(m) + '_' + str(today.year) + '.csv')
            admin_no = roll.get()
            admin = list(data['AdmissionNo'])
            cnt = admin.count(admin_no)


            label2 = Label(window, text="Total Attendance", width=15, height=1, fg="white", bg="blue2",
                              font=('times', 15, ' bold '))
            label2.place(x=20, y=220)

            label = Label(window,relief="solid", fg="black", bg="white",font=("ariel", 16, "bold"),
                            text = str(cnt))
            label.place(x = 250, y = 220)


    window = Toplevel()
    window.title("Attendance Taking System")
    window.geometry("400x400")
    window.configure(background="grey")

    var_month = StringVar()

    enroll = StringVar()

    label1 = Label(window, text="Monthly Enrollment", relief="solid", fg="white", bg="red",
                   font=("ariel", 16, "bold")).pack()

    label2 = Label(window, text="Choose Month", width=15, height=1, fg="white", bg="blue2",
                   font=('times', 15, ' bold '))
    label2.place(x=20, y=150)

    label3 = Label(window, text="Enter Enrollment", width=15, height=1, fg="white", bg="blue2",
                   font=('times', 15, ' bold '))
    label3.place(x=20, y=100)

    entry_enroll = Entry(window, textvar=enroll, width=15, fg="black", font=('times', 13, ' bold '))
    entry_enroll.place(x=250, y=100)

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
              "October", "November", "December"]

    droplist = OptionMenu(window, var_month, *months)
    var_month.set("Select Month")
    droplist.config(width=15)
    droplist.place(x=250, y=150)

    def button():

        mon = var_month.get()
        ind = months.index(mon)
        monthly(enroll, ind+1)



    b2 = Button(window, text="Enter", command=button, width=9, height=1, fg="white", bg="blue2",
                font=('times', 11, ' bold '))
    b2.place(x=160, y=280)

    b3 = Button(window, text="Exit", command=window.destroy, width=9, height=1, fg="white", bg="blue2",
                font=('times', 11, ' bold '))
    b3.place(x=160, y=320)


# exit gui

def exitcode():
    exit()

