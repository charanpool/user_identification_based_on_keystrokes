__author__ = 'skoppuravuri'
import threading

from tkinter import *
from tkinter import messagebox
from tkinter import font
#from tkinter.ttk import *
import tkinter.ttk as ttk
import main_final
import pandas as pd
from pynput.keyboard import Key, Controller
import os
import csv
import random
#from pynput import keyboard
import authenticate

keyboard = Controller()

#print sample
row = ['name', 'e', 'a', 'r', 'i', 'o', 't', 'n', 's', 'h', 'l','d','g','space','in', 'th', 'ti', 'on', 'an', 'he', 'al', 'er','es','the',\
       'and','are','ion','ing','in_DD','th_DD','ti_DD','on_DD','an_DD','he_DD','al_DD','er_DD','es_DD','input_rate']

if (not os.path.exists("reg_dataset.csv")):
    fp = open("reg_dataset.csv","w",newline='\n')
    writer = csv.writer(fp)
    writer.writerow(row)
    fp.close()
registered_data = pd.read_csv(".\\reg_dataset.csv")
reg_user_names = list(registered_data['name'])
print(reg_user_names)
#print(main_final.user)

para1_1 = "The Moon is a barren, rocky world without air and water.The Moon keeps changing its shape as it moves round the Earth. The Moon's apparent size in the sky is almost the same as that of the Sun."
para1_2 = "The Sun is the star at the center of the Solar System.The synodic rotation of Earth and its orbit around the Sun are the basis of solar calendars.The Sun is actually emitting more photons in the green portion of the spectrum."
para1_3 = "The Solar System consists of the Sun, Moon and Planets.In order of distance from the Sun, the planets are Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune and Pluto."
para2_1 = "The Ramayana is a story of Lord Rama written by the Sage Valmiki.It follows his fourteen-year exile to the forest by his father King Dasharatha.He travels across forests in India with his wife Sita and brother Lakshmana."
para2_2 = "Unaware of her guest's plan, Sita is tricked into leaving the rekha and is then forcibly carried away by Ravana. Meanwhile, Rama and Lakshmana learn about Sita's abduction from Jatayu and immediately set out to save her."
para2_3 = "The war ends when Rama kills Ravana. Rama then installs Vibhishana on the throne of Lanka. The episode of Agni Pariksha varies in the versions of Ramayana by Valmiki and Tulsidas."
para3_1 = "The Taj Mahal is a beautiful monument built by Shah Jahan in memory of his wife Mumtaz Mahal. The Taj Mahal attracts 7-8 million visitors a year and in 2007, it was declared a winner of the New7Wonders of the World."
para3_2 = "Machu Picchu was built in the classical Inca style, with polished dry-stone walls. Its three primary structures are the Intihuatana, the Temple of the Sun, and the Room of the Three Windows."
para3_3 = "The Great Wall of China is a series of fortifications made of stone, brick, tamped earth, wood, and other materials, generally built along an east-to-west line across the historical northern borders of China."

#print(len(para1), len(para2), len(para3))

currEntry = None
currLabel = None
currThread = None
warning_label = None
name = None
para_count = 0      #which para to display
next_count = 0      #which para to consider paralelly
paraSetSelect = None
paraArr = [[para1_1, para1_2, para1_3],[para2_1, para2_2, para2_3],[para3_1, para3_2, para3_3]]
regWindow = None
valWindow = None

def registerCall():
    global registerButton
    global currEntry
    global currLabel
    global currThread
    global regWindow
    global paraSetSelect
    global reg_user_names
    global registered_data
    paraSetSelect = random.randint(0,2)

    registered_data = pd.read_csv(".\\reg_dataset.csv")
    reg_user_names = list(registered_data['name'])

    print("registration")
    #registerButton['state'] = 'disabled'
    #if regWindow is not None:
        #return
    regWindow = Toplevel(rootWindow)
    regWindow.title("Registration")
    regWindow.geometry("350x170+450+200")
    regWindow.grab_set()

    #confirming that no thread is in running state at registration start
    if currThread is not None:
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)
        currThread.join()

    userLabel = Label(regWindow, text="Enter your name :", font=("Hevitica", 10), foreground='#1E5878')
    #userLabel.grid(row=1, column=2, columnspan=4)
    userLabel.place(x=50, y=40)

    userEntry = Entry(regWindow, foreground='#003366')
    #userEntry.grid(row=1, column=7)
    userEntry.place(x=160, y=40)

    para_count = 0
    max_para_count = 3
    paraImage1_1 = PhotoImage(file=".\\paraImages\\1_1.png")
    paraImage1_2 = PhotoImage(file=".\\paraImages\\1_2.png")
    paraImage1_3 = PhotoImage(file=".\\paraImages\\1_3.png")
    paraImage2_1 = PhotoImage(file=".\\paraImages\\2_1.png")
    paraImage2_2 = PhotoImage(file=".\\paraImages\\2_2.png")
    paraImage2_3 = PhotoImage(file=".\\paraImages\\2_3.png")
    paraImage3_1 = PhotoImage(file=".\\paraImages\\3_1.png")
    paraImage3_2 = PhotoImage(file=".\\paraImages\\3_2.png")
    paraImage3_3 = PhotoImage(file=".\\paraImages\\3_3.png")
    paraArray = [[paraImage1_1, paraImage1_2, paraImage1_3], [paraImage2_1, paraImage2_2, paraImage2_3],[paraImage3_1, paraImage3_2, paraImage3_3]]

    def trainUser():
        #expanding windowsize
        #regWindow.geometry("500x500")
        global para_count
        global currEntry
        global currLabel
        global currThread
        global next_count
        global registerButton
        print("#####################",next_count, para_count, "#####################")
        #if next_count != 0:
            #keyboard.release(Key.esc)
        print("Next Pressed")
        #main_final.run(True, main_final.user+"_"+str(next_count))
        #if currThread is not None:
            #currThread.join()

        #para verification
        print(len(paraArr[paraSetSelect][para_count]))
        print(len(currEntry.get("1.0", "end-1c")))
        if(len(currEntry.get("1.0", "end-1c")) in range(len(paraArr[paraSetSelect][para_count])-25, len(paraArr[paraSetSelect][para_count])+25)): #passed
            currEntry.destroy()
            currLabel.destroy()
            keyboard.press(Key.esc)
            keyboard.release(Key.esc)
            para_count += 1
            next_count += 1
            main_final.user_rep = name+"_"+str(next_count)
            if(para_count >= max_para_count):
                keyboard.press(Key.esc)
                keyboard.release(Key.esc)
                currThread.join()

                userLabel.destroy()
                userEntry.destroy()
                currLabel.destroy()
                currEntry.destroy()
                regWindow.geometry("300x150+550+280")
                def destroy_reg():
                    regWindow.destroy()
                registeredLabel = Label(regWindow, text="You are successfully registered", font='Helvetica 12 bold', foreground='#1E5878')
                registeredLabel.place(x=35, y=34)
                finalOkButton = ttk.Button(regWindow, text="Home", command=destroy_reg, style='TButton')
                finalOkButton.place(x=100, y=80)

                #regWindow.destroy()
                #regWindow = None
                registerButton['state'] = 'enabled'
                messagebox.showinfo("Registration Complete", "You have successfully registered")

                return
            else:
                tempLabel = Label(regWindow, image=paraArray[paraSetSelect][para_count])
                #tempLabel.grid(row=3, column=1, columnspan=10)
                tempLabel.place(x=40, y=90)
                currLabel = tempLabel

                #tempEntry = Entry(regWindow)
                #tempEntry.grid(row=5, column=1, columnspan=10)
                tempEntry = Text(regWindow, height=5, width=52, foreground='#003366')
                tempEntry.place(x=50, y=200)
                currEntry = tempEntry
                #next_count += 1
                #main_final.user_rep = name+"_"+str(next_count)
                main_registration_thread = threading.Thread(target=main_final.run)
                currThread = main_registration_thread
                main_registration_thread.start()

        else:
            messagebox.showwarning("Warning!", "Please complete atleast 70% of the para")
            #next_count -= 1
            #trainUser()
            return

    def verifyUserId():
        global currLabel
        global currEntry
        global currThread
        global next_count
        global para_count
        global reg_user_names
        global name
        global warning_label
        para_count = 0
        next_count = 0
        #warning_label = None
        print(userEntry.get())
        if(len(userEntry.get()) == 0):
            if warning_label is not None:
                warning_label.destroy()
            warning_label = Label(regWindow,text="Please enter the name", font='Helvetica 9 italic', foreground='red')
            warning_label.place(x=93, y=18)
        elif(userEntry.get()+"_1" in reg_user_names):
            if warning_label is not None:
                warning_label.destroy()
            warning_label = Label(regWindow,text="This username already exists", font='Helvetica 9 italic', foreground='red')
            warning_label.place(x=92, y=18)
        else:
            name = userEntry.get()
            if warning_label is not None:
                warning_label.destroy()
            reg_user_names.append(userEntry.get())
            userEntry.config(state='disabled')
            main_final.user = userEntry.get()
            main_final.registration = True
            #main_final.run(True, main_final.user)

            print(name, " is registered successfully")
            #print(preArr)

            #killing continue button
            continueRegButton.destroy()

            regWindow.geometry("520x400")

            paraLabel_1 = Label(regWindow, image=paraArray[paraSetSelect][para_count])
            #paraLabel_1.grid(row=3, column=1, columnspan=10)
            paraLabel_1.place(x=40,y=90)
            currLabel = paraLabel_1

            #paraEntry_1 = Entry(regWindow, width=30)
            #paraEntry_1.grid(row=5, column=1, columnspan=10)
            paraEntry_1 = Text(regWindow, height=5, width=52, foreground='#003366')
            paraEntry_1.place(x=50, y=200)
            currEntry = paraEntry_1

            #Calling training method
            #trainUser()

            #nexParaButton = Button(regWindow, text = "Next", command=trainUser, font=('Hevitica', 10))
            nexParaButton = ttk.Button(regWindow, text = "Next", command=trainUser, style='TButton')
            #nexParaButton.grid(row=7, column=6)
            nexParaButton.place(x=220, y=320)

            #main_final.run(True, main_final.user+"_0")
            main_final.user_rep = name+"_"+str(next_count)
            print(main_final.user_rep)
            #next_count += 1
            keyboard.press(Key.esc)
            keyboard.release(Key.esc)
            main_registration_thread = threading.Thread(target=main_final.run)
            currThread = main_registration_thread
            main_registration_thread.start()

    #continueRegButton = Button(regWindow, text="Continue", command=verifyUserId, font=('Hevitica', 10))
    continueRegButton = ttk.Button(regWindow, text="Continue", command=verifyUserId, style='TButton')
    #continueRegButton.grid(row=3, column=6, columnspan=3)
    continueRegButton.place(x=130, y=90)

    print(userEntry.get())
    #regWindow.deiconify()
    regWindow.resizable(0, 0)
    regWindow.mainloop()


def validateCall():
    global validateButton
    global currThread
    global valWindow

    varSetSelect = random.randint(0,2)

    #validateButton['state'] = 'disabled'
    #if valWindow is not None:
        #return
    if currThread is not None:
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)
        currThread.join()

    valWindow = Toplevel(rootWindow)
    valWindow.title("Authentication")
    valWindow.geometry("500x300+400+200")
    valWindow.grab_set()
	
    valImage1 = PhotoImage(file=".\\paraImages\\v_1.png")
    valImage2 = PhotoImage(file=".\\paraImages\\v_2.png")
    valImage3 = PhotoImage(file=".\\paraImages\\v_3.png")
    valImageArr = [valImage1, valImage2, valImage3]
    #valImg = PhotoImage(file="C:\\Users\\skoppuravuri\\Desktop\\GUI_6\\v_1.png")

    valLabel = Label(valWindow, image=valImageArr[varSetSelect])
    valLabel.place(x=20,y=50)

    #valEntry = Entry(valWindow, width=70)
    valEntry = Text(valWindow, height=5, width=52, foreground='#003366')
    valEntry.place(x=25, y=150)

    def validateUser():
        global valWindow
        global validateButton
        #valWindow.destroy()
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)
        currThread.join()
        valLabel.destroy()
        valEntry.destroy()
        valWindow.geometry("300x150+550+280")
        #messagebox.showinfo("Result", "The user is : "+authenticate.result_user)
        #authenticate.authenticate_user.conc()

        def destroy_val():
            valWindow.destroy()

        if authenticate.tieFlag == 0:
            resLabel = Label(valWindow, text="User is : "+authenticate.result_user1, font='Helvetica 13 bold', foreground='#1E5878')
            resLabel.place(x=60, y=30)
        elif authenticate.tieFlag == 1:
            valWindow.geometry("350x150+550+280")
            resLabel = Label(valWindow, text="Probable users are : "+authenticate.result_user1+", "+authenticate.result_user2, font='Helvetica 13 bold', foreground='#1E5878')
            resLabel.place(x=50, y=30)
            authenticate.tieFlag = 0
        elif authenticate.tieFlag == 2:
            valWindow.geometry("380x150+550+280")
            resLabel = Label(valWindow, text="Probable users are : "+authenticate.result_user1+", "+authenticate.result_user2+", "+authenticate.result_user3, font='Helvetica 13 bold', foreground='#1E5878')
            resLabel.place(x=50, y=30)
            authenticate.tieFlag = 0
        finalOkButton = ttk.Button(valWindow, text="Home", command=destroy_val, style='TButton')
        finalOkButton.place(x=100, y=80)
        #main_final.main_thread.join()
        #validateButton['state'] = 'disabled'
        #dialog window to show result
        #try:
            #messagebox.showinfo("Result", "The user is : ")
        #except BaseException as e:
            #print(e)

        #valWindow.destroy()
        #validateButton['state'] = 'enabled'

		
    finalButton = ttk.Button(valWindow, text="OK", style='TButton', command=validateUser)#font=("Hevitica", 10), width=5)
    finalButton.place(x=190, y=250)

    #keyboard.press(Key.esc)
    #keyboard.release(Key.esc)
    main_final.registration = False
    validation_thread = threading.Thread(target=main_final.run)
    currThread = validation_thread
    validation_thread.start()

    valWindow.resizable(0,0)
    valWindow.mainloop()


rootWindow = Tk()
rootWindow.title("User Identification")
rootWindow.configure(background="white")

#button configuration
style = ttk.Style()
style.configure('TButton', font = ('Helvetica', 13, 'bold'), foreground = '#003366')

mainLabelFont = font.Font(family='Helvetica', size=12, weight='bold')
label = Label(rootWindow, text="Welcome! ", width=50, height=2, font=mainLabelFont, foreground='#1E5878')
#label.config(font=("times new roman", 13))
label.place(x=45, y=30)

regButtonFont = font.Font(family='Helvetica', size=10, weight='bold')
#registerButton = ttk.Button(rootWindow, text="Register", bd='2', command=registerCall, style = 'TButton')#font=regButtonFont, width=9)
registerButton = ttk.Button(rootWindow, text="Register", command=registerCall, style='TButton')#font=regButtonFont, width=9)
#registerButton.grid(row=3, column=1)
registerButton.place(x=180, y=100)

#validateButton = Button(rootWindow, text="Validate", bd='2', command=validateCall, font=regButtonFont, width=9)
validateButton = ttk.Button(rootWindow, text="Authenticate", command=validateCall, style='TButton')#font=regButtonFont, width=9)
#validateButton.grid(row=3, column=5)
validateButton.place(x=300, y=100)

rootWindow.grab_set()
rootWindow.resizable(0, 0)
rootWindow.geometry("600x200+350+250")
rootWindow.mainloop()