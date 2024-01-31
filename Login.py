import re
from tkinter import *
from tkinter import messagebox
# from ctypes import windll
import pymysql
import customtkinter
from PIL import Image
from PIL import ImageTk
# from MainApp import Main


def resize_image(image_path, new_size):
    original_image = Image.open(image_path)
    resized_image = original_image.resize(new_size)
    return ImageTk.PhotoImage(resized_image)


def resized(imagePath, newSize):
    original_image = Image.open(imagePath)
    resized_image = original_image.resize(newSize)
    return ImageTk.PhotoImage(resized_image)


def is_valid_email(email):
    email_regex = (
        r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    )
    return re.match(email_regex, email)


class Login:

    def connect_database(self):
        firstName = self.first_name_label_entry.get()
        lastName = self.last_name_label_entry.get()
        self.email = self.email_label_entry.get()
        password = self.password_label_entry.get()
        confirmPassword = self.confirm_password_label_entry.get()
        contactNo = self.contact_no_label_entry.get()

        if firstName == '' or lastName == '' or self.email == '' or password == '' or confirmPassword == '' or contactNo == '':
            messagebox.showerror("Error", "Please fill all the fields", )

        elif not contactNo.isdigit():
            messagebox.showerror('Error', "\"Contact Number\" should be a valid number", )
        elif not password == confirmPassword:
            messagebox.showerror('Error', "password mismatch", )

        elif not is_valid_email(self.email):
            messagebox.showerror("Error", "Please enter a valid email address", icon='error', )

        else:
            try:
                connection = pymysql.connect(host="localhost", user="root", password="isaac")
                cursor = connection.cursor()
                query = "create database if not exists userEmployees"
                cursor.execute(query)
                query = "use userEmployees"
                cursor.execute(query)
                query = ("create table if not exists user_logins(contactNo int  primary key not null, firstName "
                         "varchar(50) not null, lastName varchar(50) not null, email varchar(40) not null, "
                         "password varchar(100) not null)")
                cursor.execute(query)
                # cursor.close()

            except Exception as e:
                print(e)
                messagebox.showerror("Error", "Connection Failed", )
                return

            try:
                cursor.execute('use userEmployees')
                query = "select * from user_logins where contactNo= %s"
                cursor.execute(query, (contactNo,))
                row = cursor.fetchone()
                if row is not None:
                    messagebox.showerror('Error', f'user \"{contactNo}\" already exists', )

                else:
                    query = ("insert into user_logins(contactNo, firstName, lastName, email, password) values(%s,%s,"
                             "%s,%s,%s)")
                    cursor.execute(query, (contactNo, firstName, lastName, self.email, password))
                    messagebox.showinfo('Success', 'Registration Successful', )
                    connection.commit()
                    connection.close()
                    self.destroy_signup_method()

            except Exception as e:
                print(e)
                messagebox.showerror('Error', 'Something went wrong', )

    def login_user(self):
        contact = self.contactNoEntry.get()
        password = self.passwordEntry.get()

        if contact == '' or password == '':
            messagebox.showerror("Error", "All fields are required")
        elif not contact.isdigit():
            messagebox.showerror("Error", "Invalid contact No")
        else:
            try:
                connection = pymysql.connect(host='localhost', user='root', password='isaac', database="userEmployees")
                cursor = connection.cursor()
                cursor.execute('use userEmployees')
                query = "select * from user_logins where contactNo= %s"
                # cursor.execute(query, (contact, password))
                cursor.execute(query, (contact,))
                row1 = cursor.fetchone()

                query = "select * from user_logins where contactNo= %s and password= %s"
                # cursor.execute(query, (contact, password))
                cursor.execute(query, (contact, password))
                row2 = cursor.fetchone()
                # messagebox.showinfo("Welcome", "Login is Successful")

                if row1 is None:
                    messagebox.showerror("Error", "Contact number does not exist")
                else:
                    if row2 is None:
                        messagebox.showerror("Error", "Incorrect Password")
                    else:
                        # messagebox.showinfo("Welcome", "Login is Successful")
                        self.window.destroy()
                        from BillApp import BillApp
                        BillApp()

            except Exception as e:
                print(e)
                # messagebox.showerror("Error", f"{e} sorry")

    def destroy_signup_method(self):
        self.register_frame.destroy()
        self.headerFrame2.destroy()

    def fade_in(self, alpha=0.0):
        if alpha < 1.0:
            alpha += 0.1
            self.window.attributes('-alpha', alpha)
            self.window.after(50, lambda: self.fade_in(alpha))

    def fade_out(self, alpha=1.0):
        if alpha > 0.0:
            alpha -= 0.1
            self.window.attributes('-alpha', alpha)
            self.window.after(50, lambda: self.fade_out(alpha))
        else:
            self.window.destroy()

    def header_frame_function(self):
        headerFrame = customtkinter.CTkFrame(self.window, fg_color='#1D2328', height=510, width=400)
        headerFrame.place(x=400, y=50)

        # *************************** creating details for the header Frame *******************
        new_size = (125, 125)
        self.systemLogo = resize_image('images2/fin.png', new_size)
        systemLogoLabel = Label(headerFrame, image=self.systemLogo, bg='#1D2328')
        systemLogoLabel.place(x=5, y=145)
        headerLabel = customtkinter.CTkLabel(headerFrame, text='Smart Collections',
                                             font=('mv boli', 30), fg_color='#1D2328', text_color='#8DB22A'
                                             )
        headerLabel.place(x=125, y=175)
        headerLabel2 = customtkinter.CTkLabel(headerFrame, text='Billing System',
                                              font=('mv boli', 26), fg_color='#1D2328', text_color='#8DB22A'
                                              )
        headerLabel2.place(x=170, y=215)

    def header_frame_function2(self):
        self.headerFrame2 = customtkinter.CTkFrame(self.window, fg_color='#15191C', height=560, width=400)
        self.headerFrame2.place(x=0, y=0)

        # *************************** creating details for the header Frame *******************
        new_size = (125, 125)
        self.systemLogo3 = resize_image('images2/fin.png', new_size)
        systemLogoLabel = Label(self.headerFrame2, image=self.systemLogo3, bg='#15191C')
        systemLogoLabel.place(x=5, y=175)
        headerLabel = customtkinter.CTkLabel(self.headerFrame2, text='Smart Collections',
                                             font=('mv boli', 30), fg_color='#15191C', text_color='#8DB22A'
                                             )
        headerLabel.place(x=125, y=205)
        headerLabel2 = customtkinter.CTkLabel(self.headerFrame2, text='Billing System',
                                              font=('mv boli', 26), fg_color='#15191C', text_color='#8DB22A'
                                              )
        headerLabel2.place(x=170, y=245)

    def quitMethod(self):

        # ********************* beginning of quit frame button **************************

        quitFrameButtons = Frame(self.window, width=400, height=50, background='#1D2328')
        quitFrameButtons.place(x=400, y=0)

        new_size = (25, 25)
        self.quitButtonImage = resize_image('images2/icons8_Cancel_32px.png', new_size)
        self.quitButtonImage2 = resize_image('images2/icons8_Cancel_30px_3.png', new_size)
        self.minimizeButtonImage = resize_image('images2/icons8_Minus_32px_1.png', new_size)
        self.minimizeButtonImage2 = resize_image('images2/icons8_Minus_30px_3.png', new_size)

        self.minimizeButton = Button(quitFrameButtons, image=self.minimizeButtonImage, text='', bg='#1D2328',
                                     bd=0, activebackground='#1D2328', activeforeground='#1D2328', cursor='hand2',
                                     command=lambda: self.window.withdraw())
        self.minimizeButton.place(x=340, y=0)
        self.minimizeButton.bind('<Enter>',
                                 lambda event: self.minimizeButton.configure(image=self.minimizeButtonImage2))
        self.minimizeButton.bind('<Leave>', lambda event: self.minimizeButton.configure(image=self.minimizeButtonImage))

        self.quitButton = Button(quitFrameButtons, image=self.quitButtonImage, text='', bg='#1D2328',
                                 bd=0, activebackground='#1D2328', activeforeground='#1D2328', cursor='hand2', )
        self.quitButton.configure(
            command=lambda: self.fade_out()
            if messagebox.askyesno("Confirm Exit", "Do you really want to quit?",
                                   parent=self.window)
            else None
        )
        self.quitButton.place(x=370, y=0)
        self.quitButton.bind('<Enter>', lambda event: self.quitButton.configure(image=self.quitButtonImage2))
        self.quitButton.bind('<Leave>', lambda event: self.quitButton.configure(image=self.quitButtonImage))

    def new_user(self):
        self.register_frame = Frame(self.window, width=400, height=500, bg='#1D2328')
        self.register_frame.place(x=400, y=50)
        # self.register_frame.grab_set()

        new_size = (80, 80)
        self.systemLogo2 = resize_image('images2/fin.png', new_size)
        systemLogoLabel2 = Label(self.register_frame, image=self.systemLogo2, bg='#1D2328')
        systemLogoLabel2.place(x=50, y=0)
        headerLabel = customtkinter.CTkLabel(self.register_frame, text='Smart Collections',
                                             font=('mv boli', 26), fg_color='#1D2328', text_color='#8DB22A'
                                             )
        headerLabel.place(x=130, y=10)
        headerLabel2 = customtkinter.CTkLabel(self.register_frame, text='Billing System',
                                              font=('mv boli', 21), fg_color='#1D2328', text_color='#8DB22A'
                                              )
        headerLabel2.place(x=165, y=40)

        first_name_label = customtkinter.CTkLabel(self.register_frame, text='First Name', font=('arial', 15),
                                                  fg_color='#1D2328', text_color='#8DB22A')
        first_name_label.place(x=93, y=95)
        self.first_name_label_entry = customtkinter.CTkEntry(self.register_frame, border_color='#8DB22A', width=150,
                                                             height=30, border_width=1,
                                                             font=('arial', 15), fg_color='#15191C', corner_radius=20,
                                                             text_color='#8DB22A')
        self.first_name_label_entry.place(x=50, y=120)

        last_name_label = customtkinter.CTkLabel(self.register_frame, text='Last Name', font=('arial', 15),
                                                 fg_color='#1D2328', text_color='#8DB22A')
        last_name_label.place(x=250, y=95)
        self.last_name_label_entry = customtkinter.CTkEntry(self.register_frame, border_color='#8DB22A', width=150,
                                                            height=30, border_width=1,
                                                            font=('arial', 15), fg_color='#15191C', corner_radius=20,
                                                            text_color='#8DB22A')
        self.last_name_label_entry.place(x=210, y=120)

        contact_no_label = customtkinter.CTkLabel(self.register_frame, text='Contact Number', font=('arial', 15),
                                                  fg_color='#1D2328', text_color='#8DB22A')
        contact_no_label.place(x=105, y=160)
        self.contact_no_label_entry = customtkinter.CTkEntry(self.register_frame, border_color='#8DB22A', width=240,
                                                             height=30, border_width=1,
                                                             font=('arial', 15), fg_color='#15191C', corner_radius=20,
                                                             text_color='#8DB22A')
        self.contact_no_label_entry.place(x=90, y=185)

        email_label = customtkinter.CTkLabel(self.register_frame, text='Email', font=('arial', 15),
                                             fg_color='#1D2328', text_color='#8DB22A')
        email_label.place(x=105, y=220)
        self.email_label_entry = customtkinter.CTkEntry(self.register_frame, border_color='#8DB22A', width=240,
                                                        height=30, border_width=1,
                                                        font=('arial', 15), fg_color='#15191C', corner_radius=20,
                                                        text_color='#8DB22A')
        self.email_label_entry.place(x=90, y=245)

        password_label = customtkinter.CTkLabel(self.register_frame, text='Password', font=('arial', 15),
                                                fg_color='#1D2328', text_color='#8DB22A')
        password_label.place(x=105, y=280)
        self.password_label_entry = customtkinter.CTkEntry(self.register_frame, border_color='#8DB22A', width=240,
                                                           height=30, border_width=1, show='*',
                                                           font=('arial', 15), fg_color='#15191C', corner_radius=20,
                                                           text_color='#8DB22A')
        self.password_label_entry.place(x=90, y=305)

        confirm_password_label = customtkinter.CTkLabel(self.register_frame, text='Confirm Password',
                                                        font=('arial', 15),
                                                        fg_color='#1D2328', text_color='#8DB22A')
        confirm_password_label.place(x=105, y=340)
        self.confirm_password_label_entry = customtkinter.CTkEntry(self.register_frame, border_color='#8DB22A',
                                                                   width=240, show='*',
                                                                   height=30, border_width=1,
                                                                   font=('arial', 15), fg_color='#15191C',
                                                                   corner_radius=20,
                                                                   text_color='#8DB22A')
        self.confirm_password_label_entry.place(x=90, y=365)

        signInButton = customtkinter.CTkButton(self.register_frame, font=('arial', 13, 'bold'),
                                               fg_color='#8DB22A', hover_color='#FBD71D',
                                               text_color='#15191C', text='Sign In',
                                               border_width=0, cursor='hand2', width=150, height=30,
                                               corner_radius=15, command=self.connect_database)
        # signInButton.configure(command=lambda: self.connect_database())
        signInButton.place(x=50, y=415)

        resetButton = customtkinter.CTkButton(self.register_frame, font=('arial', 13, 'bold'),
                                              fg_color='#8DB22A', hover_color='#FBD71D',
                                              text_color='#15191C', text='Reset',
                                              border_width=0, cursor='hand2', width=150, height=30,
                                              corner_radius=15)
        # resetButton.configure(command=lambda: [self.register_frame.destroy(), self.new_user()])
        resetButton.configure(
            command=lambda: self.window.after(0, lambda: [self.register_frame.destroy(), self.new_user()]))

        resetButton.place(x=212, y=415)

        new_size = (22, 22)
        self.backButtonImage = resize_image('images2/icons8_Back_To_32px_2.png', new_size)

        backButton = Button(self.register_frame, text=' Back', font=('arial', 13), fg='#9AC72F', bg='#1D2328',
                            image=self.backButtonImage, compound='left', borderwidth=0, cursor='hand2',
                            activebackground='#FBD71D',
                            command=lambda: [self.register_frame.destroy(), self.headerFrame2.destroy()])
        # backButton.configure(command=lambda: [self.destroy_register_frame, self.headerFrame2])
        backButton.place(x=180, y=465)

    def submit_forgot_password(self):
        contact = self.head_contact_entry.get()
        newPassword = self.new_password_entry.get()
        confirmPassword = self.confirm_password_entry.get()

        if contact == '' or newPassword == '' or confirmPassword == '':
            messagebox.showerror("Error", "All fields are required")

        elif not contact.isdigit():
            messagebox.showerror("Error", "Invalid Contact Number")

        elif newPassword != confirmPassword:
            messagebox.showerror("Error", "Password Mismatch")

        else:
            try:
                connection = pymysql.connect(host='localhost', user='root', password='isaac', database='userEmployees')
                cursor = connection.cursor()
                cursor.execute('use userEmployees')
                query = "select * from user_logins where contactNo= %s"
                cursor.execute(query, (contact,))
                row = cursor.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Incorrect Contact Number")

                else:

                    query = "update user_logins set password=%s where contactNo=%s"
                    cursor.execute(query, (newPassword, contact))
                    connection.commit()
                    connection.close()
                    messagebox.showinfo("Success", "Password reset successfully, login with new password.")
                    self.forgotPasswordFrame.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"{e}")

    def forgot_password(self):
        self.forgotPasswordFrame = customtkinter.CTkFrame(self.window, height=500, width=400, fg_color='#15191C')
        self.forgotPasswordFrame.place(x=0, y=70)

        header_label = Label(self.forgotPasswordFrame, text='RESET PASSWORD', bg='#15191C',
                             fg='#9AC72F', font=('Microsoft Yahei UI Light', 25, 'bold underline'))
        header_label.place(x=50, y=10)

        header_label_contact = customtkinter.CTkLabel(self.forgotPasswordFrame, text='Contact No',
                                                      bg_color='#15191C',
                                                      text_color='#9AC72F', font=('arial', 13))
        header_label_contact.place(x=60, y=70)

        self.head_contact_entry = customtkinter.CTkEntry(self.forgotPasswordFrame, border_color='#8DB22A',
                                                         width=240,
                                                         height=30, border_width=0,
                                                         font=('arial', 15), fg_color='#1D2328',
                                                         corner_radius=20,
                                                         text_color='#8DB22A')
        self.head_contact_entry.place(x=60, y=95)
        customtkinter.CTkFrame(self.forgotPasswordFrame, width=230, height=2, fg_color='#8DB22A').place(x=65, y=125)

        new_password = customtkinter.CTkLabel(self.forgotPasswordFrame, text='New Password', bg_color='#15191C',
                                              text_color='#9AC72F', font=('arial', 13))
        new_password.place(x=60, y=150)

        self.new_password_entry = customtkinter.CTkEntry(self.forgotPasswordFrame, border_color='#8DB22A',
                                                         width=240, show='*',
                                                         height=30, border_width=0,
                                                         font=('arial', 15), fg_color='#1D2328',
                                                         corner_radius=20,
                                                         text_color='#8DB22A')
        self.new_password_entry.place(x=60, y=175)
        customtkinter.CTkFrame(self.forgotPasswordFrame, width=230, height=2, fg_color='#8DB22A').place(x=65, y=205)

        confirm_password2 = customtkinter.CTkLabel(self.forgotPasswordFrame, text='Confirm Password',
                                                   bg_color='#15191C',
                                                   text_color='#9AC72F', font=('arial', 13))
        confirm_password2.place(x=60, y=230)

        self.confirm_password_entry = customtkinter.CTkEntry(self.forgotPasswordFrame, border_color='#8DB22A',
                                                             width=240, show='*',
                                                             height=30, border_width=0,
                                                             font=('arial', 15), fg_color='#1D2328',
                                                             corner_radius=20,
                                                             text_color='#8DB22A')
        self.confirm_password_entry.place(x=60, y=255)
        customtkinter.CTkFrame(self.forgotPasswordFrame, width=230, height=2, fg_color='#8DB22A').place(x=65, y=285)

        self.submit_forgot_password_button = customtkinter.CTkButton(self.forgotPasswordFrame,
                                                                     font=('arial', 13, 'bold'),
                                                                     fg_color='#8DB22A', hover_color='#FBD71D',
                                                                     text_color='#15191C', text='Submit',
                                                                     border_width=0, cursor='hand2', width=240,
                                                                     height=35,
                                                                     corner_radius=15,
                                                                     command=self.submit_forgot_password)
        self.submit_forgot_password_button.place(x=60, y=330)

        new_size = (22, 22)
        self.backButtonImage2 = resize_image('images2/icons8_Back_To_32px_2.png', new_size)

        backButton = Button(self.forgotPasswordFrame, text=' Back', font=('arial', 13), fg='#9AC72F', bg='#15191C',
                            image=self.backButtonImage2, compound='left', borderwidth=0, cursor='hand2',
                            activebackground='#FBD71D', command=lambda: self.forgotPasswordFrame.destroy())
        # backButton.configure(command=lambda: [self.destroy_register_frame, self.headerFrame2])
        backButton.place(x=140, y=385)

    def login_file(self):
        loginFrame = customtkinter.CTkFrame(self.window, fg_color='#15191C', width=400, height=560)
        loginFrame.place(x=0, y=0)
        socialSitesFrame = customtkinter.CTkFrame(loginFrame, fg_color='#15191C', width=180, height=60)
        socialSitesFrame.place(x=0, y=0)

        userLoginsFrame = customtkinter.CTkFrame(loginFrame, fg_color='#15191C', height=350, width=330)
        userLoginsFrame.place(x=45, y=170)

        new_size = (30, 30)
        self.twitterImage = resize_image("images2/icons8_Twitter_32px.png", new_size)
        self.twitterImage2 = resize_image("images2/icons8_Twitter_32px_2.png", new_size)
        self.faceBook = resize_image('images2/icons8_Facebook_32px_2.png', new_size)
        self.faceBook2 = resize_image('images2/icons8_Facebook_32px_8.png', new_size)
        self.instagramImage = resize_image("images2/icons8_Instagram_32px.png", new_size)
        self.instagramImage2 = resize_image("images2/icons8_Instagram_32px_3.png", new_size)
        self.youtubeImage = resize_image("images2/icons8_YouTube_32px.png", new_size)
        self.youtubeImage2 = resize_image("images2/icons8_YouTube_32px_1.png", new_size)
        self.gmailImage = resize_image("images2/icons8_Secured_Letter_32px.png", new_size)
        self.gmailImage2 = resize_image("images2/icons8_Secured_Letter_32px_2.png", new_size)

        self.twitterButton = Button(socialSitesFrame, image=self.twitterImage, text='',
                                    bg='#15191C', width=25, fg='#15191C',
                                    cursor='hand2', bd=0)
        self.twitterButton.bind('<Enter>', lambda event: self.twitterButton.configure(image=self.twitterImage2))
        self.twitterButton.bind('<Leave>', lambda event: self.twitterButton.configure(image=self.twitterImage))
        self.twitterButton.place(x=5, y=5)

        self.faceBookButton = Button(socialSitesFrame, image=self.faceBook, text='',
                                     bg='#15191C', width=25, fg='#15191C', bd=0,
                                     cursor='hand2')
        self.faceBookButton.bind('<Enter>', lambda event: self.faceBookButton.configure(image=self.faceBook2))
        self.faceBookButton.bind('<Leave>', lambda event: self.faceBookButton.configure(image=self.faceBook))
        self.faceBookButton.place(x=37, y=5)

        self.instagramButton = Button(socialSitesFrame, image=self.instagramImage, text='',
                                      bg='#15191C', width=25, fg='#15191C', bd=0, cursor='hand2')
        self.instagramButton.bind('<Enter>', lambda event: self.instagramButton.configure(image=self.instagramImage2))
        self.instagramButton.bind('<Leave>', lambda event: self.instagramButton.configure(image=self.instagramImage))
        self.instagramButton.place(x=69, y=5)

        self.youtubeButton = Button(socialSitesFrame, image=self.youtubeImage, text='',
                                    bg='#15191C', width=25, fg='#15191C', bd=0, cursor='hand2')
        self.youtubeButton.bind('<Enter>', lambda event: self.youtubeButton.configure(image=self.youtubeImage2))
        self.youtubeButton.bind('<Leave>', lambda event: self.youtubeButton.configure(image=self.youtubeImage))
        self.youtubeButton.place(x=101, y=5)

        self.gmailButton = Button(socialSitesFrame, image=self.gmailImage, text='',
                                  bg='#15191C', width=25, fg='#15191C', bd=0, cursor='hand2')
        self.gmailButton.bind('<Enter>', lambda event: self.gmailButton.configure(image=self.gmailImage2))
        self.gmailButton.bind('<Leave>', lambda event: self.gmailButton.configure(image=self.gmailImage))
        self.gmailButton.place(x=133, y=5)

        customtkinter.CTkLabel(socialSitesFrame, text_color='#8DB22A',
                               text='Connect with us on', font=('arial', 13, 'bold')).place(x=35, y=37)

        # *************** End of social sites frame ***************

        # *************** beginning of userLoginsFrame ***************

        # loginIcon = CTkImage(Image.open('images2/icons8_User_Shield_100px.png'))
        imageSize = (100, 100)
        self.originalLoginIcon = resized('images2/icons8_User_Shield_100px.png', imageSize)
        Label(loginFrame, image=self.originalLoginIcon, text='', bg='#15191C').place(x=140, y=60)

        contactNoLabel = customtkinter.CTkLabel(userLoginsFrame, text='Contact Number', font=('arial', 15),
                                                fg_color='#15191C', text_color='#8DB22A')
        contactNoLabel.place(x=95, y=0)
        self.contactNoEntry = customtkinter.CTkEntry(userLoginsFrame, border_color='#8DB22A', width=240, height=35,
                                                     font=('arial', 15), fg_color='#1D2328', corner_radius=15,
                                                     text_color='#8DB22A')
        self.contactNoEntry.place(x=50, y=25)
        new_size = (33, 33)
        self.userImage = resize_image("images2/icons8_Male_User_100px.png", new_size)
        Label(userLoginsFrame, image=self.userImage, text='', bg='#15191C').place(x=5, y=24)

        passwordLabel = customtkinter.CTkLabel(userLoginsFrame, text='Password', font=('arial', 15),
                                               fg_color='#15191C', text_color='#8DB22A')
        passwordLabel.place(x=120, y=90)
        self.passwordEntry = customtkinter.CTkEntry(userLoginsFrame, border_color='#8DB22A', width=240, height=35,
                                                    font=('arial', 15), fg_color='#1D2328', corner_radius=15, show='*',
                                                    text_color='#8DB22A')
        self.passwordEntry.place(x=50, y=115)
        new_size = (33, 33)
        self.passwordImage = resize_image("images2/icons8_Lock_35px.png", new_size)
        Label(userLoginsFrame, image=self.passwordImage, text='', bg='#15191C').place(x=5, y=114)

        forgotPasswordButton = Button(userLoginsFrame, font=('arial', 9, 'underline'), bg='#15191C',
                                      fg='#8DB22A', text='Forget Password', activebackground='#15191C',
                                      bd=0, cursor='hand2', command=self.forgot_password)
        forgotPasswordButton.place(x=187, y=170)

        logInButton = customtkinter.CTkButton(userLoginsFrame, font=('arial', 13, 'bold'),
                                              fg_color='#8DB22A', hover_color='#FBD71D',
                                              text_color='#15191C', text='Log In',
                                              border_width=0, cursor='hand2', width=240, height=35,
                                              corner_radius=15, command=self.login_user)
        logInButton.place(x=50, y=210)

        customtkinter.CTkLabel(userLoginsFrame, text='----------------- OR -----------------',
                               font=('arial', 17),
                               fg_color='#15191C', text_color='#8DB22A').place(x=50, y=270)

        createUserButton = Button(userLoginsFrame, font=('arial', 10, 'underline'), bg='#15191C',
                                  fg='#8DB22A', text='Create New User', activebackground='#15191C',
                                  bd=0, cursor='hand2', activeforeground='#FBD71D')
        createUserButton.configure(command=lambda: [self.new_user(), self.header_frame_function2()])
        createUserButton.place(x=130, y=310)

    def __init__(self):

        self.backButtonImage2 = None
        self.submit_forgot_password = self.submit_forgot_password
        self.submit_forgot_password_button = None
        self.confirm_password_entry = None
        self.new_password_entry = None
        self.head_contact_entry = None
        self.forgotPasswordFrame = None
        self.forgot_password = self.forgot_password
        self.passwordEntry = None
        self.contactNoEntry = None
        self.login_user = self.login_user
        self.password = None
        self.confirmPassword = None
        self.contactNo = None
        self.email = None
        self.lastName = None
        self.firstName = None
        self.email_label_entry = None
        self.password_label_entry = None
        self.confirm_password_label_entry = None
        self.contact_no_label_entry = None
        self.last_name_label_entry = None
        self.first_name_label_entry = None
        self.connect_database = self.connect_database
        self.restoreButton = None
        self.systemLogo3 = None
        self.headerFrame2 = None
        self.register_frame = None
        self.backButtonImage = None
        self.systemLogo2 = None
        self.systemLogo = None
        self.passwordImage = None
        self.userImage = None
        self.originalLoginIcon = None
        self.quitButtonImage = None
        self.quitButtonImage2 = None
        self.quitButton = None
        self.minimizeButtonImage = None
        self.minimizeButtonImage2 = None
        self.minimizeButton = None
        self.gmailImage = None
        self.gmailButton = None
        self.gmailImage2 = None
        self.youtubeImage = None
        self.youtubeButton = None
        self.youtubeImage2 = None
        self.instagramImage = None
        self.instagramImage2 = None
        self.instagramButton = None
        self.faceBook = None
        self.faceBook2 = None
        self.twitterImage = None
        self.faceBookButton = None
        self.twitterImage2 = None
        self.twitterButton = None
        self.loginFrame = None

        self.window = Tk()
        self.window.overrideredirect(True)
        self.window.config(background='#15191C')
        self.window.geometry('800x560+300+100')
        self.window.iconbitmap('images2/icon2.ico')
        self.window.attributes('-alpha', 0.0)
        self.window.after(50, self.fade_in)

        self.login_file()
        self.header_frame_function()
        self.quitMethod()

        self.window.mainloop()


if __name__ == '__main__':
    Login()
