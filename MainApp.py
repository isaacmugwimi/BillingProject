import os
import random
import smtplib
import tempfile
import tkinter as tk
from time import strftime
from tkinter import *
from tkinter import ttk, messagebox
import re
from datetime import datetime

import customtkinter
import pymysql
from PIL import Image
from PIL import ImageTk


# theme types alt, clam, classic, aqua


def resizing(path, imageSize):
    originalImage = Image.open(path)
    resized_image = originalImage.resize(imageSize)
    return ImageTk.PhotoImage(resized_image)


def resize2(imagePath, imageSize2):
    originalImage = Image.open(imagePath)
    newImage = originalImage.resize(imageSize2)
    return ImageTk.PhotoImage(newImage)


def is_valid_email(email):
    email_regex = (
        r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    )
    return re.match(email_regex, email)


class Main:

    # def scroll_text(self):
    #     def move_text():
    #         self.marquee_text.place(x=self.marquee_text.winfo_x() - 1)
    #         if self.marquee_text.winfo_x() + self.marquee_text.winfo_width() < 0:
    #             self.marquee_text.place(x=1366)  # Reset the label position when it goes out of the screen
    #
    #         self.mainWindow.after(3, move_text)
    #
    #     move_text()

    def time(self):
        string = strftime('%H:%M:%S %p')
        self.labelTime.config(text=string)
        self.labelTime.after(1000, self.time)

    def on_combobox_select(self):
        self.selectedItem = self.combobox1_category.get()
        return self.selectedItem

    def exit_method(self):
        response = messagebox.askyesno("Exit", "Do you want to Exit?")
        if response:
            self.mainWindow.destroy()

    def mainMethod(self):
        # ********************************** Middle image *************************
        # imageSize2 = (400, 265)

        self.middleImage = resize2("images2/good.jpg", (370, 350))
        Label(self.mainWindow, text='', image=self.middleImage).place(x=0, y=420)

        # ********************************** Customer_Product Frame *************************

        self.customer_product_frame = customtkinter.CTkFrame(self.mainWindow, width=950, height=170,
                                                             fg_color='#FFFFFF',
                                                             corner_radius=50, border_width=2, border_color='#00FFFF')

        self.customer_product_frame.place(x=5, y=80)

        # ************* Customer Frame **************

        self.customerFrame = LabelFrame(self.customer_product_frame, text='Customer Details', fg='#F60514', width=400,
                                        font=('Arial', 13, 'bold'), bg='#FFFFFF', border=2, height=200)
        self.customerFrame.place(x=20, y=10)

        # Mobile Number
        mobileNoLabel = customtkinter.CTkLabel(self.customerFrame, text='Mobile No:', font=('arial', 13, 'bold'),
                                               fg_color='#FFFFFF', text_color='#0C0C0C')
        mobileNoLabel.grid(row=0, column=1, padx=15, pady=5, sticky='w')
        self.mobileNoEntry = customtkinter.CTkEntry(self.customerFrame, border_color='#DCDCDC', width=110,
                                                    border_width=0, text_color='#0C0C0C',
                                                    corner_radius=15, height=25, font=('arial', 15),
                                                    placeholder_text="Enter Mobile Number", fg_color='#DCDCDC')
        self.mobileNoEntry.grid(row=0, column=2, padx=10, pady=5)
        # Customer Name
        customerNameLabel = customtkinter.CTkLabel(self.customerFrame, text='Customer Name:',
                                                   font=('arial', 13, 'bold'),
                                                   fg_color='#FFFFFF', text_color='#0C0C0C')
        customerNameLabel.grid(row=0, column=3, padx=15, pady=5, sticky='w')
        self.customerNameEntry = customtkinter.CTkEntry(self.customerFrame, border_color='#DCDCDC', width=140,
                                                        border_width=0, fg_color='#DCDCDC', text_color='#0C0C0C',
                                                        corner_radius=15, height=25, font=('arial', 15))
        self.customerNameEntry.grid(row=0, column=4, padx=10, pady=5)

        # Email
        emailLabel = customtkinter.CTkLabel(self.customerFrame, text='Email:', font=('arial', 13, 'bold'),
                                            fg_color='#FFFFFF', text_color='#0C0C0C')
        emailLabel.grid(row=0, column=5, padx=15, pady=5, sticky=W)
        self.emailEntry = customtkinter.CTkEntry(self.customerFrame, border_color='#DCDCDC', width=130,
                                                 border_width=0, fg_color='#DCDCDC', text_color='#0C0C0C',
                                                 corner_radius=15, height=25, font=('arial', 15))
        self.emailEntry.grid(row=0, column=6, padx=10, pady=5)

        # Address

        addressLabel = customtkinter.CTkLabel(self.customerFrame, text='Address:', font=('arial', 13, 'bold'),
                                              fg_color='#FFFFFF', text_color='#0C0C0C')
        addressLabel.grid(row=0, column=7, padx=15, pady=5, sticky=W)
        self.addressEntry = customtkinter.CTkEntry(self.customerFrame, border_color='#DCDCDC', width=60,
                                                   border_width=0, fg_color='#DCDCDC', text_color='#0C0C0C',
                                                   corner_radius=15, height=25, font=('arial', 15))
        self.addressEntry.grid(row=0, column=8, padx=10, pady=5)

        # **************** product Frame ************
        self.productFrame = LabelFrame(self.customer_product_frame, text='Product Details', fg='#F60514', width=680,
                                       font=('Arial', 13, 'bold'), bg='#FFFFFF', border=2, )
        self.productFrame.place(x=20, y=80)

        # Category
        select_category_Label = customtkinter.CTkLabel(self.productFrame, text='Category:',
                                                       font=('arial', 13, 'bold'),
                                                       fg_color='#FFFFFF', text_color='#0C0C0C')
        select_category_Label.grid(row=0, column=0, padx=8, pady=5, sticky=W)

        def combobox_values():

            connection = pymysql.connect(host='localhost', user='root', password='isaac', database='billing')
            cursor = connection.cursor()
            self.details_list = []
            try:
                query = "select * from products"
                cursor.execute(query)
                rows = cursor.fetchall()

                for row in rows:
                    index, details = row
                    current_details = details.split(', ')
                    self.details_list.extend(current_details)

            except Exception as e:
                messagebox.showerror("Error", f"{e}")

            finally:
                cursor.close()
                connection.close()

            return self.details_list

        value_details = combobox_values()

        self.combobox1_category = ttk.Combobox(self.productFrame, font=('arial', 8, 'bold'), width=13,
                                               state='readonly', height=20, values=value_details
                                               )

        # self.combobox1_category['values'] = value_details
        self.combobox1_category.set("Select Option")
        self.combobox1_category.bind('<<ComboboxSelected>>', lambda event: self.on_combobox_select())

        self.combobox1_category.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        # Product Name
        product_name_Label = customtkinter.CTkLabel(self.productFrame, text='Product Name:',
                                                    font=('arial', 13, 'bold'),
                                                    fg_color='#FFFFFF', text_color='#0C0C0C')
        product_name_Label.grid(row=0, column=2, padx=12, pady=5, sticky=W)

        self.product_name_entry = customtkinter.CTkEntry(self.productFrame, font=('arial', 13), width=140,
                                                         corner_radius=15, height=25,
                                                         border_color='#008B8B')
        # self.product_name_entry.configure(command=self.product_selection)
        self.product_name_entry.bind("<Return>", lambda event: self.on_enter_pressed_pname())
        self.product_name_entry.grid(row=0, column=3, padx=0, pady=6, sticky=W)

        # Product ID
        product_id_Label = customtkinter.CTkLabel(self.productFrame, text='Product ID:',
                                                  font=('arial', 13, 'bold'),
                                                  fg_color='#FFFFFF', text_color='#0C0C0C')
        product_id_Label.grid(row=0, column=4, padx=12, pady=5, sticky=W)

        self.product_id_entry = customtkinter.CTkEntry(self.productFrame, font=('arial', 13), width=80,
                                                       corner_radius=15, height=25,
                                                       border_color='#008B8B')
        self.product_id_entry.grid(row=0, column=5, padx=0, pady=6, sticky=W)
        # self.product_id_entry.bind("<Return>", lambda event: self.on_enter_pressed_pname())

        # price_rate
        rate_Label = customtkinter.CTkLabel(self.productFrame, text='Rate:',
                                            font=('arial', 13, 'bold'),
                                            fg_color='#FFFFFF', text_color='#0C0C0C')
        rate_Label.grid(row=0, column=6, padx=12, pady=5, sticky=W)

        self.rate_entry = customtkinter.CTkEntry(self.productFrame, font=('arial', 13), width=90,
                                                 corner_radius=15, height=25,
                                                 border_color='#008B8B')

        self.rate_entry.grid(row=0, column=7, padx=4, pady=6, sticky=W)
        # rate_entry_readonly_method(self.rate_entry, 'readonly')

        # quantity
        quantity_Label = customtkinter.CTkLabel(self.productFrame, text='QTY:',
                                                font=('arial', 13, 'bold'),
                                                fg_color='#FFFFFF', text_color='#0C0C0C')
        quantity_Label.grid(row=0, column=8, padx=12, pady=5, sticky=W)

        self.quantity_entry = customtkinter.CTkEntry(self.productFrame, font=('arial', 13), width=60,
                                                     corner_radius=15, height=25,
                                                     border_color='#008B8B')
        self.quantity_entry.bind("<Return>", lambda event: self.add_total_details_to_table())
        self.quantity_entry.grid(row=0, column=9, padx=6, pady=6, sticky=W)

        # add button
        self.add_total_button = customtkinter.CTkButton(self.customer_product_frame, text='Add',
                                                        text_color='#FFFFFF',
                                                        fg_color='#36719F', height=20, corner_radius=25, width=60,
                                                        cursor='hand2', hover_color='#FF4505', font=('arial', 14))
        self.add_total_button.configure(command=self.add_total_details_to_table)
        self.add_total_button.place(x=850, y=143)

        # ********************************** End *************************

        # ********************************** Bill Counter Frame *************************
        self.bill_counter_frame = customtkinter.CTkFrame(self.mainWindow, width=1000, height=130,
                                                         fg_color='#FFFFFF',
                                                         corner_radius=50, border_width=2, border_color='#00FFFF')

        self.bill_counter_frame.place(x=375, y=630)

        # ********** Bill Frame **************

        self.billFrame = LabelFrame(self.bill_counter_frame, text='Bill Counter', fg='#F60514', width=330,
                                    font=('Arial', 13, 'bold'), bg='#FFFFFF', border=2, height=110, )
        self.billFrame.place(x=20, y=10)

        # total

        total_Label = customtkinter.CTkLabel(self.billFrame, text='Total:',
                                             font=('arial', 13, 'bold'),
                                             fg_color='#FFFFFF', text_color='#0C0C0C')
        total_Label.place(x=5, y=10)

        self.total_entry = customtkinter.CTkEntry(self.billFrame, font=('arial', 13), width=100,
                                                  corner_radius=15, height=25,
                                                  border_color='#008B8B')
        self.total_entry.place(x=50, y=10)

        # Paid
        paid_Label = customtkinter.CTkLabel(self.billFrame, text='Paid:',
                                            font=('arial', 13, 'bold'),
                                            fg_color='#FFFFFF', text_color='#0C0C0C')
        paid_Label.place(x=170, y=10)

        self.paid_entry = customtkinter.CTkEntry(self.billFrame, font=('arial', 13), width=100,
                                                 corner_radius=15, height=25, border_color='#008B8B')
        self.paid_entry.bind("<Return>", lambda event: self.balance_method())
        self.paid_entry.place(x=210, y=10)

        # balance
        balance_Label = customtkinter.CTkLabel(self.billFrame, text='Balance:',
                                               font=('arial', 13, 'bold'),
                                               fg_color='#FFFFFF', text_color='#0C0C0C')
        balance_Label.place(x=60, y=55)

        self.balance_entry = customtkinter.CTkEntry(self.billFrame, font=('arial', 13), width=100,
                                                    corner_radius=15, height=25,
                                                    border_color='#008B8B')
        self.balance_entry.place(x=130, y=55)

        # ********** Buttons Frame **************

        self.buttonsFrame = customtkinter.CTkFrame(self.bill_counter_frame, width=600,
                                                   fg_color='#FFFFFF', height=100, )
        self.buttonsFrame.place(x=360, y=55)

        # generate button
        self.generate_bill_button = customtkinter.CTkButton(self.buttonsFrame, text='Generate Bill',
                                                            text_color='#FFFFFF',
                                                            fg_color='#36719F', height=40, corner_radius=25, width=100,
                                                            cursor='hand2', hover_color='#FF4505', font=('arial', 14))
        self.generate_bill_button.configure(command=lambda: self.text_area_method())
        self.generate_bill_button.grid(row=0, column=0, padx=3, ipadx=5)

        # Email Button
        self.email_bill_button = customtkinter.CTkButton(self.buttonsFrame, text='Email Bill',
                                                         text_color='#FFFFFF', command=self.email_bill_button_method,
                                                         fg_color='#36719F', height=40, corner_radius=25, width=100,
                                                         cursor='hand2', hover_color='#FF4505', font=('arial', 14))

        self.email_bill_button.grid(row=0, column=1, padx=3, ipadx=5)

        # save button
        # self.save_bill_button = customtkinter.CTkButton(self.buttonsFrame, text='Save Bill',
        #                                                 text_color='#FFFFFF',
        #                                                 fg_color='#36719F', height=40, corner_radius=25, width=100,
        #                                                 cursor='hand2', hover_color='#FF4505', font=('arial', 14))
        #
        # self.save_bill_button.configure(command=lambda: self.save_method())
        # self.save_bill_button.grid(row=0, column=2, padx=3, ipadx=5)

        # print button
        self.print_bill_button = customtkinter.CTkButton(self.buttonsFrame, text='Print Bill',
                                                         text_color='#FFFFFF', command=self.print_bill_method,
                                                         fg_color='#36719F', height=40, corner_radius=25, width=100,
                                                         cursor='hand2', hover_color='#FF4505', font=('arial', 14))
        self.print_bill_button.grid(row=0, column=2, padx=3, ipadx=5)

        # clear button
        self.Reset_bill_button = customtkinter.CTkButton(self.buttonsFrame, text='Reset',
                                                         text_color='#FFFFFF',
                                                         fg_color='#36719F', height=40, corner_radius=25, width=100,
                                                         cursor='hand2', hover_color='#FF4505', font=('arial', 14))
        self.Reset_bill_button.configure(command=lambda: self.resetMethod())
        self.Reset_bill_button.grid(row=0, column=3, padx=3, ipadx=5)

        # Exit button
        self.exit_bill_button = customtkinter.CTkButton(self.buttonsFrame, text='Exit Bill',
                                                        text_color='#FFFFFF', command=self.exit_method,
                                                        fg_color='#36719F', height=40, corner_radius=25, width=100,
                                                        cursor='hand2', hover_color='#FF4505', font=('arial', 14))
        self.exit_bill_button.grid(row=0, column=4, padx=3, ipadx=5)

        # ********************************** End *************************

        # self.customerFrame = customtkinter.CTkFrame(self.customer_product_frame, text='Customer Details',
        # fg='#F60514', width=400, font=('Arial', 13, 'bold'), bg='#FFFFFF', border=2, height=200)

        style = ttk.Style(self.mainWindow)
        style.theme_use('alt')
        # theme types alt, clam, classic, aqua
        style.configure('Treeview.Heading', background='light green', font=('arial', 10), relief=FLAT)
        style.configure('Treeview', font=('arial', 10), foreground='#fff', background='#000', fieldbackground='#313837')
        style.map('Treeview', background=[('selected', '#1A8F2D')])
        # style.map('Treeview', background=[('Selected', '#1A8F2D')])
        # style.map('Treeview.column', background=[('active', '#1A8F2D')])

        self.app_tree = ttk.Treeview(self.mainWindow, height=7, )
        self.app_tree['columns'] = ('Product ID', 'Product_Category', 'Product_Name', 'Price', 'Quantity', 'Total')

        self.app_tree.column('#0', width=0, stretch=tk.NO)
        self.app_tree.column("Product ID", anchor=tk.CENTER, width=100)
        self.app_tree.column("Product_Category", anchor=tk.CENTER, width=120)
        self.app_tree.column("Product_Name", anchor=tk.CENTER, width=130)
        self.app_tree.column("Price", anchor=tk.CENTER, width=90)
        self.app_tree.column("Quantity", anchor=tk.CENTER, width=80)
        self.app_tree.column("Total", anchor=tk.CENTER, width=70)

        self.app_tree.heading('Product ID', text='Product ID')
        self.app_tree.heading('Product_Category', text='Product_Category')
        self.app_tree.heading('Product_Name', text='Product_Name')
        self.app_tree.heading('Price', text='Price')
        self.app_tree.heading('Quantity', text='Quantity')
        self.app_tree.heading('Total', text='Total')

        self.app_tree.tag_configure('hovered', background='#1affff')

        self.app_tree.place(x=375, y=250)

        # ********************************** Bill Area Frame *************************
        self.bill_area_frame = customtkinter.CTkFrame(self.mainWindow, width=406, height=520, fg_color='#FFFFFF',
                                                      border_color='#00FFFF', border_width=2, corner_radius=25)
        self.bill_area_frame.place(x=960, y=80)

        bill_number_Label = customtkinter.CTkLabel(self.bill_area_frame, text='Bill Number:',
                                                   font=('arial', 15, 'bold'), width=100,
                                                   fg_color='#F60514', text_color='#FFFFFF')
        bill_number_Label.place(x=10, y=18)

        self.bill_number_entry = customtkinter.CTkEntry(self.bill_area_frame, font=('arial', 14), width=150,
                                                        corner_radius=15, height=35,
                                                        border_color='#008B8B')
        self.bill_number_entry.place(x=125, y=16)

        self.search_bill_button = customtkinter.CTkButton(self.bill_area_frame, text='Search',
                                                          text_color='#FFFFFF', command=self.search_method,
                                                          fg_color='#36719F', height=35, corner_radius=25, width=100,
                                                          cursor='hand2', hover_color='#FF4505', font=('arial', 14))
        self.search_bill_button.place(x=290, y=16)

        # ********** Bill Text Area Frame *****************
        text_bill_frame = LabelFrame(self.bill_area_frame, text='Bill Area', fg='#F60514',
                                     bg='#FFFFFF')
        text_bill_frame.place(x=10, y=60, width=390, height=430)
        titleFrame = customtkinter.CTkFrame(text_bill_frame, border_width=2, fg_color='white', width=340, height=40)
        titleFrame.pack(fill=X, padx=4, pady=2)
        # titleFrame.place( x=3, y=100)
        customtkinter.CTkLabel(titleFrame, text="Bill Receipt", font=('arial', 18, 'bold'), fg_color='white',
                               text_color='#008B8B', ).place(x=145, y=5)
        scrollbar1 = customtkinter.CTkScrollbar(text_bill_frame, orientation=VERTICAL, width=10)
        # scrollbar1.pack(side=RIGHT, fill=Y)

        self.text_Area = Text(text_bill_frame, bg='#FFFFFF', yscrollcommand=scrollbar1.set, width=46, height=22, )
        scrollbar1.pack(side=RIGHT, fill=Y)
        scrollbar1.configure(command=self.text_Area.yview)
        self.text_Area.place(x=5, y=50)

        # ********************************** End *************************
        self.mainWindow.bind("<Button-3>", lambda event: self.show_context_menu(event))
        self.context_menu()

    def __init__(self):

        self.exit_method = self.exit_method
        self.sender_email_entry = None
        self.sender_password_entry = None
        self.receiver_email_entry = None
        self.text_Area2 = None
        self.quitting = None
        self.send_gmail = self.send_gmail
        self.email_bill_button = None
        self.bill_no = None
        self.Reset_bill_button = None
        self.context_menu = self.context_menu
        self.delete_command = self.delete_command
        self.copy_command = self.copy_command
        self.update_total_entry = self.update_total_entry
        self.rate_entry = None
        self.add_total_details_to_table = self.add_total_details_to_table
        self.on_enter_pressed_pname = self.on_enter_pressed_pname
        self.details_list = None
        self.selectedItem = None
        self.add_total_button = None
        self.app_tree = None
        self.balance_entry = None
        self.paid_entry = None
        self.product_id_entry = None
        self.product_name_entry = None
        self.middleImage = None
        self.imageSize2 = None
        self.sub_total_entry = None
        self.customer_product_frame = None
        self.customerFrame = None
        self.mobileNoEntry = None
        self.customerNameEntry = None
        self.emailEntry = None
        self.addressEntry = None
        self.productFrame = None
        self.quantity_entry = None
        self.bill_counter_frame = None
        self.billFrame = None
        self.tax_entry = None
        self.total_entry = None
        self.buttonsFrame = None
        self.add_to_cart_button = None
        self.generate_bill_button = None
        self.save_bill_button = None
        self.print_bill_button = None
        self.clear_bill_button = None
        self.exit_bill_button = None
        self.bill_area_frame = None
        self.bill_number_entry = None
        self.search_bill_button = None
        self.text_Area = None
        self.combobox1_category = None

        # ***************** End of variables **************
        self.mainWindow = Tk()
        self.mainWindow.overrideredirect(True)
        self.mainWindow.iconbitmap("images2/icon2.ico")
        self.mainWindow.geometry('1366x768+0+0')
        self.mainWindow.resizable(False, False)
        # self.bg = ImageTk.PhotoImage(file='images2/bookkeeping-615384_1280.jpg')
        self.imageSize = (1366, 768)
        self.bg = resizing('images2/bookkeeping-615384_1280.jpg', self.imageSize)
        self.mainFrame = customtkinter.CTkFrame(self.mainWindow, width=1366, height=768)
        self.mainFrame.place(x=-1, y=-1)

        self.background_label = Label(self.mainWindow, text='', image=self.bg)

        self.background_label.place(x=-3, y=0)
        self.labelTime = Label(self.mainWindow, font=('times new roman', 16, 'bold'), background='white',
                               foreground='blue')
        self.labelTime.place(x=600, y=3, width=120, height=25)
        self.time()

        # ********************************** Header Frame *************************

        self.marquee_text = customtkinter.CTkLabel(self.mainWindow, text_color='#F60514', fg_color='#0095D5',
                                                   text='SMART COLLECTIONS BILLING SYSTEM',
                                                   font=('mv boli', 35, 'underline'))
        # self.mainWindow.wm_attributes('-transparent', '#0095D5')
        self.marquee_text.place(x=350, y=25)
        # ********************************** End *************************

        # ********************************** methods *************************
        self.mainMethod()
        # self.scroll_text()
        # self.add_context_menu()

        self.mainWindow.mainloop()
        # ********************************** End *************************

    def on_enter_pressed_pname(self):
        connection = pymysql.connect(host='localhost', user='root', password='isaac', database='billing')
        cursor = connection.cursor()
        try:
            if self.selectedItem != 'Select Option':
                selectedItem = self.selectedItem
                if selectedItem == "Shoes":
                    pName = self.product_name_entry.get()
                    query = f"select * from shoes where shoes_type like '%{pName}%'"
                    cursor.execute(query)
                    rows = cursor.fetchone()
                    if rows:
                        self.product_name_entry.delete(0, END)
                        self.product_id_entry.delete(0, END)
                        self.rate_entry.delete(0, END)

                        self.product_id_entry.insert(0, rows[0])
                        self.product_name_entry.insert(0, rows[1])
                        self.rate_entry.insert(0, rows[3])
                elif selectedItem == "clothes":
                    pName = self.product_name_entry.get()
                    query = f"select * from clothes where clothes_type like '%{pName}%'"
                    cursor.execute(query)
                    rows = cursor.fetchone()
                    if rows:
                        self.product_name_entry.delete(0, END)
                        self.product_id_entry.delete(0, END)
                        self.rate_entry.delete(0, END)

                        self.product_id_entry.insert(0, rows[0])
                        self.product_name_entry.insert(0, rows[1])
                        self.rate_entry.insert(0, rows[3])

                elif selectedItem == "Electronics":
                    pName = self.product_name_entry.get()
                    query = f"select * from electronics where electronics_type like '%{pName}%'"
                    cursor.execute(query)
                    rows = cursor.fetchone()
                    if rows:
                        self.product_name_entry.delete(0, END)
                        self.product_id_entry.delete(0, END)
                        self.rate_entry.delete(0, END)

                        self.product_id_entry.insert(0, rows[0])
                        self.product_name_entry.insert(0, rows[1])
                        self.rate_entry.insert(0, rows[3])

                elif selectedItem == "Groceries":
                    pName = self.product_name_entry.get()
                    query = f"select * from groceries where groceries_type like '%{pName}%'"
                    cursor.execute(query)
                    rows = cursor.fetchone()
                    if rows:
                        self.product_name_entry.delete(0, END)
                        self.product_id_entry.delete(0, END)
                        self.rate_entry.delete(0, END)

                        self.product_id_entry.insert(0, rows[0])
                        self.product_name_entry.insert(0, rows[1])
                        self.rate_entry.insert(0, rows[3])

            else:
                messagebox.showerror("Error", "Please select the category fast")

        except Exception as e:
            messagebox.showerror("Error", f"{e}")

    def add_total_details_to_table(self):
        quantity = self.quantity_entry.get()
        pname = self.product_name_entry.get()
        pId = self.product_id_entry.get()
        price = self.rate_entry.get()

        if self.selectedItem != 'Select Option' and self.selectedItem in self.details_list:
            if quantity != '' and pname != '' and pId != '' and price != '':
                if quantity.isnumeric():
                    if not quantity == '0':
                        price = float(price)
                        total = float(int(quantity) * int(price))
                        self.app_tree.insert("", "end", values=(pId, self.selectedItem, pname, price, quantity, total))
                        self.total_entry.delete(0, END)
                        self.update_total_entry()
                    else:
                        messagebox.showerror("Error", "quantity can't be 0")
                else:
                    messagebox.showerror('Error', "Quantity should be a valid Integer")
            else:
                messagebox.showerror('Error', "Please fill all the products field")

        else:
            messagebox.showerror('Error', "Please select product category")

    def update_total_entry(self):
        finalTotal = 0
        for x in self.app_tree.get_children():
            finalTotal += float(self.app_tree.item(x, 'values')[-1])
            self.total_entry.delete(0, END)
            self.total_entry.insert(0, finalTotal)

    # def add_context_menu(self):
    #     self.on_app_item_enter()
    def context_menu(self):
        self.context_menu = Menu(self.mainWindow, tearoff=False)
        self.context_menu.add_command(label="Copy", command=self.copy_command)
        # self.context_menu.configure(postcommand= lambda : self.copy_command())
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Delete", command=self.delete_command)

    def show_context_menu(self, event):
        item = self.app_tree.identify_row(event.y)
        if item:
            self.app_tree.selection_set(item)  # Highlight the right-clicked row
            self.context_menu.post(event.x_root, event.y_root)

    def delete_command(self):
        selected_item = self.app_tree.selection()
        if selected_item:
            self.app_tree.delete(selected_item)
            self.total_entry.delete(0, END)
            self.update_total_entry()

    def copy_command(self):
        messagebox.showinfo("INFO", "Copy will be integrated soon")

    def balance_method(self):
        paidAmount = float(self.paid_entry.get())
        totalAmount = float(self.total_entry.get())

        balance = paidAmount - totalAmount
        self.balance_entry.delete(0, END)
        self.balance_entry.insert(0, balance)

    def text_area_method(self):
        balance = self.balance_entry.get()
        amount_paid = self.paid_entry.get()
        total_amount = self.total_entry.get()

        number = self.mobileNoEntry.get()
        name = self.customerNameEntry.get()
        email = self.emailEntry.get()
        address = self.addressEntry.get()

        if balance == '' or amount_paid == '' or total_amount == '':
            messagebox.showerror("Error", "Transaction not done! \n Some Fields are Empty.")
            return
        amount_paid = float(amount_paid)
        total_amount = float(total_amount)
        balance = float(balance)

        if amount_paid == 0 or total_amount == 0:
            messagebox.showerror("Error", "Invalid Transaction, Total and Paid fields can't be 0")
            return

        if not balance.is_integer() or not amount_paid.is_integer() or not total_amount.is_integer():
            messagebox.showerror("Error", f"Invalid transaction, values should be integers!")
            return

        if number == '' or name == '' or email == '' or address == '':
            messagebox.showerror('Error', 'Customer details are blank.')
            return

        if name.isnumeric():
            messagebox.showerror('Error', 'Invalid Customer Name')
            return
        if not number.isnumeric():
            messagebox.showerror('Error', 'Invalid Customer Mobile Number')
            return
        if not is_valid_email(email):
            messagebox.showerror("Error", "Please enter a valid email address")

        current_datetime = datetime.now()
        current_date = current_datetime.strftime("%Y-%m-%d")
        current_time = current_datetime.strftime("%H:%M:%S %p")
        # current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.bill_no = random.randrange(100, 500)

        self.text_Area.tag_configure("head", font=("Courier", 13, "bold"), foreground="blue")
        self.text_Area.tag_configure("head2", font=("Courier", 11, "bold"))

        self.text_Area.delete(1.0, END)
        # self.text_Area.insert(END, "\n ============================================")
        self.text_Area.insert(END, " --------------------------------------------")
        self.text_Area.insert(END, "\n   ***SMART COLLECTIONS LIMITED***", "head")
        self.text_Area.insert(END, f"\n\n Date: {current_date}      Time: {current_time}")
        self.text_Area.insert(END, f"\n Bill Number: {self.bill_no}")
        self.text_Area.insert(END, f"\n Customer Name: {self.customerNameEntry.get()}")
        self.text_Area.insert(END, f"\n Phone Number: {self.mobileNoEntry.get()}")
        self.text_Area.insert(END, f"\n Customer Email: {self.emailEntry.get()}")
        self.text_Area.insert(END, f"\n Customer Address: {self.addressEntry.get()}")
        self.text_Area.insert(END, "\n ============================================")
        self.text_Area.insert(END, "\n Product            Price      Amount", "head2")
        self.text_Area.insert(END, "\n ============================================")
        self.text_Area.insert(END, "\n")

        for item in self.app_tree.get_children():
            values = self.app_tree.item(item, 'values')
            itemProduct, product, quantity, price, amount = values[0], values[2], values[4], values[3], \
                values[
                    -1]

            self.text_Area.insert(END, f" {product:<22} {quantity:<10} {price:<12}\n")

        # self.text_Area.insert(END, f"\n {product}")
        self.text_Area.insert(END, " ============================================")
        self.text_Area.insert(END, f"\n Total                   Ksh.{self.total_entry.get()}", "head2")
        self.text_Area.insert(END, f"\n Paid                    Ksh.{self.paid_entry.get()}", "head2")
        self.text_Area.insert(END, f"\n Balance                 Ksh.{self.balance_entry.get()}", "head2")
        self.text_Area.insert(END, f"\n\n\t***** Served by Isaac Ireri *****")
        self.text_Area.insert(END, f"\n\n            *** Please come again ***")
        self.text_Area.insert(END, "\n ============================================")
        self.save_method()

    def resetMethod(self):
        self.mobileNoEntry.delete(0, END)
        self.customerNameEntry.delete(0, END)
        self.emailEntry.delete(0, END)
        self.addressEntry.delete(0, END)
        self.product_name_entry.delete(0, END)
        self.product_id_entry.delete(0, END)
        self.rate_entry.delete(0, END)
        self.quantity_entry.delete(0, END)
        self.total_entry.delete(0, END)
        self.paid_entry.delete(0, END)
        self.balance_entry.delete(0, END)
        self.text_Area.delete(1.0, END)
        for item in self.app_tree.get_children():
            self.app_tree.delete(item)

    def save_method(self):

        if not os.path.exists('./bills'):
            os.mkdir('./bills')

        try:
            billContent = self.text_Area.get(1.0, END).strip()
            if billContent == '':
                messagebox.showerror("Failed", "Sorry, The  bill is Empty!")
                return

            else:
                response = messagebox.askyesno("Save Bill", "Do you want to save your bill?")
                if response:
                    files = open(f"bills/{self.customerNameEntry.get()}-{self.bill_no}", 'w')
                    files.write(billContent)
                    files.close()
                    messagebox.showinfo("Success", f"Bill {self.customerNameEntry.get()}-{self.bill_no} Saved "
                                                   f"Successfully.")

        except Exception as e:
            messagebox.askretrycancel("Retry", f"An Error occurred, would you like to try again? \n {e}")

    def print_bill_method(self):
        billContent = self.text_Area.get(1.0, END).strip()

        if billContent == "":
            messagebox.showerror('Error', 'Sorry, Bill is Empty')
            return
        else:
            file = tempfile.mktemp(f"{self.customerNameEntry.get()}-{self.bill_no}.txt")
            open(file, "w").write(billContent)
            os.startfile(file, 'print')
            messagebox.showinfo("Printed", "Successfully printed")

    def search_method(self):
        for i in os.listdir("./bills"):
            if i.split(".")[0] == self.bill_number_entry.get():
                with open(f"bills/{i}", "r") as files:
                    self.text_Area.delete(1.0, END)
                    for data in files:
                        self.text_Area.insert(END, data)
                    files.close()
                    break
        else:
            messagebox.showerror("Failed", f"Bill Number {self.bill_number_entry.get()} does not Exist")

    def email_bill_button_method(self):
        if self.text_Area.get(1.0, END) == ''.strip():
            messagebox.showerror("Failed", "Bill is empty")
            return
        else:
            window2 = Toplevel()
            window2.resizable(False, False)
            window2.grab_set()
            window2.geometry('430x620+450+70')
            window2.title('Send Gmail')
            window2.config(background='#15191C')
            # window2.overrideredirect(True)
            frame = LabelFrame(window2, bg='#15191C', height=600, text='SENDER', bd=5, fg='#9BCE2E',
                               font=('Consolas', 16, 'bold'), borderwidth=1, relief=GROOVE)
            sender_email_label = customtkinter.CTkLabel(frame, text='Sender\'s Email:',
                                                        font=('arial', 15),
                                                        fg_color='#15191C', text_color='#9BCE2E')
            sender_email_label.grid(row=0, column=0, pady=10, padx=10)

            self.sender_email_entry = customtkinter.CTkEntry(frame, border_color='#8DB22A', width=180,
                                                             height=30, border_width=1,
                                                             font=('consolas', 13), fg_color='#15191C',
                                                             corner_radius=20,
                                                             text_color='#FFF')
            self.sender_email_entry.grid(row=0, column=1, pady=10, padx=5)

            sender_password_label = customtkinter.CTkLabel(frame, text='Password:',
                                                           font=('arial', 15),
                                                           fg_color='#15191C', text_color='#9BCE2E')
            sender_password_label.grid(row=2, column=0, pady=10, padx=10)

            self.sender_password_entry = customtkinter.CTkEntry(frame, border_color='#8DB22A', width=180,
                                                                height=30, border_width=1, show='*',
                                                                font=('consolas', 13), fg_color='#15191C',
                                                                corner_radius=20,
                                                                text_color='#FFF')
            self.sender_password_entry.grid(row=2, column=1, pady=10, padx=5)

            frame.place(x=55, y=20)
            # ******************************* frame 2 ************************
            frame2 = LabelFrame(window2, bg='#15191C', text='RECIPIENT', bd=5, fg='#9BCE2E',
                                font=('Consolas', 16, 'bold'), borderwidth=1)
            receiver_email_label = customtkinter.CTkLabel(frame2, text='Email Address:',
                                                          font=('arial', 15),
                                                          fg_color='#15191C', text_color='#9BCE2E')
            receiver_email_label.grid(row=0, column=0, pady=10, padx=10)

            self.receiver_email_entry = customtkinter.CTkEntry(frame2, border_color='#8DB22A', width=180,
                                                               height=30, border_width=1,
                                                               font=('consolas', 13), fg_color='#15191C',
                                                               corner_radius=20,
                                                               text_color='#FFF')
            self.receiver_email_entry.grid(row=0, column=1, pady=10, padx=5)

            # message_label = customtkinter.CTkLabel(frame2, text='Message',
            #                                        font=('times new romans', 20, 'bold'),
            #                                        fg_color='#15191C', text_color='#9BCE2E')
            # message_label.grid(row=1, column=0, pady=10, padx=15)

            # scroll_bar_email = customtkinter.CTkScrollbar(frame2, orientation=VERTICAL)
            # scroll_bar_email.pack(side=RIGHT, fill=Y)

            frame2.place(x=55, y=160)

            frame3 = LabelFrame(window2, bg='#15191C', text='Body', bd=5, fg='#9BCE2E',
                                font=('Consolas', 16, 'bold'), borderwidth=1, width=100)
            frame3.place(x=20, y=250)
            scroll_bar_email2 = customtkinter.CTkScrollbar(frame3, orientation=HORIZONTAL, width=9)
            # scroll_bar_email2.pack(side=BOTTOM, fill=X)
            scroll_bar_email = customtkinter.CTkScrollbar(frame3, orientation=VERTICAL, width=10)
            scroll_bar_email.pack(side=RIGHT, fill=Y)  # Adjust the position based on your layout
            self.text_Area2 = Text(frame3, bg='#FFFFFF', width=47, height=14, yscrollcommand=scroll_bar_email.set,
                                   xscrollcommand=scroll_bar_email2.set)
            self.text_Area2.pack(pady=5, padx=5)
            scroll_bar_email2.configure(command=self.text_Area2.xview)
            scroll_bar_email.configure(command=self.text_Area2.yview)

            # Fetch content after creating text_Area2
            content = self.text_Area.get(1.0, "end-1c")
            self.text_Area2.delete(1.0, END)
            self.text_Area2.insert(END, content)

            send_button = customtkinter.CTkButton(window2, text='SEND', font=('Arial', 17), text_color='#fff',
                                                  fg_color='#05A312', hover_color='#00850B', bg_color='#161C25',
                                                  cursor='hand2',
                                                  corner_radius=15, width=150,
                                                  command=self.send_gmail)
            send_button.place(x=50, y=540)

            quit_button = customtkinter.CTkButton(window2, text='Quit', text_color='#fff', font=('Arial', 17,),
                                                  fg_color='#E40404', hover_color='#AE0000', border_color='#E40404',
                                                  border_width=2, corner_radius=15, bg_color='#161C25', cursor='hand2',
                                                  width=150, command=lambda: quit_method())

            quit_button.place(x=220, y=540)

        def quit_method():
            response = messagebox.askyesno("Exit", "Do you want to Exit?", parent=window2)
            if response:
                window2.destroy()

    def send_gmail(self):
        try:
            message = self.text_Area2.get(1.0, END)
            receiver = self.receiver_email_entry.get()
            sender = self.sender_email_entry.get()
            password = self.sender_password_entry.get()

            email_object = smtplib.SMTP("smtp.gmail.com", 587)
            email_object.starttls()
            email_object.login(sender, password)

            email_object.sendmail(sender, receiver, message)
            email_object.quit()
            messagebox.showinfo('Success', 'Email, Successfully Sent')

        except Exception as e:
            messagebox.showerror("Error", f"{e}")
            print(e)


if __name__ == '__main__':
    Main()
