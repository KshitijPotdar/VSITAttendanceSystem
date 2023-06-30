from tkinter import *
import tkinter as tk
from PIL import Image
from tkinter import ttk
from PIL import ImageTk
import pymysql
import time
import datetime
import calendar
from tkinter import messagebox
import cv2
import numpy
import sys
import os
from tkcalendar import Calendar,DateEntry
#from playsound import playsound 
import smtplib
import pandas as pd
import tkinter.filedialog as fd
import matplotlib.pyplot as plt

#==================================================================================================================================
#========================================================class login===============================================================
class login:
    def __init__(self):
        global login_window
        login_window = tk.Tk()
        login_window.title("   Smart Attendance Sytem")
        login_window.geometry("1350x700+50+50")
        login_window.configure(bg="black")
        login_window.resizable(False, False)
        login_window.iconbitmap("images/surveillance.ico")

        # =====bg image====
        self.bg = ImageTk.PhotoImage(Image.open("images/login_bg.png"))
        bg = Label(login_window, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        # ======left bg=======
        self.left = PhotoImage(file="images/left3.png")
        bg = Label(login_window, image=self.left).place(x=250, y=150, width=400, height=500)

        # =======images for sliders======
        self.img_title_bar = ImageTk.PhotoImage(Image.open("images/titlebar.png"))
        self.img1 = ImageTk.PhotoImage(Image.open("images/photo1.png"))
        self.img2 = ImageTk.PhotoImage(Image.open("images/photo2.png"))
        self.img3 = ImageTk.PhotoImage(Image.open("images/photo3.png"))
        self.img4 = ImageTk.PhotoImage(Image.open("images/photo4.png"))
        self.img5 = ImageTk.PhotoImage(Image.open("images/photo5.png"))

        # =======frame and heading=======
        frame_h = Frame(login_window, bg="white")
        frame_h.place(x=250, y=70, width=900, height=50)
        title_bar = Label(frame_h, image=self.img_title_bar).place(x=0, y=0, relwidth=1, relheight=1)
        title_heading = Label(frame_h, text="Smart Attendance System", font=("times new roman", 20, "bold"),
                              fg="#F94F05", bg="white").place(x=295, y=9)

        # =======left bg Frame photo=======
        frame2 = Frame(login_window, bg="white")
        frame2.place(x=350, y=310, width=200, height=170)

        # Create a label
        self.l = Label(frame2)
        self.l.place(x=0, y=0, width=190, height=169)

        # take a variable
        self.x = 1

        # create a function for moving a picture
        def move():  # name anything but meaningful
            global x
            if self.x == 6:
                self.x = 1
            if self.x == 1:
                self.l.config(image=self.img1)  # by writing this line first picture will appear
            elif self.x == 2:
                self.l.config(image=self.img2)
            elif self.x == 3:
                self.l.config(image=self.img3)
            elif self.x == 4:
                self.l.config(image=self.img4)
            elif self.x == 5:
                self.l.config(image=self.img5)
            elif self.x == 6:
                self.l.config(image=self.img6)
            # you can do it for thousands of images
            # now increase the count by one
            self.x += 1
            # set images to work automatically by "after" feature in tkinter
            frame2.after(2000, move)

        # Call the function
        move()

        # ======show pass image====
        #self.show_pass = PhotoImage(file="images/show_icon2.png")

        # ======Login frame=====
        frame1 = Frame(login_window, bg="white")
        frame1.place(x=650, y=150, width=500, height=500)

        # log=PhotoImage(file="images/log.png")
        memberlogin = Label(frame1, text="Member login", font=("times new roman", 24, "bold"), bg="white",
                            fg="#F36223").place(x=180, y=30)

        user_mail_label = Label(frame1, text="Email", font=("times new roman", 15, "bold"), bg="white",
                                fg="black").place(x=120, y=130)
        self.user_txt = Entry(frame1, font=("times new roman", 15), bg="#F1F1F1")
        self.user_txt.place(x=120, y=160, width=300)

        user_pass_label = Label(frame1, text="Password", font=("times new roman", 15, "bold"), bg="white",
                                fg="black").place(x=120, y=210)
        self.user_pass = Entry(frame1, show="*", font=("times new roman", 15), bg="#F1F1F1")
        self.user_pass.place(x=120, y=240, width=300)

        #show_pass = Button(frame1, image=self.show_pass, bd=False).place(x=386, y=240, width=35, height=26)

        # ====forgot btn|login btn=======
        btn_forget = Button(frame1, cursor="hand2", text="Forget Password.?", command=self.forgot_password_email,
                            font=("times new roman", 14, "underline"), bg="white", bd=0, fg="#B00857",
                            activebackground="white").place(x=120, y=290)
        btn_login = Button(frame1, cursor="hand2", text="Login", command=self.login,
                           font=("times new roman", 20, "bold"), bg="#00ff00", bd=0, fg="black",
                           activebackground="lightgreen").place(x=180, y=360, width=180, height=50)
        # ========admin login=========
        admin_login_button = Button(frame1, cursor="hand2", text="Admin Login", command=self.admin_login,
                                    font=("times new roman", 16, "underline"), bg="white", bd=0, fg="#B00857",
                                    activebackground="white").place(x=205, y=425)

        login_window.mainloop()
    def reset(self):
        self.fp_new.delete(0, END)
        self.fp_confirm.delete(0, END)
        self.user_txt.delete(0, END)
        self.user_pass.delete(0, END)


    def forget_password(self):  # still in progress
        if self.fp_new.get() == "" or self.fp_confirm.get() == "":
            messagebox.showerror("error", "All fields are required", parent=login_window)
        elif self.fp_new.get() != self.fp_confirm.get():
            messagebox.showerror("error", "New password and Confirm password should be same", parent=login_window)
        else:
            try:
                con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
                cur = con.cursor()
                cur.execute("select * from login_credentials where email=%s", self.user_txt.get())
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Please fill all fields", parent=login_window)
                else:
                    cur.execute("update login_credentials set password=%s where email=%s",
                                (self.fp_new.get(), self.user_txt.get()))
                    con.commit()
                    con.close()
                    messagebox.showinfo("success", "Password successfully changed.!!,please login with new password",
                                        parent=login_window)
                    self.reset()
            except Exception as es:
                messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=login_window)


    # sign in button /back button
    def sign_in(self):
        login_window.destroy()
    
    def forgot_password_email(self):
        if self.user_txt.get() == "":
            messagebox.showerror("Error", "Please enter the email address to reset yor password", parent=login_window)
        else:
            result = messagebox.askyesno("Forgot password","Do you want to retrieve password...?",parent=login_window)
            if result==True:
                #=======top level=========
                mailing_process = Toplevel()
                mailing_process.title("   Mailing Process")
                mailing_process.geometry("300x150+600+370")
                mailing_process.configure(bg="white")
                mailing_process.resizable(False, False)
                mailing_process.iconbitmap("images/surveillance.ico")
                mailing_process.focus_force()
                mailing_process.grab_set()

                self.progress = ttk.Progressbar(mailing_process, orient = HORIZONTAL,length = 200, mode = 'determinate')
                
                def destroy_bar():
                    mailing_process.destroy()
                

                def bar():
                    self.progress['value'] = 20
                    mailing_process.update_idletasks()
                    time.sleep(1)
                    pls_wait = Label(mailing_process, text = 'Please Wait....',font=("times new roman",12),fg="black", bg='white').place(x=100,y=65)
                
                    self.progress['value'] = 40
                    mailing_process.update_idletasks()
                    time.sleep(0.5)

                    #==========email to user(password) ================
                    user_email = self.user_txt.get()
                    #print(user_email)
                    query = "select name,password from login_credentials where email = '"+user_email+"';"
                    con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
                    cur = con.cursor()
                    cur.execute(query)
                    rows = cur.fetchone()
                    con.commit()
                    name = rows[0]
                    user_password = rows[1]
                    email = "smartattendance0@gmail.com"  # "email@domain.com"
                    password = "rohandarshit89"  # ""
                    # turn on less secure apps from gmail before sending mails
                    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                    server.login(email, password)
                    mail_subject = "Smart Attendance Password"
                    mail_body = "Hello " + name + ",\nYour password for smart_attendance is "+user_password
                    mail_message = 'Subject: {}\n\n{}'.format(mail_subject, mail_body)
                    server.sendmail(email, user_email, mail_message)
                    server.quit()
                
                    self.progress['value'] = 50
                    mailing_process.update_idletasks()
                    time.sleep(0.5)
                
                    self.progress['value'] = 60
                    mailing_process.update_idletasks()
                    time.sleep(0.5)
                
                    self.progress['value'] = 80
                    mailing_process.update_idletasks()
                    time.sleep(0.05)
                    pls_wait = Label(mailing_process, text = 'Mail sent successfully.!',font=("times new roman",12),fg="black", bg='white').place(x=85,y=65)
                    self.progress['value'] = 100
                    exit_btn = Button(mailing_process, text = 'Ok', command = destroy_bar,font=("times new roman",12,"bold"),bd=1,activebackground="white").place(x=135,y=105)
                

                self.progress.pack(pady=30)
                bar()
                

    # =============login================
    def login(self):
        global email,email_og
        if self.user_txt.get() == "" or self.user_pass.get() == "":
            messagebox.showerror("Error", "All fields are reqired", parent=login_window)
        else:
            try:
                con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
                cur = con.cursor()
                cur.execute("select * from login_credentials where email=%s and password=%s",
                            (self.user_txt.get(), self.user_pass.get()))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Username & Password", parent=login_window)
                else:
                    email_og= self.user_txt.get()
                    email = row[2]
                    #print(email)
                    login_window.destroy()
                    home()
                cur.close()
                con.close()
            except Exception as es:
                messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=login_window)


    def admin_login(self):
        # ==========admin login frame=======
        admin_login_frame = Frame(login_window, bg="white")
        admin_login_frame.place(x=650, y=150, width=500, height=500)

        # ==========admin login heading=======
        admin_login_label = Label(admin_login_frame, text="Admin Login", font=("times new roman", 24, "bold"), bg="white",
                                  fg="#F36223").place(x=180, y=30)

        admin_mail_label = Label(admin_login_frame, text="Email", font=("times new roman", 15, "bold"), bg="white",
                                 fg="black").place(x=120, y=130)
        self.admin_mail_txt = Entry(admin_login_frame, font=("times new roman", 15), bg="#F1F1F1")
        self.admin_mail_txt.place(x=120, y=160, width=300)

        admin_pass_label = Label(admin_login_frame, text="Password", font=("times new roman", 15, "bold"), bg="white",
                                 fg="black").place(x=120, y=210)
        self.admin_pass = Entry(admin_login_frame, show="*", font=("times new roman", 15), bg="#F1F1F1")
        self.admin_pass.place(x=120, y=240, width=300)

        # ====forgot btn|login btn=======
        admin_btn_login = Button(admin_login_frame, cursor="hand2", text="Admin Login", command=self.admin_login_page,
                                 font=("times new roman", 20, "bold"), bg="#00ff00", bd=0, fg="black",
                                 activebackground="lightgreen").place(x=180, y=360, width=180, height=50)

        

    #====================admin login=========================
    def admin_login_page(self):
        global email_admin
        if self.admin_mail_txt.get() == "" or self.admin_pass.get() == "":
            messagebox.showerror("Error", "All fields are reqired", parent=self.admin_login)
        else:
            try:
                con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
                cur = con.cursor()
                cur.execute("select * from admin_credentials where email=%s and password=%s",
                            (self.admin_mail_txt.get(), self.admin_pass.get()))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Username & Password", parent=self.admin_login)
                else:
                    email_admin=row[3]
                    login_window.destroy()
                    admin_page()
                cur.close()
                con.close()
            except Exception as es:
                messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.admin_login)









#=====================================================================================================================================
#=======================================================class home====================================================================
class home:
    def __init__(self):
        global email, home_window
        home_window = tk.Tk()
        home_window = home_window
        home_window.title("      Smart Attendance System")
        home_window.geometry("1350x700+50+50")
        home_window.resizable(False, False)
        home_window.iconbitmap("images/surveillance.ico")
        home_window.focus_force()
        home_window.grab_set()

        # =====welcome label====
        welcome = Label(home_window, text="Welcome  {}".format(email), font=("times new roman", 16, "bold"),
                        fg="black")
        welcome.place(x=1000, y=5)

        # =======button images======
        self.img_title_bar = ImageTk.PhotoImage(Image.open("images/titlebar.png"))
        self.img_capture = ImageTk.PhotoImage(Image.open("images/capture1-1.png"))
        self.img_view_attendance = ImageTk.PhotoImage(Image.open("images/view attendance1.png"))
        self.img_change_password = ImageTk.PhotoImage(Image.open("images/change password1.png"))
        self.img_about_us = ImageTk.PhotoImage(Image.open("images/about-us1.png"))
        self.img_create_dataset = ImageTk.PhotoImage(Image.open("images/report.png"))
        self.img_logout = ImageTk.PhotoImage(Image.open("images/logout1.png"))

        # =====home frame=======
        frame_home = Frame(home_window, bg="#7ec850")
        frame_home.place(x=80, y=60, width=1180, height=600)

        title_bar = Label(frame_home, bg="white").place(x=0, y=0, relwidth=1, height=60)
        title_heading = Label(frame_home, text="Smart Attendance System", font=("times new roman", 25, "bold"),
                              fg="#7ec850", bg="white").place(x=440, y=12)

        # ========1st row buttons=======
        capture_img_button = Button(frame_home, image=self.img_capture, command=self.take_attendance, cursor="hand2",
                                    bd=False).place(x=55, y=100, width=170, height=170)
        capture_label = Label(frame_home, text="Take Attendance", font=("times new roman", 16), fg="white",
                              bg="#7ec850").place(x=70, y=270)

        view_img_button = Button(frame_home, image=self.img_view_attendance, command=self.view_attendance,
                                 cursor="hand2", bd=False).place(x=355, y=100, width=170, height=170)
        view_label = Label(frame_home, text="View Attendance", font=("times new roman", 16), fg="white",
                           bg="#7ec850").place(x=365, y=270)

        change_password_img_button = Button(frame_home, image=self.img_change_password,
                                            command=self.forget_password_window, cursor="hand2", bd=False).place(x=655,
                                                                                                                 y=100,
                                                                                                                 width=170,
                                                                                                                 height=170)
        change_password_label = Label(frame_home, text="Change Password", font=("times new roman", 16), fg="white",
                                      bg="#7ec850").place(x=663, y=270)

        about_us_img_button = Button(frame_home, image=self.img_about_us, command=self.about_us, cursor="hand2",
                                     bd=False).place(x=955, y=100, width=170, height=170)
        about_us_label = Label(frame_home, text="About US", font=("times new roman", 16), fg="white",
                               bg="#7ec850").place(x=990, y=270)

        # ===========2nd row buttons=============

        created_dataset_button = Button(frame_home, image=self.img_create_dataset, command=self.Analyze_attendance,
                                        cursor="hand2", bd=False).place(x=55, y=350, width=170, height=170)
        created_dataset_label = Label(frame_home, text="Analyze Attendance", font=("times new roman", 16), fg="white",
                                      bg="#7ec850").place(x=55, y=520)

        logout_button = Button(frame_home, image=self.img_logout, command=self.logout, cursor="hand2", bd=False).place(
            x=355, y=350, width=170, height=170)
        logout_label = Label(frame_home, text="Logout", font=("times new roman", 16), fg="white", bg="#7ec850").place(
            x=405, y=520)

        # ========digital clock=======
        # ======hr label=====
        lbl_hr = Label(frame_home, text="12", font=("times new roman", 40, "bold"), bg="#0875B7", fg="white")
        lbl_hr.place(x=700, y=380, width=80, height=85)

        lbl_hr2 = Label(frame_home, text="HOUR", font=("times new roman", 12, "bold"), bg="#0875B7", fg="white")
        lbl_hr2.place(x=700, y=475, width=80, height=30)

        lbl_date = Label(frame_home, text="DATE", font=("times new roman", 12, "bold"), bg="#0875B7", fg="white")
        lbl_date.place(x=700, y=515, width=80, height=30)

        # ======min label====
        lbl_min = Label(frame_home, text="00", font=("times new roman", 40, "bold"), bg="#008EA4", fg="white")
        lbl_min.place(x=790, y=380, width=80, height=85)

        lbl_min2 = Label(frame_home, text="MINUTES", font=("times new roman", 12, "bold"), bg="#008EA4", fg="white")
        lbl_min2.place(x=790, y=475, width=80, height=30)

        lbl_month = Label(frame_home, text="MONTH", font=("times new roman", 12, "bold"), bg="#008EA4", fg="white")
        lbl_month.place(x=790, y=515, width=80, height=30)

        # ======sec label===
        lbl_sec = Label(frame_home, text="00", font=("times new roman", 40, "bold"), bg="#DF002A", fg="white")
        lbl_sec.place(x=880, y=380, width=80, height=85)

        lbl_sec2 = Label(frame_home, text="SECONDS", font=("times new roman", 12, "bold"), bg="#DF002A", fg="white")
        lbl_sec2.place(x=880, y=475, width=80, height=30)

        lbl_year = Label(frame_home, text="YEAR", font=("times new roman", 12, "bold"), bg="#DF002A", fg="white")
        lbl_year.place(x=880, y=515, width=80, height=30)

        # =======am/pm======
        lbl_am_pm = Label(frame_home, text="AM", font=("times new roman", 35, "bold"), bg="#DF002A", fg="white")
        lbl_am_pm.place(x=970, y=380, width=80, height=85)

        lbl_am_pm2 = Label(frame_home, text="NOON", font=("times new roman", 12, "bold"), bg="#DF002A", fg="white")
        lbl_am_pm2.place(x=970, y=475, width=80, height=30)

        lbl_Date2 = Label(frame_home, text="DATE", font=("times new roman", 12, "bold"), bg="#DF002A", fg="white")
        lbl_Date2.place(x=970, y=515, width=80, height=30)

        def clock():
            # =====time======
            h = str(time.strftime("%H"))
            m = str(time.strftime("%M"))
            s = str(time.strftime("%S"))

            # =====date=====
            dd = str(time.strftime("%d"))
            mm = int(time.strftime("%m"))
            mm = calendar.month_name[mm]
            yy = datetime.datetime.now()

            lbl_date.config(text=dd)
            lbl_month.config(text=str(mm))
            lbl_year.config(text=str(yy.year))

            # print(h,m,s)
            if int(h) > 12 and int(m) > 0:
                lbl_am_pm.config(text="PM")

            if int(h) > 12:
                h = str((int(h) - 12))

            lbl_hr.config(text=h)
            lbl_min.config(text=m)
            lbl_sec.config(text=s)

            lbl_hr2.after(200, clock)

        clock()



    #===========================take attendance window==========================
    def take_attendance(self):
        self.root_take_attendance = Toplevel()
        self.root_take_attendance.title("Take Attendance")
        self.root_take_attendance.geometry("1000x550+250+200")
        self.root_take_attendance.iconbitmap("images/surveillance.ico")
        self.root_take_attendance.resizable(False, False)
        self.root_take_attendance.focus_force()
        self.root_take_attendance.grab_set()

        # =========take attendance variable===========
        self.student_id_var = StringVar()
        self.section_combobox_var = StringVar()
        self.course_combobox_var = StringVar()
        self.div_combobox_var = StringVar()
        self.subject_var = StringVar()
        self.class_code_take_entry_var = StringVar()

        take_attendance_frame = Frame(self.root_take_attendance, bg="#7ec850")
        take_attendance_frame.place(x=0, y=0, relwidth=1, relheight=1)

        title_bar = Label(take_attendance_frame, bg="white").place(x=0, y=0, relwidth=1, height=60)
        take_attendance_heading = Label(take_attendance_frame, text="Take Attendance",
                                        font=("times new roman", 25, "bold"), fg="#7ec850", bg="white")
        take_attendance_heading.pack()

        id_label = Label(take_attendance_frame, text="STUDENT-ID", font=("times new roman", 16, "bold"), fg="white",
                         bg="#7ec850")
        id_label.place(x=35, y=100)

        id_label_entry = Entry(take_attendance_frame, textvariable=self.student_id_var, bd=0,
                               font=("times new roman", 16, "bold"), fg="black", bg="white", justify=CENTER)
        id_label_entry.place(x=200, y=100, width=150)

        #=============comment id manually=============
        id_comment_label = Label(take_attendance_frame, text="[ Add student id for manual attendance only! ]", font=("times new roman", 16, "bold"), fg="white",
                         bg="#7ec850")
        id_comment_label.place(x=360, y=100)


        section_label = Label(take_attendance_frame, text="SECTION", font=("times new roman", 16, "bold"), fg="white",
                              bg="#7ec850")
        section_label.place(x=35, y=150)

        section_combobox = ttk.Combobox(take_attendance_frame, textvariable=self.section_combobox_var,
                                        font=("times new roman", 15), state="readonly", justify=CENTER)
        section_combobox['values'] = ("IT", "commerce")
        section_combobox.place(x=200, y=150, width=150)
        section_combobox.current()

        course_label = Label(take_attendance_frame, text="ClASS", font=("times new roman", 16, "bold"), fg="white",
                             bg="#7ec850")
        course_label.place(x=35, y=200)

        course_combobox = ttk.Combobox(take_attendance_frame, textvariable=self.course_combobox_var,
                                       font=("times new roman", 15), state="readonly", justify=CENTER)
        course_combobox['values'] = ("Bsc-IT", "Msc-IT", "BMS", "BAF", "M-com")
        course_combobox.place(x=200, y=200, width=150)
        course_combobox.current()

        div_label = Label(take_attendance_frame, text="DIV", font=("times new roman", 16, "bold"), fg="white",
                          bg="#7ec850")
        div_label.place(x=35, y=250)

        div_combobox = ttk.Combobox(take_attendance_frame, textvariable=self.div_combobox_var,
                                    font=("times new roman", 15), state="readonly", justify=CENTER)
        div_combobox['values'] = ("A", "B", "C", "D", "E", "F")
        div_combobox.place(x=200, y=250, width=150)
        div_combobox.current()

        subject_label = Label(take_attendance_frame, text="SUBJECT", font=("times new roman", 16, "bold"), fg="white",
                              bg="#7ec850")
        subject_label.place(x=35, y=300)

        subject_entry = Entry(take_attendance_frame, textvariable=self.subject_var, bd=0,
                              font=("times new roman", 16, "bold"), fg="black", bg="white", justify=CENTER)
        subject_entry.place(x=200, y=300, width=150)

        class_code_label = Label(take_attendance_frame, text="CLASS-CODE", font=("times new roman", 16, "bold"),
                                 fg="white", bg="#7ec850")
        class_code_label.place(x=35, y=350)

        class_code_take_entry = Entry(take_attendance_frame, textvariable=self.class_code_take_entry_var, bd=0,
                                      font=("times new roman", 16, "bold"), fg="black", bg="white", justify=CENTER)
        class_code_take_entry.place(x=200, y=350, width=150)

        camera_button = Button(take_attendance_frame, text="Camera", bd=2, cursor="hand2", command=self.opencamera,
                               font=("times new roman", 16, "bold"), fg="white", bg="#2A908F",
                               activebackground="#173F5F")
        camera_button.place(x=40, y=450)
        capture_button = Button(take_attendance_frame, text="Add Manually", bd=2, cursor="hand2",
                                command=self.addStudentManually, font=("times new roman", 16, "bold"), fg="white",
                                bg="#bd2000", activebackground="red")
        capture_button.place(x=160, y=450)

    # =======print data=============
    def print_data(self):
        print(self.section_combobox_var.get(), self.course_combobox_var.get(), self.div_combobox_var.get(),
              self.subject_var.get(), self.class_code_take_entry_var.get())

    # ======getting name============
    def getting_name(self):
        print(self.names[:])

    # ==========manual attendance function===========
    def addStudentManually(self):
        if (
                self.student_id_var.get() == "" or self.class_code_take_entry_var.get() == "" or self.section_combobox_var.get() == "" or self.course_combobox_var.get() == "" or self.div_combobox_var.get() == "" or self.subject_var.get() == ""):
            messagebox.showerror("Error", "All Fields are required", parent=self.root_take_attendance)
        else:
            # fetching student record
            con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
            cur = con.cursor()
            query = "select * from students where id = '" + self.student_id_var.get() + "';"
            cur.execute(query)
            rows = cur.fetchall()
            if (len(rows) > 0):
                student_username = ""
                student_name = ""
                student_email = ""
                student_contact = ""
                for row in rows:
                    student_username = row[1]
                    student_name = row[2]
                    student_email = row[3]
                    student_contact = row[4]
                date = str(datetime.datetime.now()).split()
                today = date[0]
                # inserting into db
                con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
                cur = con.cursor()

                query = "UPDATE attendance SET status = 'present' where id = '"+self.student_id_var.get()+"' and course = '"+self.course_combobox_var.get()+"' and divison = '"+self.div_combobox_var.get()+"' and subject = '"+self.subject_var.get()+"' and class_code = '"+self.class_code_take_entry_var.get()+"' and date = '"+today+"';"
                '''values = (
                    self.student_id_var.get(), student_username, student_name, student_email, student_contact,
                    self.course_combobox_var.get(),
                    self.div_combobox_var.get(), self.class_code_take_entry_var.get(), self.subject_var.get(),
                    "present", today)'''
                cur.execute(query)
                con.commit()
                con.close()

                messagebox.showinfo("", "Attendance for " + student_name + " added successfully!",
                                    parent=self.root_take_attendance)
            else:
                messagebox.showerror("Error", "invalid student ID", parent=self.root_take_attendance)

    # =============mark attendance function=====
    def markAtt(self, names):
        # fetching student record
        con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
        cur = con.cursor()
        # query = "select * from students where id = '" + name + "';"
        query = "select * from students"
        cur.execute(query)
        rows = cur.fetchall()
        student_id = ""
        student_username = ""
        student_name = ""
        student_email = ""
        student_contact = ""
        for row in rows:
            student_id = row[0]
            student_username = row[1]
            student_name = row[2]
            student_email = row[3]
            student_contact = row[4]

            date = str(datetime.datetime.now()).split()
            today = date[0]

            # inserting into db

            con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
            cur = con.cursor()
            query = "INSERT INTO attendance VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (
                student_id, student_username, student_name, student_email, student_contact,
                self.course_combobox_var.get(),
                self.div_combobox_var.get(), self.class_code_take_entry_var.get(), self.subject_var.get(), "absent",
                today)
            cur.execute(query, values)
            con.commit()
            con.close()

        present_students = list(set(names))
        # print(present_students)
        for name in present_students:
            # updating present students
            con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
            cur = con.cursor()
            query = "update attendance set status = 'present' where id = '" + name + "';"
            cur.execute(query)
            con.commit()
            con.close()
        messagebox.showinfo("", "Attendance Successfully Recorded!\n\nStudents Count: " + str(len(present_students)),
                            parent=self.root_take_attendance)

        # mailing students
        query = "select name,email,status from attendance where course = '" + self.course_combobox_var.get() + "' and date = '" + today + "';"
        con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
        cur = con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        #=======top level=========
        mailing_process = Toplevel()
        mailing_process.title("   Mailing Process")
        mailing_process.geometry("300x150+600+370")
        mailing_process.configure(bg="white")
        mailing_process.resizable(False, False)
        mailing_process.iconbitmap("images/surveillance.ico")
        mailing_process.focus_force()
        mailing_process.grab_set()

        self.progress = ttk.Progressbar(mailing_process, orient = HORIZONTAL,length = 200, mode = 'determinate')
        
        def destroy_bar():
            mailing_process.destroy()
        

        def bar():
            self.progress['value'] = 20
            mailing_process.update_idletasks()
            time.sleep(1)
            pls_wait = Label(mailing_process, text = 'Please Wait....',font=("times new roman",12),fg="black", bg='white').place(x=100,y=65)
        
            self.progress['value'] = 40
            mailing_process.update_idletasks()
            time.sleep(0.5)

            #============email to everyone===========

            for row in rows:
                name = row[0]
                email_to = row[1]
                attendance_status = row[2]
                #print(name,email_to,attendance_status)
                email = "smartattendance0@gmail.com"  # "email@domain.com"
                password = "rohandarshit89"  # ""

                # turn on less secure apps from gmail before sending mails
                server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                server.login(email, password)

                to = ""
                mail_subject = "Smart Attendance Status"
                mail_body = "Hello " + name + ",\nAttendance for :\nDate: " + today + "\nSubject: " + self.subject_var.get() + "\nStatus: " + attendance_status
                mail_message = 'Subject: {}\n\n{}'.format(mail_subject, mail_body)

                server.sendmail(email, email_to, mail_message)
                server.quit()
        
            self.progress['value'] = 50
            mailing_process.update_idletasks()
            time.sleep(0.5)
        
            self.progress['value'] = 60
            mailing_process.update_idletasks()
            time.sleep(0.5)
        
            self.progress['value'] = 80
            mailing_process.update_idletasks()
            time.sleep(0.05)
            pls_wait = Label(mailing_process, text = 'Mail sent successfully.!',font=("times new roman",12),fg="black", bg='white').place(x=85,y=65)
            self.progress['value'] = 100
            exit_btn = Button(mailing_process, text = 'Ok', command = destroy_bar,font=("times new roman",12,"bold"),bd=1,activebackground="white").place(x=135,y=105)
        

        self.progress.pack(pady=30)
        bar()
        
        

        
    #===========================opens camera=====================
    def opencamera(self):

        if (
                self.class_code_take_entry_var.get() == "" or self.section_combobox_var.get() == "" or self.course_combobox_var.get() == "" or self.div_combobox_var.get() == "" or self.subject_var.get() == ""):
            messagebox.showerror("Error", "All Fields are required", parent=self.root_take_attendance)
        else:
            rel = messagebox.askyesno("Confirmation","Are you sure you want to continue..?",parent=self.root_take_attendance)
            if rel==True:    
                # code for face recognition
                size = 4
                haar_file = 'haarcascade_frontalface_default.xml'
                datasets = 'datasets'
                # Part 1: Create fisherRecognizer
                print('Recognizing Face Please Be in sufficient Lights...')

                (images, lables, names, id) = ([], [], {}, 0)
                for (subdirs, dirs, files) in os.walk(datasets):
                    for subdir in dirs:
                        names[id] = subdir
                        subjectpath = os.path.join(datasets, subdir)
                        for filename in os.listdir(subjectpath):
                            path = subjectpath + '/' + filename
                            lable = id
                            images.append(cv2.imread(path, 0))
                            lables.append(int(lable))
                        id += 1
                (width, height) = (130, 100)

                # Create a Numpy array from the two lists above
                (images, lables) = [numpy.array(lis) for lis in [images, lables]]

                # OpenCV trains a model from the images
                # NOTE FOR OpenCV2: remove '.face'
                model = cv2.face.LBPHFaceRecognizer_create()
                model.train(images, lables)

                # Part 2: Use fisherRecognizer on camera stream
                face_cascade = cv2.CascadeClassifier(haar_file)
                webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                while True:
                    (_, im) = webcam.read()
                    cv2.putText(im, '[Press space-key to exit]', (400, 460), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                    all_names = []
                    for (x, y, w, h) in faces:
                        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        face = gray[y:y + h, x:x + w]
                        face_resize = cv2.resize(face, (width, height))
                        # Try to recognize the face
                        prediction = model.predict(face_resize)
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)

                        if (prediction[1] < 77):
                            cv2.putText(im, '% s - %.0f' % (names[prediction[0]], prediction[1]), (x - 10, y - 10),
                                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                            # markAttendance(names[prediction[0]])
                            all_names.append(names[prediction[0]])


                        else:
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 3)
                            cv2.putText(im, 'Unknown', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
                            '''cv2.rectangle(im,(x, y), (x + w, y + h), (0, 0, 255), 3)
                            cv2.putText(im, 'not recognized',
                                        (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))'''

                    cv2.imshow('Camera', im)
                    key = cv2.waitKey(1)
                    if key == ord(' '):
                        break
                webcam.release()
                cv2.destroyAllWindows()
                self.markAtt(all_names)




    #=======================================view attendance==================================
    def view_attendance(self):
        self.root_view_attendance = Toplevel()
        self.root_view_attendance.title("view attendance")
        self.root_view_attendance.geometry("900x550+300+180")
        self.root_view_attendance.config(bg="white")
        self.root_view_attendance.iconbitmap("images/surveillance.ico")
        self.root_view_attendance.resizable(False, False)
        self.root_view_attendance.focus_force()
        self.root_view_attendance.grab_set()

        # =========class-code Variable===========
        self.date_var = StringVar()
        self.class_code_var = StringVar()
        self.course_combobox_view_var = StringVar()
        self.div_view_var = StringVar()
        self.subject_view_var = StringVar()

        take_attendance_heading = Label(self.root_view_attendance, text="View Attendance",
                                        font=("times new roman", 30, "bold"), fg="#7ec850", bg="white")
        take_attendance_heading.pack()

        # =====view attendance frame======
        view_attendance_frame = Frame(self.root_view_attendance, bg="#7ec850")
        view_attendance_frame.place(x=5, y=60, width=300, height=485)

        date_view = Label(view_attendance_frame, text="Date", font=("times new roman", 16, "bold"),
                          fg="white", bg="#7ec850")
        date_view.place(x=5, y=50)

        date_view_entry_view = DateEntry(view_attendance_frame, font=("times new roman", 16, "bold"),
                                         date_pattern='y-mm-dd', bg="white", fg="black", textvariable=self.date_var,
                                         justify=CENTER)
        date_view_entry_view.place(x=120, y=50, width=150)

        course_view = Label(view_attendance_frame, text="Course", font=("times new roman", 16, "bold"),
                            fg="white", bg="#7ec850")
        course_view.place(x=5, y=100)

        course_combobox_view = ttk.Combobox(view_attendance_frame, textvariable=self.course_combobox_view_var,
                                            font=("times new roman", 15), state="readonly", justify=CENTER)
        course_combobox_view['values'] = ("Bsc-IT", "Msc-IT", "BMS", "BAF", "M-com")
        course_combobox_view.place(x=120, y=100, width=150)
        course_combobox_view.current()

        class_code_view = Label(view_attendance_frame, text="Class-Code", font=("times new roman", 16, "bold"),
                                fg="white", bg="#7ec850")
        class_code_view.place(x=5, y=150)

        class_code_entry_view = Entry(view_attendance_frame, bd=0, textvariable=self.class_code_var,
                                      font=("times new roman", 16, "bold"), fg="black", bg="white", justify=CENTER)
        class_code_entry_view.place(x=120, y=150, width=150)

        div_view_label = Label(view_attendance_frame, text="Div", font=("times new roman", 16, "bold"),
                               fg="white", bg="#7ec850")
        div_view_label.place(x=5, y=200)

        div_view = ttk.Combobox(view_attendance_frame, textvariable=self.div_view_var,
                                font=("times new roman", 15), state="readonly", justify=CENTER)
        div_view['values'] = ("A", "B", "C", "D", "E", "F")
        div_view.place(x=120, y=200, width=150)
        div_view.current()

        subject_view = Label(view_attendance_frame, text="Subject", font=("times new roman", 16, "bold"),
                             fg="white", bg="#7ec850")
        subject_view.place(x=5, y=250)

        subject_view_entry_view = Entry(view_attendance_frame, bd=0, textvariable=self.subject_view_var,
                                        font=("times new roman", 16, "bold"), fg="black", bg="white", justify=CENTER)
        subject_view_entry_view.place(x=120, y=250, width=150)


        # ===============view and export attendance button===============

        view_attendance_button = Button(view_attendance_frame, text="View", command=self.fetch_data, bd=2,
                                        cursor="hand2", font=("times new roman", 16, "bold"), fg="white", bg="#2A908F",
                                        activebackground="#173F5F")
        view_attendance_button.place(x=40, y=325, width=100)

        view_clear_button = Button(view_attendance_frame, text="clear", command=self.clear, bd=2,
                                   cursor="hand2", font=("times new roman", 16, "bold"), fg="white", bg="#2A908F",
                                   activebackground="#173F5F")
        view_clear_button.place(x=160, y=325, width=100)

        download_attendance_button = Button(view_attendance_frame, text="Export-File", command=self.export_to_csv, bd=2,
                                            cursor="hand2",
                                            font=("times new roman", 12, "bold"), fg="white", bg="#bd2000",
                                            activebackground="red")
        download_attendance_button.place(x=70, y=400, width=150)



        # ======view attendance frame2=====
        view_attendance_frame2 = Frame(self.root_view_attendance, bg="white")
        view_attendance_frame2.place(x=310, y=60, width=585, height=485)

        scroll_x = Scrollbar(view_attendance_frame2, cursor="hand2", orient=HORIZONTAL)
        scroll_y = Scrollbar(view_attendance_frame2, cursor="hand2", orient=VERTICAL)
        self.view_attendance_table = ttk.Treeview(view_attendance_frame2, columns=(
            "id", "username", "name", "email", "contact", "course", "divison", "class_code", "subject", "status",
            "date"),
                                                  xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.view_attendance_table.xview)
        scroll_y.config(command=self.view_attendance_table.yview)
        self.view_attendance_table.heading("id", text="ID")
        self.view_attendance_table.heading("username", text="Username")
        self.view_attendance_table.heading("name", text="Name")
        self.view_attendance_table.heading("email", text="E-mail")
        self.view_attendance_table.heading("contact", text="Phone")
        self.view_attendance_table.heading("course", text="Course")
        self.view_attendance_table.heading("divison", text="DIV")
        self.view_attendance_table.heading("class_code", text="Class-code")
        self.view_attendance_table.heading("subject", text="Subject")
        self.view_attendance_table.heading("status", text="Status")
        self.view_attendance_table.heading("date", text="Date")
        self.view_attendance_table['show'] = 'headings'
        self.view_attendance_table.column("id", width=90)
        self.view_attendance_table.column("username", width=150)
        self.view_attendance_table.column("name", width=110)
        self.view_attendance_table.column("email", width=190)
        self.view_attendance_table.column("contact", width=160)
        self.view_attendance_table.column("course", width=120)
        self.view_attendance_table.column("divison", width=60)
        self.view_attendance_table.column("class_code", width=150)
        self.view_attendance_table.column("subject", width=150)
        self.view_attendance_table.column("status", width=150)
        self.view_attendance_table.column("date", width=150)
        self.view_attendance_table.pack(fill=BOTH, expand=1)


    #=====================fetch data====================
    def fetch_data(self):
        if self.date_var.get() == "" or self.class_code_var.get() == "" or self.div_view_var.get() == "" or self.course_combobox_view_var.get() == "" or self.subject_view_var.get() == "":
            messagebox.showerror("error", "All fields are required!!", parent=self.root_view_attendance)
        else:
            try:
                con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
                cur = con.cursor()
                cur.execute(
                    "select * from attendance where class_code=%s and divison=%s and course=%s and subject=%s and date=%s",
                    (self.class_code_var.get(), self.div_view_var.get(), self.course_combobox_view_var.get(),
                     self.subject_view_var.get(), self.date_var.get()))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "No Data Found", parent=self.root_view_attendance)
                    # self.clear()
                else:
                    cur.execute(
                        "select * from attendance where class_code=%s and divison=%s and course=%s and subject=%s and date=%s",
                        (self.class_code_var.get(), self.div_view_var.get(), self.course_combobox_view_var.get(),
                         self.subject_view_var.get(), self.date_var.get()))
                    rows = cur.fetchall()
                    if len(rows) != 0:
                        self.view_attendance_table.delete(*self.view_attendance_table.get_children())
                        for row in rows:
                            self.view_attendance_table.insert('', END, values=row)
                        con.commit()
                    con.close()
                    messagebox.showinfo("", "Match found!\n\nStudents Count: " + str(len(rows)),
                                        parent=self.root_view_attendance)
                    # self.clear()
            except Exception as es:
                messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root_view_attendance)

    # =======export to csv========
    def export_to_csv(self):
        if self.date_var.get() == "" or self.class_code_var.get() == "" or self.div_view_var.get() == "" or self.course_combobox_view_var.get() == "" or self.subject_view_var.get() == "":
            messagebox.showerror("error", "All fields are required!!", parent=self.root_view_attendance)
        else:
            con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
            select_query = "select * from attendance where class_code='" + self.class_code_var.get() + "' and divison='" + self.div_view_var.get() + "' and course='" + self.course_combobox_view_var.get() + "' and subject='" + self.subject_view_var.get() + "' and date='" + self.date_var.get() + "';"
            sql_query = pd.read_sql_query(select_query, con)
            df = pd.DataFrame(sql_query)
            if df.empty:
                messagebox.showerror("Error", "No Data Found!", parent=self.root_view_attendance)
            else:
                df.drop(["username", "email", "contact"], axis=1, inplace=True)
                # print(df.iloc[:,0])
                date = str(datetime.datetime.now()).split()
                currdir = os.getcwd()
                tempdir2 = fd.askdirectory(parent=self.root_view_attendance, initialdir=currdir,
                                           title='Please select a directory to save output file')
                file_name = date[0] + "_" + self.subject_view_var.get() + ".csv"
                output = tempdir2 + "/" + file_name
                df.to_csv(output)
                messagebox.showinfo("Exported", "Data exported to CSV Successfully!\nFile Location: " + output,
                                    parent=self.root_view_attendance)
            con.close()

    def clear(self):
        self.class_code_var.set("")
        self.div_view_var.set("-SELECT-")
        self.course_combobox_view_var.set("-SELECT-")
        self.subject_view_var.set("")
        self.date_var.set("yy-mm-dd")
        self.view_attendance_table.delete(*self.view_attendance_table.get_children())

    def reset(self):
        self.fp_new.delete(0, END)
        self.fp_confirm.delete(0, END)
        

    #===========change password function=================
    def change_password(self):
        if self.fp_new.get() == "" or self.fp_confirm.get() == "":
            messagebox.showerror("error", "All fields are required", parent=self.root_change_password)
        elif self.fp_new.get() != self.fp_confirm.get():
            messagebox.showerror("error", "New password and Confirm password should be same",
                                 parent=self.root_change_password)
        else:
            try:
                con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
                cur = con.cursor()
                cur.execute("select * from login_credentials where email=%s", email_og)
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Please fill all fields", parent=self.root_change_password)
                else:
                    cur.execute("update login_credentials set password=%s where email=%s",
                                (self.fp_new.get(), email_og))
                    con.commit()
                    con.close()
                    messagebox.showinfo("success", "Password successfully changed.!!,please login with new password",
                                        parent=self.root_change_password)
                    self.reset()
            except Exception as es:
                messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.root_change_password)



    #====================forget password/change password window==================
    def forget_password_window(self):
        self.root_change_password = Toplevel()
        self.root_change_password.title("Forget Password")
        self.root_change_password.geometry("400x400+500+250")
        self.root_change_password.config(bg="white")
        self.root_change_password.iconbitmap("images/surveillance.ico")
        self.root_change_password.resizable(False, False)
        self.root_change_password.focus_force()
        self.root_change_password.grab_set()

        fp_label = Label(self.root_change_password, text="Change Password", font=("times new roman", 20, "bold"),
                         bg="white", fg="#7ec850").place(x=0, y=20, relwidth=1)

        fp_new_password = Label(self.root_change_password, text="New Password", font=("times new roman", 15, "bold"),
                                bg="white", fg="black").place(x=50, y=130)
        self.fp_new = Entry(self.root_change_password, font=("times new roman", 15), show="*", bg="#B8F9EC")
        self.fp_new.place(x=50, y=170, width=300)

        fp_confirm_password = Label(self.root_change_password, text="Confirm Password",
                                    font=("times new roman", 15, "bold"), bg="white", fg="black").place(x=50, y=210)
        self.fp_confirm = Entry(self.root_change_password, font=("times new roman", 15), bg="#B8F9EC")
        self.fp_confirm.place(x=50, y=250, width=300)

        fp_change_password = Button(self.root_change_password, command=self.change_password, cursor="hand2",
                                    text="Change", font=("times new roman", 16, "bold"), bg="#2A908F", bd=1, fg="white",
                                    activebackground="#173F5F").place(x=100, y=330, width=200, height=35)


    



    #=======================about us window===============================
    def about_us(self):
        self.root_about_us = Toplevel()
        self.root_about_us.title("about us")
        self.root_about_us.geometry("900x550+300+180")
        self.root_about_us.config(bg="#4a3933")
        self.root_about_us.iconbitmap("images/surveillance.ico")
        self.root_about_us.resizable(False, False)
        self.root_about_us.focus_force()
        self.root_about_us.grab_set()

        aboutus_heading = Label(self.root_about_us, text="ABOUT US", font=("times new roman", 35, "bold"), fg="#7ec850",
                                bg="#4a3933")
        aboutus_heading.pack()

        # ==========about us content image===========
        self.about_us_img = PhotoImage(file="images/about-us-content.png")

        # ============about us frame===========
        about_us_frame = Frame(self.root_about_us, bg="white")
        about_us_frame.place(x=15, y=80, width=870, height=450)

        # ===about-us label image====
        about_us_img_label = Label(about_us_frame, image=self.about_us_img, text="Email",
                                   font=("times new roman", 15, "bold"), bg="white", fg="black").place(x=40, y=25)



    
    


    #=======================Analyze attendance window====================
    def Analyze_attendance(self):
        self.Analyze_attendance = Toplevel()
        self.Analyze_attendance.title("Analyze attendance")
        self.Analyze_attendance.geometry("1000x600+225+130")
        self.Analyze_attendance.config(bg="White")
        self.Analyze_attendance.iconbitmap("images/surveillance.ico")
        self.Analyze_attendance.resizable(False, False)
        self.Analyze_attendance.focus_force()
        self.Analyze_attendance.grab_set()

        # ======variables=======
        self.from_date_var = StringVar()
        self.to_date_var = StringVar()
        self.course_combobox_analyze_var = StringVar()
        self.div_analyze_combobox_var = StringVar()
        self.export_analyze_var = StringVar()
        self.class_code_analyze_var = StringVar()

        # ==========heading=====
        Analyze_attendance_heading = Label(self.Analyze_attendance, text="Analyze Attendance",
                                           font=("times new roman", 30, "bold"), fg="#7ec850", bg="white")
        Analyze_attendance_heading.pack()

        # ======frame==========
        Analyze_attendance_frame = Frame(self.Analyze_attendance, bg="#7ec850")
        Analyze_attendance_frame.place(x=5, y=60, width=300, height=535)

        # =======left frame fields=====
        from_date = Label(Analyze_attendance_frame, text="From Date", font=("times new roman", 16, "bold"),
                          fg="red", bg="#7ec850")
        from_date.place(x=5, y=50)

        from_date_entry = DateEntry(Analyze_attendance_frame, font=("times new roman", 16, "bold"),
                                    date_pattern='y-mm-dd', bg="white", fg="black", textvariable=self.from_date_var,
                                    justify=CENTER)
        from_date_entry.place(x=120, y=50, width=150)

        to_date = Label(Analyze_attendance_frame, text="To Date", font=("times new roman", 16, "bold"),
                        fg="dark blue", bg="#7ec850")
        to_date.place(x=5, y=100)

        to_date_entry = DateEntry(Analyze_attendance_frame, font=("times new roman", 16, "bold"),
                                  date_pattern='y-mm-dd', bg="white", fg="black", textvariable=self.to_date_var,
                                  justify=CENTER)
        to_date_entry.place(x=120, y=100, width=150)

        course_analyze = Label(Analyze_attendance_frame, text="Course", font=("times new roman", 16, "bold"),
                               fg="white", bg="#7ec850")
        course_analyze.place(x=5, y=150)

        course_combobox_analyze = ttk.Combobox(Analyze_attendance_frame, textvariable=self.course_combobox_analyze_var,
                                               font=("times new roman", 15), state="readonly", justify=CENTER)
        course_combobox_analyze['values'] = ("Bsc-IT", "Msc-IT", "BMS", "BAF", "M-com")
        course_combobox_analyze.place(x=120, y=150, width=150)
        course_combobox_analyze.current()

        div_analyze_label = Label(Analyze_attendance_frame, text="Div", font=("times new roman", 16, "bold"),
                                  fg="white", bg="#7ec850")
        div_analyze_label.place(x=5, y=200)

        div_analyze_combobox = ttk.Combobox(Analyze_attendance_frame, textvariable=self.div_analyze_combobox_var,
                                            font=("times new roman", 15), state="readonly", justify=CENTER)
        div_analyze_combobox['values'] = ("A", "B", "C", "D", "E", "F")
        div_analyze_combobox.place(x=120, y=200, width=150)
        div_analyze_combobox.current()

        class_code_analyze_label = Label(Analyze_attendance_frame, text="Class_Code",
                                         font=("times new roman", 16, "bold"),
                                         fg="white", bg="#7ec850")
        class_code_analyze_label.place(x=5, y=250)

        class_code_analyze_entry = Entry(Analyze_attendance_frame, bd=0, textvariable=self.class_code_analyze_var,
                                         font=("times new roman", 16, "bold"), fg="black", bg="white", justify=CENTER)
        class_code_analyze_entry.place(x=120, y=250, width=150)

        #==================line seperater============
        line_label = Label(Analyze_attendance_frame,fg="white", bg="red")
        line_label.place(x=7, y=290, width=268, height=1.5)

        export_label = Label(Analyze_attendance_frame, text="Export", font=("times new roman", 16, "bold"),
                                fg="white", bg="#7ec850")
        export_label.place(x=5, y=300)

        export_combobox = ttk.Combobox(Analyze_attendance_frame, textvariable=self.export_analyze_var,
                                            font=("times new roman", 15), state="readonly", justify=CENTER)
        export_combobox['values'] = ("50", "75")
        export_combobox.place(x=120, y=300, width=150)
        export_combobox.current()

        # ==========left frame buttons=======
        seventy_five_button = Button(Analyze_attendance_frame, command=self.fn75, text="Below 75%", bd=2,
                                     cursor="hand2", font=("times new roman", 16, "bold"), fg="white", bg="#2A908F",
                                     activebackground="#173F5F")
        seventy_five_button.place(x=5, y=350, width=170)

        fifty_button = Button(Analyze_attendance_frame, command=self.fn50, text="Below 50%", bd=2,
                              cursor="hand2", font=("times new roman", 16, "bold"), fg="white", bg="#2A908F",
                              activebackground="#173F5F")
        fifty_button.place(x=5, y=400, width=170)

        clear_analyze_button = Button(Analyze_attendance_frame, command=self.clear_analyze, text="Clear", bd=2,
                              cursor="hand2", font=("times new roman", 16, "bold"), fg="white", bg="#2A908F",
                              activebackground="#173F5F")
        clear_analyze_button.place(x=185, y=375, width=100,height=50)

        download_analyze_button = Button(Analyze_attendance_frame, command=self.analyze_export_to_csv,
                                         text="Export-File", bd=2, cursor="hand2",
                                         font=("times new roman", 16, "bold"), fg="white", bg="#bd2000",
                                         activebackground="red")
        download_analyze_button.place(x=60, y=475, width=170)

        # ======view attendance frame2=====
        analyze_attendance_frame2 = Frame(self.Analyze_attendance, bg="white")
        analyze_attendance_frame2.place(x=310, y=60, width=685, height=535)

        scroll_x = Scrollbar(analyze_attendance_frame2, cursor="hand2", orient=HORIZONTAL)
        scroll_y = Scrollbar(analyze_attendance_frame2, cursor="hand2", orient=VERTICAL)
        self.analyze_attendance_table = ttk.Treeview(analyze_attendance_frame2, columns=(
            "id", "name", "email", "contact", "course", "divison", "class_code", "percentage"),
                                                     xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.analyze_attendance_table.xview)
        scroll_y.config(command=self.analyze_attendance_table.yview)
        self.analyze_attendance_table.heading("id", text="ID")
        self.analyze_attendance_table.heading("name", text="Name")
        self.analyze_attendance_table.heading("email", text="E-mail")
        self.analyze_attendance_table.heading("contact", text="Phone")
        self.analyze_attendance_table.heading("course", text="Course")
        self.analyze_attendance_table.heading("divison", text="DIV")
        self.analyze_attendance_table.heading("class_code", text="Class-code")
        self.analyze_attendance_table.heading("percentage", text="Percentage")
        self.analyze_attendance_table['show'] = 'headings'
        self.analyze_attendance_table.column("id", width=90)
        self.analyze_attendance_table.column("name", width=110)
        self.analyze_attendance_table.column("email", width=190)
        self.analyze_attendance_table.column("contact", width=160)
        self.analyze_attendance_table.column("course", width=120)
        self.analyze_attendance_table.column("divison", width=60)
        self.analyze_attendance_table.column("class_code", width=150)
        self.analyze_attendance_table.heading("percentage", text="Percentage")
        self.analyze_attendance_table.pack(fill=BOTH, expand=1)



    #========clear_analyze=======
    def clear_analyze(self):
        self.from_date_var.set("-Select-")
        self.to_date_var.set("-Select-")
        self.course_combobox_analyze_var.set("-Select-")
        self.div_analyze_combobox_var.set("-Select-")
        self.export_analyze_var.set("-Select-")
        self.class_code_analyze_var.set("")
        self.analyze_attendance_table.delete(*self.analyze_attendance_table.get_children())
        

    # date conversion and days calculator
    def convertDate(self, date):
        date = date.split('-')
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        return year, month, day

    def countDays(self, from_date, to_date):
        days = to_date - from_date
        return days.days

    # ============below 75% attendance==========
    def fn75(self):
        if self.from_date_var.get() == "" or self.to_date_var.get() == "" or self.course_combobox_analyze_var.get() == "" or self.div_analyze_combobox_var.get() == "" or self.class_code_analyze_var.get() == "":
            messagebox.showerror("Error", "All fields are required!!", parent=self.Analyze_attendance)
        else:
            try:

                f_date = self.from_date_var.get()
                t_date = self.to_date_var.get()

                f_year, f_month, f_day = self.convertDate(f_date)
                t_year, t_month, t_day = self.convertDate(t_date)

                days = self.countDays(datetime.date(f_year, f_month, f_day), datetime.date(t_year, t_month, t_day))

                con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
                cur = con.cursor()
                cur.execute("select monthly_record.id,monthly_record.name,\
                            monthly_record.email,monthly_record.contact,\
                            monthly_record.course,monthly_record.divison,\
                            monthly_record.class_code,monthly_record.percentage from \
                            (select *,round(count(status)*100/" + str(days) + ") as percentage from attendance\
                                where status = 'present' and date between '" + self.from_date_var.get() + "' and '" + self.to_date_var.get() + "' group by id) as monthly_record\
                                    where monthly_record.percentage<'75' and course = '" + self.course_combobox_analyze_var.get() + "' and divison = '" + self.div_analyze_combobox_var.get() + "' and class_code = '" + self.class_code_analyze_var.get() + "';")

                # cur.execute(query)
                rows = cur.fetchone()
                if rows == None:
                    messagebox.showerror("Error", "No student attendance below 75%", parent=self.Analyze_attendance)
                else:
                    query = "select monthly_record.id,monthly_record.name,\
                            monthly_record.email,monthly_record.contact,\
                            monthly_record.course,monthly_record.divison,\
                            monthly_record.class_code,monthly_record.percentage from \
                            (select *,round(count(status)*100/" + str(days) + ") as percentage from attendance\
                                where status = 'present' and date between '" + self.from_date_var.get() + "' and '" + self.to_date_var.get() + "' group by id) as monthly_record\
                                    where monthly_record.percentage<'75' and course = '" + self.course_combobox_analyze_var.get() + "' and divison = '" + self.div_analyze_combobox_var.get() + "' and class_code = '" + self.class_code_analyze_var.get() + "';"
                    cur.execute(query)

                    rows = cur.fetchall()
                    #print(rows)
                    if len(rows) != 0:
                        self.analyze_attendance_table.delete(*self.analyze_attendance_table.get_children())
                        for row in rows:
                            self.analyze_attendance_table.insert('', END, values=row)
                            
                    con.commit()
                    
                    messagebox.showinfo("", "Match found!\n\nStudents Count: " + str(len(rows)),
                                        parent=self.Analyze_attendance)
                    sql = pd.read_sql_query(query, con)
                    df = pd.DataFrame(sql)

                    name = df['name']
                    percentage = df['percentage']
                    figure = plt.figure()
                    axes = figure.add_subplot(1, 1, 1)
                    axes.set_ylim(0, 100)
                    axes.bar(name, percentage)
                    plt.title("Defaulter Graph below 75%")
                    plt.ylabel("Percentage")
                    plt.xlabel("Student Name")
                    plt.show()
                    con.close()

            except Exception as es:
                messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.Analyze_attendance)





    # ===========below 50% attendance==========
    def fn50(self):
        if self.from_date_var.get() == "" or self.to_date_var.get() == "" or self.course_combobox_analyze_var.get() == "" or self.div_analyze_combobox_var.get() == "" or self.class_code_analyze_var.get() == "":
            messagebox.showerror("Error", "All fields are required!!", parent=self.Analyze_attendance)
        else:
            try:

                f_date = self.from_date_var.get()
                t_date = self.to_date_var.get()

                f_year, f_month, f_day = self.convertDate(f_date)
                t_year, t_month, t_day = self.convertDate(t_date)

                days = self.countDays(datetime.date(f_year, f_month, f_day), datetime.date(t_year, t_month, t_day))

                con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
                cur = con.cursor()
                cur.execute("select monthly_record.id,monthly_record.name,\
                            monthly_record.email,monthly_record.contact,\
                            monthly_record.course,monthly_record.divison,\
                            monthly_record.class_code,monthly_record.percentage from \
                            (select *,round(count(status)*100/" + str(days) + ") as percentage from attendance\
                                where status = 'present' and date between '" + self.from_date_var.get() + "' and '" + self.to_date_var.get() + "' group by id) as monthly_record\
                                    where monthly_record.percentage<'50' and course = '" + self.course_combobox_analyze_var.get() + "' and divison = '" + self.div_analyze_combobox_var.get() + "' and class_code = '" + self.class_code_analyze_var.get() + "';")

                # cur.execute(query)
                rows = cur.fetchone()
                if rows == None:
                    messagebox.showerror("Error", "No student attendance below 50%", parent=self.Analyze_attendance)
                else:
                    query = "select monthly_record.id,monthly_record.name,\
                            monthly_record.email,monthly_record.contact,\
                            monthly_record.course,monthly_record.divison,\
                            monthly_record.class_code,monthly_record.percentage from \
                            (select *,round(count(status)*100/" + str(days) + ") as percentage from attendance\
                                where status = 'present' and date between '" + self.from_date_var.get() + "' and '" + self.to_date_var.get() + "' group by id) as monthly_record\
                                    where monthly_record.percentage<'50' and course = '" + self.course_combobox_analyze_var.get() + "' and divison = '" + self.div_analyze_combobox_var.get() + "' and class_code = '" + self.class_code_analyze_var.get() + "';"
                    cur.execute(query)

                    rows = cur.fetchall()
                    if len(rows) != 0:
                        self.analyze_attendance_table.delete(*self.analyze_attendance_table.get_children())
                        for row in rows:
                            self.analyze_attendance_table.insert('', END, values=row)
                    con.commit()
                    #con.close()
                    messagebox.showinfo("", "Match found!\n\nStudents Count: " + str(len(rows)),
                                        parent=self.Analyze_attendance)
                    sql = pd.read_sql_query(query, con)
                    df = pd.DataFrame(sql)

                    name = df['name']
                    percentage = df['percentage']
                    figure = plt.figure()
                    axes = figure.add_subplot(1, 1, 1)
                    axes.set_ylim(0, 100)
                    axes.bar(name, percentage)
                    plt.title("Defaulter Graph below 50%")
                    plt.ylabel("Percentage")
                    plt.xlabel("Student Name")
                    plt.show()
                    con.close()

            except Exception as es:
                messagebox.showerror("Error", f"Error Due to: {str(es)}", parent=self.Analyze_attendance)

    # ==========analyze attendance export function===========
    def analyze_export_to_csv(self):
        if self.from_date_var.get() == "" or self.to_date_var.get() == "" or self.course_combobox_analyze_var.get() == "" or self.div_analyze_combobox_var.get() == "" or self.class_code_analyze_var.get() == "":
            messagebox.showerror("Error", "All fields are required!!", parent=self.Analyze_attendance)
        else:
            f_date = self.from_date_var.get()
            t_date = self.to_date_var.get()

            f_year, f_month, f_day = self.convertDate(f_date)
            t_year, t_month, t_day = self.convertDate(t_date)

            days = self.countDays(datetime.date(f_year, f_month, f_day), datetime.date(t_year, t_month, t_day))
            con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
            select_query = "select monthly_record.id,monthly_record.name,\
                            monthly_record.email,monthly_record.contact,\
                            monthly_record.course,monthly_record.divison,\
                            monthly_record.class_code,monthly_record.percentage from \
                            (select *,round(count(status)*100/" + str(days) + ") as percentage from attendance\
                                where status = 'present' and date between '" + self.from_date_var.get() + "' and '" + self.to_date_var.get() + "' group by id) as monthly_record\
                                    where monthly_record.percentage<'"+self.export_analyze_var.get()+"' and course = '" + self.course_combobox_analyze_var.get() + "' and divison = '" + self.div_analyze_combobox_var.get() + "' and class_code = '" + self.class_code_analyze_var.get() + "';"
            sql_query = pd.read_sql_query(select_query, con)
            df = pd.DataFrame(sql_query)
            #print(df)
            if df.empty:
                messagebox.showerror("Error", "No Data Found!", parent=self.Analyze_attendance)
            else:
                date = str(datetime.datetime.now()).split()
                currdir = os.getcwd()
                tempdir2 = fd.askdirectory(parent=self.Analyze_attendance, initialdir=currdir,
                                           title='Please select a directory to save output file')
                file_name = date[0] + "_Defaulter_list.csv"
                output = tempdir2 + "/" + file_name
                df.to_csv(output)
                messagebox.showinfo("Exported", "Data exported to CSV Successfully!\nFile Location: " + output,
                                    parent=self.Analyze_attendance)
            con.close()

    def logout(self):
        home_window.destroy()
        login()









#====================================================================================================================================
#==========================================================class admin===============================================================
class admin_page:
    def __init__(self):
        global admin_window,email_admin
        admin_window = tk.Tk()
        admin_window.title("     Smart Attendance System (Admin)")
        admin_window.geometry("1350x700+50+50")
        admin_window.resizable(False, False)
        admin_window.iconbitmap("images/surveillance.ico")

        self.img_capture = ImageTk.PhotoImage(Image.open("images/faculty_img.png"))
        self.img_view_attendance = ImageTk.PhotoImage(Image.open("images/student_management_img.png"))
        self.img_logout = ImageTk.PhotoImage(Image.open("images/logout1.png"))

        # =====Welcome label====
        welcome = Label(admin_window, text="Welcome  {}".format(email_admin), font=("times new roman", 16, "bold"),
                        fg="black")
        welcome.place(x=1000, y=5)

        # =====home frame=======
        admin_page_frame = Frame(admin_window, bg="#7ec850")
        admin_page_frame.place(x=80, y=60, width=1180, height=600)

        admin_title_bar = Label(admin_page_frame, bg="white").place(x=0, y=0, relwidth=1, height=60)
        admin_title_heading = Label(admin_page_frame, text="Smart Attendance System",
                                    font=("times new roman", 25, "bold"), fg="#7ec850", bg="white").place(x=440, y=12)

        # ========1st row buttons=======
        faculty_img_button = Button(admin_page_frame, image=self.img_capture, command=self.faculty_management,
                                    cursor="hand2", bd=False).place(x=55, y=100, width=170, height=170)
        faculty_label = Label(admin_page_frame, text="Faculty Management", font=("times new roman", 16), fg="white",
                              bg="#7ec850").place(x=50, y=270)

        student_img_button = Button(admin_page_frame, image=self.img_view_attendance, command=self.student_management,
                                    cursor="hand2", bd=False).place(x=355, y=100, width=170, height=170)
        student_label = Label(admin_page_frame, text="Student Management", font=("times new roman", 16), fg="white",
                              bg="#7ec850").place(x=350, y=270)

        logout_button = Button(admin_page_frame, image=self.img_logout, command=self.logout, cursor="hand2", bd=False).place(
            x=55, y=350, width=170, height=170)
        logout_label = Label(admin_page_frame, text="Logout", font=("times new roman", 16), fg="white", bg="#7ec850").place(
            x=55, y=520)

        admin_window.mainloop()


    # =======faculty management=====
    def faculty_management(self):
        self.root_faculty_management = Toplevel()
        self.root_faculty_management.title("Faculty Management")
        self.root_faculty_management.geometry("1000x600+225+130")
        self.root_faculty_management.config(bg="white")
        self.root_faculty_management.iconbitmap("images/surveillance.ico")
        self.root_faculty_management.resizable(False, False)
        self.root_faculty_management.focus_force()
        self.root_faculty_management.grab_set()

        faculty_management_heading = Label(self.root_faculty_management, text="Faculty Management",
                                           font=("times new roman", 35, "bold"), fg="#7ec850", bg="white")
        faculty_management_heading.pack()

        # =============All variables=========
        self.faculty_id_var = StringVar()
        self.faculty_username_var = StringVar()
        self.faculty_name_var = StringVar()
        self.faculty_email_var = StringVar()
        self.faculty_password_var = StringVar()
        self.faculty_search_by_combobox_var = StringVar()
        self.faculty_search_by_entry_var = StringVar()

        # =====student management left frame======
        faculty_management_left_frame = Frame(self.root_faculty_management, bg="#7ec850")
        faculty_management_left_frame.place(x=5, y=60, width=300, height=535)

        faculty_id_label = Label(faculty_management_left_frame, text="ID", font=("times new roman", 14, "bold"),
                                 fg="white", bg="#7ec850")
        faculty_id_label.place(x=5, y=15)

        faculty_id_entry = Entry(faculty_management_left_frame, textvariable=self.faculty_id_var, bd=0,
                                 font=("times new roman", 16, "bold"), fg="black", bg="white")
        faculty_id_entry.place(x=120, y=15, width=150)

        faculty_username_label = Label(faculty_management_left_frame, text="User-Name",
                                       font=("times new roman", 14, "bold"), fg="white", bg="#7ec850")
        faculty_username_label.place(x=5, y=55)

        faculty_username_entry = Entry(faculty_management_left_frame, textvariable=self.faculty_username_var, bd=0,
                                       font=("times new roman", 16, "bold"), fg="black", bg="white")
        faculty_username_entry.place(x=120, y=55, width=150)

        faculty_name_label = Label(faculty_management_left_frame, text="Name", font=("times new roman", 14, "bold"),
                                   fg="white", bg="#7ec850")
        faculty_name_label.place(x=5, y=95)

        faculty_name_entry = Entry(faculty_management_left_frame, textvariable=self.faculty_name_var, bd=0,
                                   font=("times new roman", 16, "bold"), fg="black", bg="white")
        faculty_name_entry.place(x=120, y=95, width=150)

        faculty_email_label = Label(faculty_management_left_frame, text="Email", font=("times new roman", 14, "bold"),
                                    fg="white", bg="#7ec850")
        faculty_email_label.place(x=5, y=135)

        faculty_email_entry = Entry(faculty_management_left_frame, textvariable=self.faculty_email_var, bd=0,
                                    font=("times new roman", 12, "bold"), fg="black", bg="white")
        faculty_email_entry.place(x=120, y=135, width=150)

        faculty_password_label = Label(faculty_management_left_frame, text="Password",
                                       font=("times new roman", 14, "bold"), fg="white", bg="#7ec850")
        faculty_password_label.place(x=5, y=175)

        faculty_password_entry = Entry(faculty_management_left_frame, textvariable=self.faculty_password_var, bd=0,
                                       font=("times new roman", 16, "bold"), fg="black", bg="white")
        faculty_password_entry.place(x=120, y=175, width=150)

        # ========faculty left frame button======
        addbtn_faculty_management = Button(faculty_management_left_frame, command=self.add_faculty, text="Add", bd=4,
                                           cursor="hand2", font=("times new roman", 12), fg="black", bg="#5097a4",
                                           activebackground="gray")
        addbtn_faculty_management.place(x=15, y=400, width=60)
        updatebtn_faculty_management = Button(faculty_management_left_frame, command=self.faculty_update_student_data,
                                              text="Update", bd=4, cursor="hand2", font=("times new roman", 12),
                                              fg="black", bg="#5097a4", activebackground="gray")
        updatebtn_faculty_management.place(x=80, y=400, width=60)
        deletebtn_faculty_management = Button(faculty_management_left_frame, command=self.delete_faculty_data,
                                              text="Delete", bd=4, cursor="hand2", font=("times new roman", 12),
                                              fg="black", bg="red", activebackground="gray")
        deletebtn_faculty_management.place(x=145, y=400, width=60)
        clearbtn_faculty_management = Button(faculty_management_left_frame, command=self.clear_faculty_data,
                                             text="Clear", bd=4, cursor="hand2", font=("times new roman", 12),
                                             fg="black", bg="#5097a4", activebackground="gray")
        clearbtn_faculty_management.place(x=210, y=400, width=60)

        # ======faculty management right search frame=====
        faculty_management_right_frame = Frame(self.root_faculty_management, bg="#012000")
        faculty_management_right_frame.place(x=310, y=60, width=685, height=535)

        # ===========search bar==============
        faculty_search_by_label = Label(faculty_management_right_frame, text="Search By",
                                        font=("times new roman", 14, "bold"), fg="white", bg="#012000")
        faculty_search_by_label.place(x=5, y=15)

        faculty_search_by_combobox = ttk.Combobox(faculty_management_right_frame,
                                                  textvariable=self.faculty_search_by_combobox_var,
                                                  font=("times new roman", 14), state="readonly", justify=CENTER)
        faculty_search_by_combobox['values'] = ("", "id", "name")
        faculty_search_by_combobox.place(x=120, y=15, width=150)
        faculty_search_by_combobox.current(0)

        faculty_search_by_entry = Entry(faculty_management_right_frame, textvariable=self.faculty_search_by_entry_var,
                                        bd=0, font=("calibri", 16), fg="black", bg="white")
        faculty_search_by_entry.place(x=280, y=15, width=150)

        faculty_searchbtn_student_management = Button(faculty_management_right_frame,
                                                      command=self.faculty_data_search_by, text="Search", bd=4,
                                                      cursor="hand2", font=("times new roman", 12), fg="black",
                                                      bg="#5097a4", activebackground="gray")
        faculty_searchbtn_student_management.place(x=450, y=10, width=100)

        faculty_showallbtn_student_management = Button(faculty_management_right_frame, command=self.fetch_faculty_data,
                                                       text="Show All", bd=4, cursor="hand2",
                                                       font=("times new roman", 12), fg="black", bg="#5097a4",
                                                       activebackground="gray")
        faculty_showallbtn_student_management.place(x=570, y=10, width=100)

        # ======student management view frame=====
        faculty_management_view_frame = Frame(faculty_management_right_frame, bg="white")
        faculty_management_view_frame.place(x=5, y=55, width=675, height=475)

        # =========student data view=======
        scroll_x = Scrollbar(faculty_management_view_frame, cursor="hand2", orient=HORIZONTAL)
        scroll_y = Scrollbar(faculty_management_view_frame, cursor="hand2", orient=VERTICAL)
        self.faculty_data_view = ttk.Treeview(faculty_management_view_frame,
                                              columns=("id", "username", "name", "email", "password"),
                                              xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.faculty_data_view.xview)
        scroll_y.config(command=self.faculty_data_view.yview)
        self.faculty_data_view.heading("id", text="ID")
        self.faculty_data_view.heading("username", text="Username")
        self.faculty_data_view.heading("name", text="Name")
        self.faculty_data_view.heading("email", text="E-mail")
        self.faculty_data_view.heading("password", text="password")
        self.faculty_data_view['show'] = 'headings'
        self.faculty_data_view.column("id", width=90)
        self.faculty_data_view.column("username", width=150)
        self.faculty_data_view.column("name", width=110)
        self.faculty_data_view.column("email", width=190)
        self.faculty_data_view.column("password", width=160)
        self.faculty_data_view.pack(fill=BOTH, expand=1)
        self.faculty_data_view.bind("<ButtonRelease-1>", self.faculty_get_cursor)
        self.fetch_faculty_data2()

    # ======add faculty function=========
    def add_faculty(self):
        if self.faculty_id_var.get()=="" or self.faculty_username_var.get()=="" or self.faculty_name_var.get()=="" or self.faculty_email_var.get()=="" or self.faculty_password_var.get()=="":
            messagebox.showerror("Error","All fields are required!!!",parent=self.root_faculty_management)
        else:
            con=pymysql.connect(host="remotemysql.com",user="bY58KYWUaB",password="s2uMZ7iyKn",database="bY58KYWUaB")
            cur=con.cursor()
            cur.execute("insert into login_credentials values(%s,%s,%s,%s,%s)",(self.faculty_id_var.get(),self.faculty_username_var.get(),self.faculty_name_var.get(),self.faculty_email_var.get(),self.faculty_password_var.get()))

            con.commit()
            self.fetch_faculty_data2()
            #self.clear_student_data()
            con.close()    
            messagebox.showinfo("Success","Faculty data has been inserted",parent=self.root_faculty_management)
    
            
            
    # =========faculty fetch data funcion======
    def fetch_faculty_data2(self):
        con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
        cur = con.cursor()
        cur.execute("select * from login_credentials")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.faculty_data_view.delete(*self.faculty_data_view.get_children())
            for row in rows:
                self.faculty_data_view.insert('', END, values=row)
            con.commit()
        con.close()        

    # =========faculty fetch data funcion======
    def fetch_faculty_data(self):
        con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
        cur = con.cursor()
        cur.execute("select * from login_credentials")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.faculty_data_view.delete(*self.faculty_data_view.get_children())
            for row in rows:
                self.faculty_data_view.insert('', END, values=row)
            con.commit()
        con.close()
        messagebox.showinfo("Success", "Match found!\n\nTotal Faculty Count: " + str(len(rows)),
                            parent=self.root_faculty_management)

    # =========faculty clear data function=========
    def clear_faculty_data(self):
        self.faculty_id_var.set("")
        self.faculty_username_var.set("")
        self.faculty_name_var.set("")
        self.faculty_email_var.set("")
        self.faculty_password_var.set("")

    # ============clear search by========
    def faculty_search_by_clear(self):
        self.faculty_search_by_combobox_var.set("--SELECT--")
        self.faculty_search_by_entry_var.set("")

    # ========faculty cursor function===========
    def faculty_get_cursor(self,ev):
        cursor_row=self.faculty_data_view.focus()
        contents=self.faculty_data_view.item(cursor_row)
        row=contents['values']
        #print(row)
        self.faculty_id_var.set(row[0])
        self.faculty_username_var.set(row[1])
        self.faculty_name_var.set(row[2])
        self.faculty_email_var.set(row[3])
        self.faculty_password_var.set(row[4])

    # =======faculty delete function==========
    def delete_faculty_data(self):
        con=pymysql.connect(host="remotemysql.com",user="bY58KYWUaB",password="s2uMZ7iyKn",database="bY58KYWUaB")
        cur=con.cursor()
        cur.execute("delete from login_credentials where id=%s",self.faculty_id_var.get())
        con.commit()
        con.close()
        self.fetch_faculty_data2()
        self.clear_faculty_data()
        messagebox.showinfo("Success","Successfully deleted!!",parent=self.root_faculty_management)
       
        
        

    # =========update function============
    def faculty_update_student_data(self):
        con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
        cur = con.cursor()
        cur.execute("update login_credentials set username=%s,name=%s,email=%s,password=%s where id=%s", (
        self.faculty_username_var.get(), self.faculty_name_var.get(), self.faculty_email_var.get(),
        self.faculty_password_var.get(), self.faculty_id_var.get()))
        # ,name=%s,email=%s,contact=%s,course=%s,div=%s,class_code=%s,dataset=%s     self.name_var.get(),self.email_var.get(),self.contact_var.get(),self.course_var.get(),self.div_var.get(),self.class_code_var.get(),self.dataset_var.get(),
        con.commit()
        self.fetch_faculty_data2()
        self.clear_faculty_data()
        con.close()
        messagebox.showinfo("Success","Successfully updated!!",parent=self.root_faculty_management)
        

    # =========search by function========
    def faculty_data_search_by(self):
        if self.faculty_search_by_combobox_var.get()=="" or self.faculty_search_by_entry_var.get()=="":
            messagebox.showerror("Error","All fields are required",parent=self.root_faculty_management)
        else:
            con=pymysql.connect(host="remotemysql.com",user="bY58KYWUaB",password="s2uMZ7iyKn",database="bY58KYWUaB")
            cur=con.cursor()
            cur.execute("select * from login_credentials where " +str(self.faculty_search_by_combobox_var.get())+" LIKE '%"+str(self.faculty_search_by_entry_var.get())+"%'")
            rows=cur.fetchall()
            if len(rows)!=0:
                self.faculty_data_view.delete(*self.faculty_data_view.get_children())
                for row in rows:
                    self.faculty_data_view.insert('',END,values=row)
                messagebox.showinfo("Success","Match found!!",parent=self.root_faculty_management)
                self.faculty_search_by_clear() 
            else:
                messagebox.showerror("Error","no match found",parent=self.root_faculty_management)
                con.commit()
                self.faculty_search_by_clear()
            con.close()

    # =======student management=====
    def student_management(self):
        self.root_student_management = Toplevel()
        self.root_student_management.title("Student Management")
        self.root_student_management.geometry("1000x600+225+130")
        self.root_student_management.config(bg="white")
        self.root_student_management.iconbitmap("images/surveillance.ico")
        self.root_student_management.resizable(False, False)
        self.root_student_management.focus_force()
        self.root_student_management.grab_set()

        student_management_heading = Label(self.root_student_management, text="Student Management",
                                           font=("times new roman", 35, "bold"), fg="#7ec850", bg="white")
        student_management_heading.pack()

        # ======all variables===========
        self.id_var = StringVar()
        self.username_var = StringVar()
        self.name_var = StringVar()
        self.email_var = StringVar()
        self.contact_var = StringVar()
        self.course_var = StringVar()
        self.div_var = StringVar()
        self.class_code_var = StringVar()
        self.dataset_var = StringVar()

        self.search_by_combobox_var = StringVar()
        self.search_by_entry_var = StringVar()

        # =====student management left frame======
        student_management_left_frame = Frame(self.root_student_management, bg="#7ec850")
        student_management_left_frame.place(x=5, y=60, width=300, height=535)

        student_id_label = Label(student_management_left_frame, text="ID", font=("times new roman", 14, "bold"),
                                 fg="white", bg="#7ec850")
        student_id_label.place(x=5, y=15)

        student_id_entry = Entry(student_management_left_frame, textvariable=self.id_var, bd=0,
                                 font=("times new roman", 16, "bold"), fg="black", bg="white")
        student_id_entry.place(x=120, y=15, width=150)

        student_username_label = Label(student_management_left_frame, text="User-Name",
                                       font=("times new roman", 14, "bold"), fg="white", bg="#7ec850")
        student_username_label.place(x=5, y=55)

        student_username_entry = Entry(student_management_left_frame, textvariable=self.username_var, bd=0,
                                       font=("times new roman", 16, "bold"), fg="black", bg="white")
        student_username_entry.place(x=120, y=55, width=150)

        student_name_label = Label(student_management_left_frame, text="Name", font=("times new roman", 14, "bold"),
                                   fg="white", bg="#7ec850")
        student_name_label.place(x=5, y=95)

        student_name_entry = Entry(student_management_left_frame, textvariable=self.name_var, bd=0,
                                   font=("times new roman", 16, "bold"), fg="black", bg="white")
        student_name_entry.place(x=120, y=95, width=150)

        student_email_label = Label(student_management_left_frame, text="Email", font=("times new roman", 14, "bold"),
                                    fg="white", bg="#7ec850")
        student_email_label.place(x=5, y=135)

        student_email_entry = Entry(student_management_left_frame, textvariable=self.email_var, bd=0,
                                    font=("times new roman", 12, "bold"), fg="black", bg="white")
        student_email_entry.place(x=120, y=135, width=150)

        student_contact_label = Label(student_management_left_frame, text="Contact",
                                      font=("times new roman", 14, "bold"), fg="white", bg="#7ec850")
        student_contact_label.place(x=5, y=175)

        student_contact_entry = Entry(student_management_left_frame, textvariable=self.contact_var, bd=0,
                                      font=("times new roman", 16, "bold"), fg="black", bg="white")
        student_contact_entry.place(x=120, y=175, width=150)

        student_course_label = Label(student_management_left_frame, text="Course", font=("times new roman", 14, "bold"),
                                     fg="white", bg="#7ec850")
        student_course_label.place(x=5, y=215)

        student_course_combobox = ttk.Combobox(student_management_left_frame, textvariable=self.course_var,
                                               font=("times new roman", 14), state="readonly", justify=CENTER)
        student_course_combobox['values'] = ("", "Bsc-IT", "Msc-IT", "BMS", "BAF", "M-com")
        student_course_combobox.place(x=120, y=215, width=150)
        student_course_combobox.current(0)

        student_div_label = Label(student_management_left_frame, text="DIV", font=("times new roman", 14, "bold"),
                                  fg="white", bg="#7ec850")
        student_div_label.place(x=5, y=255)

        student_div_combobox = ttk.Combobox(student_management_left_frame, textvariable=self.div_var,
                                            font=("times new roman", 14), state="readonly", justify=CENTER)
        student_div_combobox['values'] = ("", "A", "B", "C", "D", "E", "F")
        student_div_combobox.place(x=120, y=255, width=150)
        student_div_combobox.current(0)

        student_class_code_label = Label(student_management_left_frame, text="Class-Code",
                                         font=("times new roman", 14, "bold"), fg="white", bg="#7ec850")
        student_class_code_label.place(x=5, y=295)

        student_class_code_entry = Entry(student_management_left_frame, textvariable=self.class_code_var, bd=0,
                                         font=("times new roman", 16, "bold"), fg="black", bg="white", justify=CENTER)
        student_class_code_entry.place(x=120, y=295, width=150)

        student_dataset_label = Label(student_management_left_frame, text="Dataset",
                                      font=("times new roman", 14, "bold"), fg="white", bg="#7ec850")
        student_dataset_label.place(x=5, y=335)

        student_dataset_combobox = ttk.Combobox(student_management_left_frame, textvariable=self.dataset_var,
                                                font=("times new roman", 14), state="readonly", justify=CENTER)
        student_dataset_combobox['values'] = ("", "1", "0")
        student_dataset_combobox.place(x=120, y=335, width=150)
        student_dataset_combobox.current(0)

        # ========left frame button======
        addbtn_student_management = Button(student_management_left_frame, command=self.add_students, text="Add", bd=4,
                                           cursor="hand2", font=("times new roman", 12), fg="black", bg="#5097a4",
                                           activebackground="gray")
        addbtn_student_management.place(x=15, y=400, width=60)
        updatebtn_student_management = Button(student_management_left_frame, command=self.update_student_data,
                                              text="Update", bd=4, cursor="hand2", font=("times new roman", 12),
                                              fg="black", bg="#5097a4", activebackground="gray")
        updatebtn_student_management.place(x=80, y=400, width=60)
        deletebtn_student_management = Button(student_management_left_frame, command=self.delete_student_data,
                                              text="Delete", bd=4, cursor="hand2", font=("times new roman", 12),
                                              fg="black", bg="red", activebackground="gray")
        deletebtn_student_management.place(x=145, y=400, width=60)
        clearbtn_student_management = Button(student_management_left_frame, command=self.clear_student_data,
                                             text="Clear", bd=4, cursor="hand2", font=("times new roman", 12),
                                             fg="black", bg="#5097a4", activebackground="gray")
        clearbtn_student_management.place(x=210, y=400, width=60)

        # =========create dataset btn========
        create_dataset_button = Button(student_management_left_frame, command=self.create_dataset_button_function,
                                       text="Create Dataset", bd=4, cursor="hand2",
                                       font=("times new roman", 12, "bold"), fg="black", bg="#ffa500",
                                       activebackground="gray")
        create_dataset_button.place(x=15, y=470, width=255)

        # ======student management right search frame=====
        student_management_right_frame = Frame(self.root_student_management, bg="#012000")
        student_management_right_frame.place(x=310, y=60, width=685, height=535)

        # ===========search bar==============
        search_by_label = Label(student_management_right_frame, text="Search By", font=("times new roman", 14, "bold"),
                                fg="white", bg="#012000")
        search_by_label.place(x=5, y=15)

        search_by_combobox = ttk.Combobox(student_management_right_frame, textvariable=self.search_by_combobox_var,
                                          font=("times new roman", 14), state="readonly", justify=CENTER)
        search_by_combobox['values'] = ("", "id", "name", "class_code")
        search_by_combobox.place(x=120, y=15, width=150)
        search_by_combobox.current(0)

        search_by_entry = Entry(student_management_right_frame, textvariable=self.search_by_entry_var, bd=0,
                                font=("calibri", 16), fg="black", bg="white")
        search_by_entry.place(x=280, y=15, width=150)

        searchbtn_student_management = Button(student_management_right_frame, text="Search",
                                              command=self.search_student_data_search_by, bd=4, cursor="hand2",
                                              font=("times new roman", 12), fg="black", bg="#5097a4",
                                              activebackground="gray")
        searchbtn_student_management.place(x=450, y=10, width=100)

        showallbtn_student_management = Button(student_management_right_frame, command=self.fetch_student_data,
                                               text="Show All", bd=4, cursor="hand2", font=("times new roman", 12),
                                               fg="black", bg="#5097a4", activebackground="gray")
        showallbtn_student_management.place(x=570, y=10, width=100)

        # ======student management view frame=====
        student_management_view_frame = Frame(student_management_right_frame, bg="white")
        student_management_view_frame.place(x=5, y=55, width=675, height=475)

        # =========student data view=======
        scroll_x = Scrollbar(student_management_view_frame, cursor="hand2", orient=HORIZONTAL)
        scroll_y = Scrollbar(student_management_view_frame, cursor="hand2", orient=VERTICAL)
        self.student_data_view = ttk.Treeview(student_management_view_frame, columns=(
        "id", "username", "name", "email", "contact", "course", "division", "class_code", "dataset"),
                                              xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_data_view.xview)
        scroll_y.config(command=self.student_data_view.yview)
        self.student_data_view.heading("id", text="ID")
        self.student_data_view.heading("username", text="Username")
        self.student_data_view.heading("name", text="Name")
        self.student_data_view.heading("email", text="E-mail")
        self.student_data_view.heading("contact", text="Phone")
        self.student_data_view.heading("course", text="Course")
        self.student_data_view.heading("division", text="Division")
        self.student_data_view.heading("class_code", text="Class-code")
        self.student_data_view.heading("dataset", text="Dataset")
        self.student_data_view['show'] = 'headings'
        self.student_data_view.column("id", width=90)
        self.student_data_view.column("username", width=150)
        self.student_data_view.column("name", width=110)
        self.student_data_view.column("email", width=190)
        self.student_data_view.column("contact", width=160)
        self.student_data_view.column("course", width=120)
        self.student_data_view.column("division", width=60)
        self.student_data_view.column("class_code", width=90)
        self.student_data_view.column("dataset", width=90)
        self.student_data_view.pack(fill=BOTH, expand=1)
        self.student_data_view.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_student_data2()

    # ======add student function=========
    def add_students(self):
        if self.id_var.get()=="" or self.username_var.get()=="" or self.name_var.get()=="" or self.email_var.get()=="" or self.contact_var.get()=="" or self.course_var.get()=="" or self.div_var.get()=="" or self.class_code_var.get()=="" or self.dataset_var.get()=="":
            messagebox.showerror("Error","All fields are required!!!",parent=self.root_student_management)
        else:
            con=pymysql.connect(host="remotemysql.com",user="bY58KYWUaB",password="s2uMZ7iyKn",database="bY58KYWUaB")
            cur=con.cursor()
            cur.execute("insert into students values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.id_var.get(),self.username_var.get(),self.name_var.get(),self.email_var.get(),self.contact_var.get(),self.course_var.get(),self.div_var.get(),self.class_code_var.get(),self.dataset_var.get()))

            con.commit()
            self.fetch_student_data2()
            self.clear_student_data()
            con.close()    
            messagebox.showinfo("Success","Student data has been inserted",parent=self.root_student_management)



    # =========fetch data funcion======
    def fetch_student_data2(self):
        con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
        cur = con.cursor()
        cur.execute("select * from students")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.student_data_view.delete(*self.student_data_view.get_children())
            for row in rows:
                self.student_data_view.insert('', END, values=row)
            con.commit()
        con.close()


    # =========fetch data funcion======
    def fetch_student_data(self):
        con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
        cur = con.cursor()
        cur.execute("select * from students")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.student_data_view.delete(*self.student_data_view.get_children())
            for row in rows:
                self.student_data_view.insert('', END, values=row)
            con.commit()
        con.close()
        messagebox.showinfo("Success", "Match found!\n\nTotal Students Count: " + str(len(rows)),
                            parent=self.root_student_management)

    # =========clear data function=========
    def clear_student_data(self):
        self.id_var.set("")
        self.username_var.set("")
        self.name_var.set("")
        self.email_var.set("")
        self.contact_var.set("")
        self.course_var.set("--SELECT--")
        self.div_var.set("--SELECT--")
        self.class_code_var.set("")
        self.dataset_var.set("--SELECT--")
        self.search_by_clear()

    # ============clear search by========
    def search_by_clear(self):
        self.search_by_combobox_var.set("--SELECT--")
        self.search_by_entry_var.set("")

    # ========cursor function===========
    def get_cursor(self, ev):
        cursor_row = self.student_data_view.focus()
        contents = self.student_data_view.item(cursor_row)
        row = contents['values']
        # print(row)
        self.id_var.set(row[0])
        self.username_var.set(row[1])
        self.name_var.set(row[2])
        self.email_var.set(row[3])
        self.contact_var.set(row[4])
        self.course_var.set(row[5])
        self.div_var.set(row[6])
        self.class_code_var.set(row[7])
        self.dataset_var.set(row[8])

    # =========update function============
    def update_student_data(self):
        con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
        cur = con.cursor()
        cur.execute(
            "update students set username=%s,name=%s,email=%s,contact=%s,course=%s,division=%s,class_code=%s,dataset=%s where id=%s",
            (self.username_var.get(), self.name_var.get(), self.email_var.get(), self.contact_var.get(),
             self.course_var.get(), self.div_var.get(), self.class_code_var.get(), self.dataset_var.get(),
             self.id_var.get()))
        # ,name=%s,email=%s,contact=%s,course=%s,div=%s,class_code=%s,dataset=%s     self.name_var.get(),self.email_var.get(),self.contact_var.get(),self.course_var.get(),self.div_var.get(),self.class_code_var.get(),self.dataset_var.get(),
        con.commit()
        self.fetch_student_data2()
        self.clear_student_data()
        con.close()
        messagebox.showinfo("Success", "Successfully updated!!", parent=self.root_student_management)

    # =======delete function==========
    def delete_student_data(self):
        con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
        cur = con.cursor()
        cur.execute("delete from students where id=%s", self.id_var.get())
        con.commit()
        con.close()
        self.fetch_student_data2()
        self.clear_student_data()
        messagebox.showinfo("Success", "Record deleted successfully!!", parent=self.root_student_management)

    # =========search by function========
    def search_student_data_search_by(self):
        if self.search_by_combobox_var.get() == "" or self.search_by_entry_var.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root_student_management)
        else:
            con = pymysql.connect(host="remotemysql.com", user="bY58KYWUaB", password="s2uMZ7iyKn", database="bY58KYWUaB")
            cur = con.cursor()
            cur.execute("select * from students where " + str(self.search_by_combobox_var.get()) + " LIKE '%" + str(
                self.search_by_entry_var.get()) + "%'")
            rows = cur.fetchall()
            if len(rows) != 0:
                self.student_data_view.delete(*self.student_data_view.get_children())
                for row in rows:
                    self.student_data_view.insert('', END, values=row)
                # messagebox.showinfo("Success","Match found!!",parent=self.root_student_management)
                messagebox.showinfo("Success", "Match found!\n\nStudents Count: " + str(len(rows)),
                                    parent=self.root_student_management)
                self.search_by_clear()
            else:
                messagebox.showerror("Error", "no match found", parent=self.root_student_management)
                con.commit()
                self.search_by_clear()
            con.close()
    
    #============admin logout==============
    def logout(self):
        admin_window.destroy()
        login()

    # ===========dataset function================
    def create_dataset_button_function(self):
        if self.id_var.get()=="" or self.username_var.get()=="" or self.name_var.get()=="" or self.email_var.get()=="" or self.contact_var.get()=="" or self.course_var.get()=="" or self.div_var.get()=="" or self.class_code_var.get()=="" or self.dataset_var.get()=="":
            messagebox.showerror("Error","Please mention student ID",parent=self.root_student_management) 
        else:
            create_dataset = messagebox.askyesno("Confirmation","Ready to create a facial dataset..?",parent=self.root_student_management)
            if create_dataset == True:

                haar_file = 'haarcascade_frontalface_default.xml'
                datasets = 'datasets'

                # These are sub data sets of folder,
                # for my faces I've used my name you can
                # change the label here
                sub_data = self.id_var.get()

                path = os.path.join(datasets, sub_data)
                if not os.path.isdir(path):
                    os.mkdir(path)

                    # defining the size of images
                (width, height) = (130, 100)

                # '0' is used for my webcam,
                # if you've any other camera 
                # attached use '1' like this 
                face_cascade = cv2.CascadeClassifier(haar_file)
                webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                # address = "http://192.168.0.101:8080/video"
                # webcam.open(address)

                # The program loops until it has 30 images of the face. 
                count = 0
                while count < 200:
                    (_, im) = webcam.read()
                    cv2.putText(im, 'Please be Still...look into camera', (360, 460), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 255, 255), 1)
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        face = gray[y:y + h, x:x + w]
                        face_resize = cv2.resize(face, (width, height))
                        cv2.imwrite('% s/% s.png' % (path, count), face_resize)
                        cv2.putText(im, str(count), (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
                    count += 1

                    cv2.imshow('Camera', im)
                    if cv2.waitKey(1) == ord(" ") or int(count) == 200:
                        break
                webcam.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("result", "Dataset Collected!!!", parent=self.root_student_management)
                # img=cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
                # img=ImageTk.PhotoImage(Image.fromarray(img))
                # l1["image"]=img
                # cv2.waitKey(10)
                # root3.update()


login = login()


#===========command for py to exe===================
# pyinstaller -F -i images/icon.ico -w --hidden-import "babel.numbers" -n smart_attendance_camera smart_attendance_camera.py