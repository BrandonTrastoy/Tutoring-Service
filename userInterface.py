try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import StringVar
    from tkinter import font as tkfont
    from tkinter import *
    from tkcalendar import Calendar, DateEntry
    from backend import *
    
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2

# Reference for grid structure pythontutorial.net/tkinter/tkinter-frame/
# Need a way to refresh the list after a student or session is created.

class ApplicationStart(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Tutoring Tracker")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.geometry('600x520')
        self.resizable(1, 1)

        # Where all other frames are located in
        self.MainContainer = tk.Frame(self)
        self.MainContainer.pack(fill="both", expand=True, pady=10, padx=10)

        # Initializes a set of frames to choose from.
        self.frames = {}
        for F in (addStudent, addSession, updateInfo, studentInformation):
            page_name = F.__name__
            frame = F(parent=self.MainContainer, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew') #Sets each frame at the same location

        menuItems = tk.Menu(self)
        self.config(menu=menuItems)

        menuOptions = tk.Menu(menuItems)
        menuItems.add_cascade(label="Main Menu", menu=menuOptions)

        menuOptions.add_command(label="Add Student", command = lambda: self.show_frame("addStudent"))
        menuOptions.add_command(label="Add Session", command = lambda: self.show_frame("addSession"))
        menuOptions.add_command(label="Update Information", command = lambda: self.show_frame("updateInfo"))
        menuOptions.add_command(label="Student Information", command = lambda: self.show_frame("studentInformation"))

        self.show_frame("addStudent")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


#Validation Purposes
def callback(input):
    if input.isdigit():
        return True
    
    elif input == '.':
        return True
    
    else:
        return False



class addStudent(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="Add Student", font=controller.title_font)
        label.grid(column=0, row=0, padx=10, pady=10, columnspan=1)

        #Name
        nameLabel = ttk.Label(self, text='Name: ')
        nameLabel.grid(column=0, row=1, sticky='W', padx=10, pady=10)

        nameEntry = ttk.Entry(self)
        nameEntry.grid(column=1, row=1, pady=10, sticky='W')

        #Session Length
        sessionLabel = ttk.Label(self, text='Session Length: ')
        sessionLabel.grid(column=0, row=2, sticky='W', padx=10, pady=10)

        sessionEntry = ttk.Entry(self) 
        sessionEntry.grid(column=1, row=2, pady=10, sticky='W')


        #Date        
        dateLabel = ttk.Label(self, text='Date: ')
        dateLabel.grid(column=0, row=3, sticky='W', padx=10, pady=10)

        
        dateEntry = DateEntry(self,background= "magenta3", foreground= "white",bd=2)        
        dateEntry.grid(column=1, row=3, sticky='W', padx=10, pady=10)
        
        
        #Amount 
        amountLabel = ttk.Label(self, text='Amount: ')
        amountLabel.grid(column=0, row=4, sticky='W', padx=10, pady=10)

        amountEntry = ttk.Entry(self) 
        amountEntry.grid(column=1, row=4, pady=10, sticky='W')

        #Payment Status
        paymentLabel = ttk.Label(self, text='Payment Status: ')
        paymentLabel.grid(column=0, row=5, sticky='W', padx=10, pady=10)

        paymentEntry = ttk.Combobox(self, state='readonly')
        paymentEntry['values'] = [ 'Paid', 'Not Paid', 'Cancelled']
        paymentEntry.current(1)
        paymentEntry.grid(column=1, row=5, pady=10, sticky='W')

        #Validate Input
        reg = self.register(callback)
        sessionEntry.config(validate = "key",validatecommand =(reg, '%S'))
        amountEntry.config(validate = "key",validatecommand =(reg, '%S'))

        def getData ():  
            # This data needs to be verified before it is sent to the addStudentBackend
            array = [nameEntry.get(), int(sessionEntry.get()), dateEntry.get(), int(amountEntry.get()), paymentEntry.get()]
            addStudentBackend(array)
            messages1.config(text=array)

        button1 = ttk.Button(self, text='Create', command= getData)
        button1.grid(column=1, row=6, pady=10, sticky='w')

        messages = tk.LabelFrame(self, text='Messages:', width=300, height=100)
        messages.grid(column=0, row=7, pady=10, padx=10, columnspan=2)

        messages1 = ttk.Label(messages, text='Enter data in the fields above.', wraplength=250)
        messages1.place(x=10, y=10, anchor="w")

class addSession(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Add Session", font=controller.title_font)
        label.grid(column=0, row=0, padx=10, pady=10)

        def refreshSession():
            
            listOfNames = studentList()
            
            
            #Name
            nameLabel = ttk.Label(self, text='Select A Student: ')
            nameLabel.grid(column=0, row=1, sticky='W', padx=10, pady=10)

            nameList = ttk.Combobox(self, state='readonly')
            nameList['values'] = listOfNames
            nameList.current(0)
            nameList.grid(column=1, row=1, pady=10, sticky='W')
        
            #Session Length
            sessionLabel = ttk.Label(self, text='Session Length: ')
            sessionLabel.grid(column=0, row=2, sticky='W', padx=10, pady=10)

            sessionEntry = ttk.Entry(self) 
            sessionEntry.grid(column=1, row=2, pady=10, sticky='W')

            #Date
            dateLabel = ttk.Label(self, text='Date: ')
            dateLabel.grid(column=0, row=3, sticky='W', padx=10, pady=10)

        
            dateEntry = DateEntry(self,background= "magenta3", foreground= "white",bd=2)        
            dateEntry.grid(column=1, row=3, sticky='W', padx=10, pady=10)

            #Amount 
            amountLabel = ttk.Label(self, text='Amount: ')
            amountLabel.grid(column=0, row=4, sticky='W', padx=10, pady=10)

            amountEntry = ttk.Entry(self) 
            amountEntry.grid(column=1, row=4, pady=10, sticky='W')

            #Payment Status
            paymentLabel = ttk.Label(self, text='Payment Status: ')
            paymentLabel.grid(column=0, row=5, sticky='W', padx=10, pady=10)

            paymentEntry = ttk.Combobox(self, state='readonly')
            paymentEntry['values'] = [ 'Paid', 'Not Paid', 'Cancelled']
            paymentEntry.current(1)
            paymentEntry.grid(column=1, row=5, pady=10, sticky='W')

            #Validate Input
            reg = self.register(callback)
            sessionEntry.config(validate = "key",validatecommand =(reg, '%S'))
            amountEntry.config(validate = "key",validatecommand =(reg, '%S'))

            def getData ():  
                # This data needs to be verified before it is sent to the addStudentBackend
                array = [nameList.get(), int(sessionEntry.get()), dateEntry.get(), int(amountEntry.get()), paymentEntry.get()]
                addStudentBackend(array)
                messages1.config(text=array)

            button1 = ttk.Button(self, text='Create', command= getData)
            button1.grid(column=1, row=6, pady=10, sticky='w')

            messages = tk.LabelFrame(self, text='Messages:', width=300, height=100)
            messages.grid(column=0, row=7, pady=10, padx=10, columnspan=2)

            messages1 = ttk.Label(messages, text='Enter data in the fields above.', wraplength=250)
            messages1.place(x=10, y=10, anchor="w")

        refreshSession()
        refreshButton = ttk.Button(self, text='Refresh', command=lambda: refreshSession())
        refreshButton.grid(column=0, row=6, pady=10, sticky='w')

class updateInfo(tk.Frame):

    def openNewWindow(self, id):

        studentInformation = singleStudent(int(id))

        newWindow = tk.Toplevel(self)
        newWindow.title("Update Information")
        title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        newWindow.geometry("450x500")
        newWindow.resizable(0, 0)

        label = ttk.Label(newWindow, text="Update Session", font=title_font)
        label.grid(column=0, row=0, padx=10, pady=10, columnspan=1)

        #Name
        nameLabel = ttk.Label(newWindow, text='Name: ')
        nameLabel.grid(column=0, row=1, sticky='W', padx=10, pady=10)

        self.entryNameText = tk.StringVar()
        self.entryNameText.set(studentInformation[0])

        nameEntry = ttk.Entry(newWindow, textvariable=self.entryNameText, state='readonly')
        nameEntry.grid(column=1, row=1, pady=10, sticky='W')

        #Session Length
        sessionLabel = ttk.Label(newWindow, text='Session Length: ')
        sessionLabel.grid(column=0, row=2, sticky='W', padx=10, pady=10)

        self.entrySessionText = tk.StringVar()
        self.entrySessionText.set(studentInformation[1])

        sessionEntry = ttk.Entry(newWindow, textvariable=self.entrySessionText) 
        sessionEntry.grid(column=1, row=2, pady=10, sticky='W')

        #Date
        dateLabel = ttk.Label(newWindow, text='Date: ')
        dateLabel.grid(column=0, row=3, sticky='W', padx=10, pady=10)

        self.entryDateText = tk.StringVar()
        self.entryDateText.set(studentInformation[2])

        dateEntry = ttk.Entry(newWindow, textvariable=self.entryDateText) 
        dateEntry.grid(column=1, row=3, pady=10, sticky='W')

        #Amount 
        amountLabel = ttk.Label(newWindow, text='Amount: ')
        amountLabel.grid(column=0, row=4, sticky='W', padx=10, pady=10)

        self.entryAmountText = tk.StringVar()
        self.entryAmountText.set(studentInformation[3])

        amountEntry = ttk.Entry(newWindow, textvariable=self.entryAmountText) 
        amountEntry.grid(column=1, row=4, pady=10, sticky='W')

        #Payment Status
        paymentLabel = ttk.Label(newWindow, text='Payment Status: ')
        paymentLabel.grid(column=0, row=5, sticky='W', padx=10, pady=10)


        paymentEntry = ttk.Combobox(newWindow, state='readonly')
        paymentEntry['values'] = [ 'Paid', 'Not Paid' , 'Cancelled']
        if studentInformation[4].lower() == 'paid':
            paymentEntry.current(0)
        else:
            paymentEntry.current(1)
        paymentEntry.grid(column=1, row=5, pady=10, sticky='W')

        def getData ():  

            array = [nameEntry.get(), int(sessionEntry.get()), dateEntry.get(), int(amountEntry.get()), paymentEntry.get()]
            updateStudent(int(id), array)
            messages1.config(text="Sucessfully Updated")

        def deleteData1():
            deleteData(int(id))

        button1 = ttk.Button(newWindow, text='Update', command= getData)
        button1.grid(column=1, row=6, pady=10, sticky='w')

        button1 = ttk.Button(newWindow, text='Delete', command= deleteData1)
        button1.grid(column=0, row=6, padx = 10, sticky ='w')

        messages = tk.LabelFrame(newWindow, text='Messages:', width=300, height=100)
        messages.grid(column=0, row=7, pady=10, padx=10, columnspan=2)

        messages1 = ttk.Label(messages, text='Enter data in the fields above.', wraplength=250)
        messages1.place(x=10, y=10, anchor="w")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Update Information", font=controller.title_font)
        label.grid(column=0, row=0, padx=10, pady=10, sticky='W')
        
        def refreshID():

            #Session ID Selection
            sessionIdLabel = ttk.Label(self, text='Select a session id to update: ')
            sessionIdLabel.grid(column=0, row=1, sticky='W', padx=100, pady=10)

            listOfSessionIDs = idList()

            self.sessionIdDropdown = ttk.Combobox(self)
            self.sessionIdDropdown['values'] = listOfSessionIDs
            self.sessionIdDropdown.grid(column=1, row=1, pady=10, sticky='W')

            button1 = ttk.Button(self, text='Update', command=lambda: updateInfo.openNewWindow(self, self.sessionIdDropdown.get()))
            button1.grid(column=1, row=2, pady=10, sticky='w')
            
        refreshID()
        refreshButton = ttk.Button(self, text='Refresh', command=lambda: refreshID())
        refreshButton.grid(column=0, row=2, pady=5, sticky='w')

class studentInformation(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="Student Information", font=controller.title_font)
        label.grid(column=0, row=0, padx=10, pady=5, sticky='W')
        
        def refreshName():
            filterLabel = ttk.Label(self, text="Filter By:")
            filterLabel.grid(column=0, row=1, padx=10, pady=5, sticky='W')

            #Filter by Name
            listOfNames = studentList()
            listOfNames.insert(0, "All")
            nameLabel = ttk.Label(self, text='Student Name: ')
            nameLabel.grid(column=0, row=2, sticky='W', padx=20, pady=5)

            nameList2 = ttk.Combobox(self, state='readonly')
            nameList2['values'] = listOfNames
            nameList2.current(0)
            nameList2.grid(column=1, row=2, pady=5, sticky='W')
            
            
            #Filter by Status
            paymentLabel = ttk.Label(self, text='Payment Status: ')
            paymentLabel.grid(column=0, row=3, sticky='W', padx=20, pady=5)

            paymentStatus = [ 'Paid', 'Not Paid', 'Cancelled']

            paymentEntry = ttk.Combobox(self, state='readonly')
            paymentEntry['values'] = paymentStatus
            paymentEntry.current(0)
            paymentEntry.grid(column=1, row=3, pady=5, sticky='W')

            filterButton = ttk.Button(self, text='Filter', command=lambda: displayInfo(nameList2.get(), paymentEntry.get()))
            filterButton.grid(column=1, row=4, pady=5, sticky='w')

            self.textBox = tk.Text(self, width=70, height=20, bd=2, bg="white", fg="black",)
            #self.studentInfo()
            self.textBox.configure(state='disabled')
            self.textBox.grid(column=0, row=5, columnspan=2, sticky='w')

            def displayInfo(name, status):

                text = filterStudentInfo(name, status)
                self.textBox.configure(state='normal')
                self.textBox.delete('1.0', tk.END)
                self.textBox.insert(tk.INSERT, text)
                self.textBox.configure(state='disabled')

            self.scrollbar = tk.Scrollbar(self, command=self.textBox.yview)
            self.textBox['yscrollcommand'] = self.scrollbar.set
            self.scrollbar.grid(column=2, row=5, sticky='nsew')
            
        refreshName()
        refreshButton = ttk.Button(self, text='Refresh', command=lambda: refreshName())
        refreshButton.grid(column=0, row=4, pady=5, sticky='w')


if __name__ == "__main__":
    app = ApplicationStart()
    app.mainloop()