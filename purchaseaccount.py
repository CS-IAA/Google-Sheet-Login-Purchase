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
Ismail A Ahmed
loginGUI.py
Version 3.0
'''

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo #popup
import csv
import socket
import time
import passlib
from passlib.hash import pbkdf2_sha256
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))  # fastest
    return str(len(str_list)+1)


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_DAB.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("userlist").sheet1
next_row = next_available_row(sheet)

global lst
lst = []

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
for x in list_of_hashes:
    lst.append(x['Username'] + ' '+ str(x['Password']))

global lsttest
lsttest = []
global userlist
userlist = []


def goodhash():
    global lst
    global lsttest
    for x in lst: #goes through a encrypted list that contains username/password
        x = x.split(' ') #splits up the username/password into their own list and puts username as x[0] and pass as x[1]
        test1 = pbkdf2_sha256.verify(usern.get(), x[0]) #checks to see if the username client entered matches encrypted version at x[0]
        userlist.append(x[0])
        test2 = pbkdf2_sha256.verify(pasw.get(), x[1]) #checks to see if the password client entered matches encrypted version at x[1]
        if test1 == True and test2 == True: #if both match, this means that the user exists, so do the following
            x[0] = usern.get() #replace the encrypted username with the unencrypted username(the username the client entered)
            x[1] = pasw.get()#replace the encrypted password with the unencrypted password(the password the client entered)
            xx = (x[0] + ' '+ x[1]) #now make the CORRECT username/password right next to each other but with a space seperating them, like it it originally was(albeit unencrpted)
            lsttest.append(xx) #check comments in rd() function to see how this is useful
            #showinfo("Success", "Logged in!")
            #usern.set('')  # makes username empty
            #pasw.set('')  # makes password empty
            #break # look at the for loop that doesnt have the list. if 5 users and the 2nd one is the users, three...
            # ...others are not the ones requested. if dont have break it will say NOT FOUND under the else. this...
            # ...breaks it after the user is found and doesn't go any further
        else:  # look at foor loop that deosnt have the list(for x in z). this is what happens if the "x" is not the one
            xx = (x[0] + ' '+ x[1]) #restores the other username/passwords back to their original state before .split(' ')
            lsttest.append(xx) #check comments in rd() function to see how this is useful
            #showinfo("Error", "Incorrect username or password!")
            #usern.set('')  # makes username empty
            #pasw.set('')  # makes password empty
            # break

def rd():
    #this placed here so time checked everytime user clicked 'check' box, else user could start the program, let run for more than 10 minuutes, and still be allowed to search
    s = socket.socket()  # Create a socket object
    port = 12345  # Reserve a port for your service.
    host = '172.17.2.87'  # Get local machine name
    s.connect((host, port))
    file0 = s.recv(1024) #receives what server sent
    s.close  # Close the socket when done
    file0 = str(file0) #server time
    myfile = time.ctime(time.time())  # my time
    file0 = file0.strip('b').strip("'")  # gets rid of the trash
    min1 = file0[14:16] #server minute
    min2 = myfile[14:16] #client minute

    if int(min1) + 10 >= int(min2) and int(min1) - 10 <= int(min2): #has to be within 10 minutes of server time
        if int(min2) + 10 >= int(min1) and int(min2) - 10 <= int(min1): #has to be within 10 minutes of server time
            if (usern.get() == '' or pasw.get() == ''): # makes sure there is entry in both username/password
                showinfo("Error", "Please enter both the username and password!")  #popup
            else:
                goodhash() #takes to function that finds the matching login info and makes it so that can use the if statment below
                count=2
                file = (usern.get() + ' ' + pasw.get()) #gets the username and password client entered and adds space in between like in lsttest list
                if file not in lsttest:
                    showinfo("Error", "Incorrect username or password!")
                    usern.set('')
                    pasw.set('')

                else:
                    for x in lsttest:  #checks to see if what the client entered is in lsttest list

                        if x==file:
                            #print(count)
                            showinfo("Success", "Logged in!")
                            file = ('Username:'+ usern.get() + ' ' + 'Time:' + file0 + '\n')
                            userbalance=sheet.cell(count, 3).value
                            #print(type(userbalance))
                            userbalance=int(userbalance)
                            userbalance-=1
                            #row,column
                            if userbalance>0:
                                sheet.update_cell(count, 3, userbalance)
                                showinfo("Purchase Succsessful", "Your Balance is $"+str(userbalance)+".00!")
                            else:
                                showinfo("Purchase Failed", "Insufficient Credit!")
                            usern.set('')
                            pasw.set('')


                        count+=1

        else:
            showinfo("Error", "Please update your time!") #client/server NOT  within 10 minutes of client/server time
            usern.set('')  # makes username empty
            pasw.set('')  # makes password empty

    else:
        showinfo("Error", "Please update your time!") #client/server NOT  within 10 minutes of client/server time
        usern.set('')  # makes username empty
        pasw.set('')  # makes password empty
root = Tk()
root.title("Purchase")

mainframe = ttk.Frame(root, padding="5 10")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

usern = StringVar() #variable that stores username
pasw = StringVar() #variable that stores the password
result = StringVar() #variable that stores the result

userna = ttk.Entry(mainframe, width=25, textvariable=usern)
userna.grid(column=2, row=2, sticky=(W))
paswo = ttk.Entry(mainframe, width=25, textvariable=pasw, show="*")
paswo.grid(column=2, row=3, sticky=(W))

nameu = ttk.Label(mainframe, text="Purchase", font = ("", 12)).grid(column=1, row=1, sticky=E)
wordp = ttk.Label(mainframe, text="Username ").grid(column=1, row=2, sticky=(S,W))
ttk.Label(mainframe, text="Password  ").grid(column=1, row=3, sticky=(S,W))

ttk.Label(mainframe, textvariable=result).grid(column=1, row=4, sticky=(W))#testing
#ttk.Button(mainframe, text="Create", command = createup).grid(column=2, row=4, sticky=(N,W))
ttk.Button(mainframe, text="Purchase", command = rd).grid(column=2, row=4, sticky=(N,E))

root.resizable(False, False) #makes it so that neither side of the window can be stretched

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

userna.focus()
paswo.focus()

root.mainloop()
