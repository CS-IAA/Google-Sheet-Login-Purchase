'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
#####
Ismail A Ahmed/Hanzala N Siddiqui
adminaccount.py
Version 4.0
'''
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo #popup
from passlib.hash import pbkdf2_sha256
import gspread
from oauth2client.service_account import ServiceAccountCredentials

global lst
lst = []
global lsttest
lsttest = []
global userlist
userlist = []

global lst2
lst2 = []
global lsttest2
lsttest2 = []
global userlist2
userlist2 = []

def next_available_row(worksheet): #next avilable row
    str_list = list(filter(None, worksheet.col_values(1)))  # fastest
    return str(len(str_list)+1)
def next_available_row2(worksheet2):
    str_list2 = list(filter(None, worksheet2.col_values(1)))  # fastest
    return str(len(str_list2)+1)

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_ADMIN.json', scope) #connects sheets with json file and allows usage with python
client = gspread.authorize(creds)
creds2 = ServiceAccountCredentials.from_json_keyfile_name('client_DAB.json', scope)
client2 = gspread.authorize(creds2)

# Find a workbook by name and open the first sheet
sheet = client.open("adminlist").sheet1
next_row = next_available_row(sheet)
sheet2 = client2.open("userlist").sheet1
next_row2 = next_available_row2(sheet2)


# Extract and print all of the values
list_of_hashes = sheet.get_all_records() #dictionary of all values in sheets
for x in list_of_hashes:
    lst.append(x['Username'] + ' '+ str(x['Password'])) #gets username/password from dictionary and adds to a list
list_of_hashes2 = sheet2.get_all_records()
for x in list_of_hashes2:
    lst2.append(x['Username'] + ' '+ str(x['Password']))

def second():
    window = Tk()  # new tkinter window opened
    window.title("Admin")  # title of new tiknter

    def goodhash2():
        global lst2
        global lsttest2
        for x in lst2: #goes through a encrypted list that contains username/password
            x = x.split(' ') #splits up the username/password into their own list and puts username as x[0] and pass as x[1]
            test1 = pbkdf2_sha256.verify(usern2.get(), x[0]) #checks to see if the username client entered matches encrypted version at x[0]
            userlist2.append(x[0])
            test2 = pbkdf2_sha256.verify(pasw2.get(), x[1]) #checks to see if the password client entered matches encrypted version at x[1]
            if test1 == True and test2 == True: #if both match, this means that the user exists, so do the following
                x[0] = usern2.get() #replace the encrypted username with the unencrypted username(the username the client entered)
                x[1] = pasw2.get()#replace the encrypted password with the unencrypted password(the password the client entered)
                xx = (x[0] + ' '+ x[1]) #now make the CORRECT username/password right next to each other but with a space seperating them, like it it originally was(albeit unencrpted)
                lsttest2.append(xx) #check comments in rd() function to see how this is useful
            else:  # look at foor loop that deosnt have the list(for x in z). this is what happens if the "x" is not the one
                xx = (x[0] + ' '+ x[1]) #restores the other username/passwords back to their original state before .split(' ')
                lsttest2.append(xx) #check comments in rd() function to see how this is useful

    def money_add():
        try:
            goodhash2()
            if len(userlist2) != 0:  # checks to see if sheets has users
                for i in userlist2:
                    test1 = pbkdf2_sha256.verify(usern2.get(),i)  # checks to see if the username client entered matches encrypted version at x[0]
                    betatest.append(test1)
            if usern2.get() != '' and money2.get() != '': #if user entered some value for username/money
                if True in betatest:
                    usercount = 2 #since first user is starting from row 2
                    if len(betatest) != 0:  # checks to see if sheets has users
                        for x in betatest:
                            if x == True: #if the user matches
                                print(usercount)
                                if int(money2.get()) >= 0: #to make sure that they don't dont a negative number
                                    userbalance = sheet2.cell(usercount, 3).value  # row,column
                                    userbalance = int(userbalance)
                                    userbalance += int(money2.get())
                                    sheet2.update_cell(usercount, 3, userbalance)  # row,column
                                    showinfo("Success", "You successfully added $"+money2.get()+".00!")
                                    usern2.set('')
                                    pasw2.set('')
                                    money2.set('')
                                    del lsttest2[:]
                                    del userlist2[:]
                                    del betatest[:]

                                else:
                                    showinfo("Error", "No negative money allowed!")  # popup
                                    del lsttest2[:]
                                    del userlist2[:]
                                    del betatest[:]

                            usercount += 1
                else:
                    showinfo("Error", "User does not exist!")
                    usern2.set('')
                    pasw2.set('')
                    money2.set('')
                    del lsttest2[:]
                    del userlist2[:]
                    del betatest[:]

            else:
                showinfo("Error", "Please enter both the username and money!")  # popup
                del lsttest2[:]
                del userlist2[:]
                del betatest[:]

        except ValueError: #if they leave the money field blank, leters in money field
            showinfo("Error", "Please make sure to enter the money and that it is in an integer in numerical form.")  # popup
            del lsttest2[:]
            del userlist2[:]
            del betatest[:]
        except TclError: #if they leave the money field blank, leters in money field
            showinfo("Error", "Please enter both the username and money. Make sure the money is in numerical form.")  # popup
            del lsttest2[:]
            del userlist2[:]
            del betatest[:]



    betatest = []

    def createup():
        try:
            if (usern2.get() == '' or pasw2.get() == ''):
                # makes sure there is entry in both username/password/money
                showinfo("Error", "Please enter the username, password and money!")  # popup
                del lsttest2[:]
                del userlist2[:]
                del betatest[:]

            else:
                if int(money2.get()) >= 0: #to make sure that they don't dont a negative number
                    goodhash2()
                    if len(userlist2) != 0:  # checks to see if sheets has users
                        for x in userlist2:
                            test1 = pbkdf2_sha256.verify(usern2.get(),x)  # checks to see if the username client entered matches encrypted version at x[0]
                            betatest.append(test1)
                        letup()
                    else:
                        letup()
                else:
                    showinfo("Error", "No negative money allowed!")  # popup
                    del lsttest2[:]
                    del userlist2[:]
                    del betatest[:]

        except ValueError:
            showinfo("Error", "Please make sure to enter the money and that it is in an integer in numerical form!")  # popup
            del lsttest2[:]
            del userlist2[:]
            del betatest[:]

        except TclError: #if they leave the money field blank
            showinfo("Error", "Please enter the username, password and money. Make sure the money is in numerical form.")  # popup
            del lsttest2[:]
            del userlist2[:]
            del betatest[:]


    def letup():
        if True in betatest:
            showinfo("Error", "Sorry, but that user already exists. Please try again!")
            usern2.set('')
            pasw2.set('')
            money2.set('')
            del lsttest2[:]
            del userlist2[:]
            del betatest[:]

        else:
            hashusr = pbkdf2_sha256.hash(usern2.get())  # encrypts what the user inputs
            hashpsw = pbkdf2_sha256.hash(pasw2.get())  # encrypts what the user inputs
            sheet2.update_acell("A{}".format(next_row2), hashusr)
            sheet2.update_acell("B{}".format(next_row2), hashpsw)
            sheet2.update_acell("C{}".format(next_row2), money2.get())

            showinfo("Success","New user created!")  # tells user how the code successfully managed to encrypt the username/password like it was supposed to
            usern2.set('')
            pasw2.set('')
            money2.set('')
            del lsttest2[:]
            del userlist2[:]
            del betatest[:]
            del lst2[:] #does this otherwise it would look at the original list of users when the program ran, which would not included removed/added users
            list_of_hashes2 = sheet2.get_all_records()
            for x in list_of_hashes2:
                lst2.append(x['Username'] + ' ' + str(x['Password']))

    def getout(): #removing the user
        goodhash2()
        if len(userlist2) != 0:  # checks to see if sheets has users
            for i in userlist2:
                test1 = pbkdf2_sha256.verify(usern2.get(),i)  # checks to see if the username client entered matches encrypted version at x[0]
                betatest.append(test1)
        if usern2.get() == '':
            showinfo("Error", "Please enter the username!")  # popup
            del lsttest2[:]
            del userlist2[:]
            del betatest[:]
        elif True in betatest:
            usercount=2
            if len(betatest) != 0:  # checks to see if sheets has users
                for x in betatest:
                    if x==True:
                        sheet2.delete_row(usercount)
                        showinfo("Success", "User removed!")
                        usern2.set('')
                        pasw2.set('')
                        money2.set('')
                        del lsttest2[:]
                        del userlist2[:]
                        del betatest[:]
                        del lst2[:] #does this otherwise it would look at the original list of users when the program ran, which would not included removed/added users
                        list_of_hashes2 = sheet2.get_all_records()
                        for x in list_of_hashes2:
                            lst2.append(x['Username'] + ' ' + str(x['Password']))

                    usercount+=1
        else:
            showinfo("Error", "User does not exist!")
            usern2.set('')
            pasw2.set('')
            money2.set('')
            del lsttest2[:]
            del userlist2[:]
            del betatest[:]

    usern2 = StringVar()
    pasw2 = StringVar()
    money2 = StringVar()

    mainframe2 = ttk.Frame(window, padding="5 10")
    mainframe2.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe2.columnconfigure(0, weight=1)
    mainframe2.rowconfigure(0, weight=1)

    userN2 = ttk.Entry(mainframe2, width=25, textvariable=usern2)
    userN2.grid(column=2, row=2, sticky=(W, E))
    paswN2 = ttk.Entry(mainframe2, width=25, textvariable=pasw2, show="*")
    paswN2.grid(column=2, row=3, sticky=(W, E))
    moneyN2 = ttk.Entry(mainframe2, width=25, textvariable=money2)
    moneyN2.grid(column=2, row=4, sticky=(W, E))

    ttk.Label(mainframe2, text="Account", font=("", 15)).grid(column=1, row=1, sticky=W)
    ttk.Label(mainframe2, text=" Username ").grid(column=1, row=2, sticky=W)
    ttk.Label(mainframe2, text=" Password  ").grid(column=1, row=3, sticky=W)
    ttk.Label(mainframe2, text=" Money").grid(column=1, row=4, sticky=W)

    ttk.Button(mainframe2, text="Remove", command = getout).grid(column=1, row=5, sticky=(W))
    ttk.Button(mainframe2, text="Create", command = createup).grid(column=2, row=5, sticky=(N,W))
    ttk.Button(mainframe2, text="Add", command = money_add).grid(column=2, row=5, sticky=(N,E))
    window.resizable(False, False) #makes it so that neither side of the window can be stretched

    for child in mainframe2.winfo_children(): child.grid_configure(padx=5, pady=5)

    window.mainloop()

def begin():
    root = Tk()
    root.title("Admin")

    def goodhash():
        global lst
        global lsttest
        for x in lst:  # goes through a encrypted list that contains username/password
            x = x.split(' ')  # splits up the username/password into their own list and puts username as x[0] and pass as x[1]
            test1 = pbkdf2_sha256.verify(usern.get(), x[0])  # checks to see if the username client entered matches encrypted version at x[0]
            userlist.append(x[0])
            test2 = pbkdf2_sha256.verify(pasw.get(), x[1])  # checks to see if the password client entered matches encrypted version at x[1]
            if test1 == True and test2 == True:  # if both match, this means that the user exists, so do the following
                x[0] = usern.get()  # replace the encrypted username with the unencrypted username(the username the client entered)
                x[1] = pasw.get()  # replace the encrypted password with the unencrypted password(the password the client entered)
                xx = (x[0] + ' ' + x[1])  # now make the CORRECT username/password right next to each other but with a space seperating them, like it it originally was(albeit unencrpted)
                lsttest.append(xx)  # check comments in rd() function to see how this is useful
            else:  # look at foor loop that deosnt have the list(for x in z). this is what happens if the "x" is not the one
                xx = (x[0] + ' ' + x[1])  # restores the other username/passwords back to their original state before .split(' ')
                lsttest.append(xx)  # check comments in rd() function to see how this is useful

    def rd():
        if (usern.get() == '' or pasw.get() == ''):  # makes sure there is entry in both username/password
            showinfo("Error", "Please enter both the username and password!")  # popup
        else:
            goodhash()  # takes to function that finds the matching login info and makes it so that can use the if statment below
            file = (
            usern.get() + ' ' + pasw.get())  # gets the username and password client entered and adds space in between like in lsttest list
            if file in lsttest:  # checks to see if what the client entered is in lsttest list
                showinfo("Success", "Logged in!")
                root.destroy()
                second()

            else:  # look at foor loop that deosnt have the list(for x in z). this is what happens if the "x" is not the one
                showinfo("Error", "Incorrect username or password!")

    mainframe = ttk.Frame(root, padding="5 10")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    usern = StringVar() #variable that stores username
    pasw = StringVar() #variable that stores the password
    result = StringVar() #variable that stores the result
    money = StringVar() #variable that stores the money

    userna = ttk.Entry(mainframe, width=25, textvariable=usern)
    userna.grid(column=2, row=2, sticky=(W, E))
    paswo = ttk.Entry(mainframe, width=25, textvariable=pasw, show="*")
    paswo.grid(column=2, row=3, sticky=(W, E))

    nameu = ttk.Label(mainframe, text="Login", font = ("", 15)).grid(column=1, row=1, sticky=W)
    wordp = ttk.Label(mainframe, text=" Username ").grid(column=1, row=2, sticky=W)
    ttk.Label(mainframe, text=" Password  ").grid(column=1, row=3, sticky=W)

    ttk.Label(mainframe, textvariable=result).grid(column=1, row=4, sticky=(W))#testing
    ttk.Button(mainframe, text="Login", command = rd).grid(column=2, row=4, sticky=(N,E))

    root.resizable(False, False) #makes it so that neither side of the window can be stretched

    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    userna.focus()
    paswo.focus()

    root.mainloop()
begin()