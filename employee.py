from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3

class employeeClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.title("Employee Management | Command Center")
        self.root.config(bg="#0a0e27")
        self.root.resizable(True,True)
        self.root.focus_force()

        #------------ all variables --------------
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()
        self.var_salary=StringVar()

        #------------- TOP HEADER --------------
        header = Frame(self.root, bg="#1a1f3a", height=50)
        header.pack(side=TOP, fill=X)
        
        Label(header, text="EMPLOYEE MANAGEMENT MODULE", 
              font=("Consolas", 20, "bold"), bg="#1a1f3a", fg="#00d4ff").pack(pady=10)
        
        Frame(self.root, bg="#00d4ff", height=3).pack(side=TOP, fill=X)

        #---------- Search Frame -------------
        SearchFrame=Frame(self.root, bg="#1a1f3a", bd=0)
        SearchFrame.place(x=250,y=65,width=600,height=50)

        Label(SearchFrame, text="SEARCH:", font=("Consolas", 11, "bold"),
              bg="#1a1f3a", fg="#00d4ff").place(x=10, y=12)

        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,
                               values=("Select","Email","Name","Contact"),
                               state='readonly',font=("Segoe UI", 11))
        cmb_search.place(x=90,y=10,width=150)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,
                        font=("Segoe UI", 11),bg="#0f1535",fg="white",
                        insertbackground="white").place(x=250,y=10,width=180)
        
        btn_search=Button(SearchFrame,command=self.search,text="SEARCH",
                         font=("Consolas", 10, "bold"),bg="#00d4ff",
                         fg="#0a0e27",cursor="hand2",bd=0).place(x=440,y=9,width=140,height=30)

        #-------------- Form Section ---------------
        form_frame = Frame(self.root, bg="#0a0e27")
        form_frame.place(x=50, y=130, width=1000, height=200)

        label_style = {"font": ("Segoe UI", 11), "bg": "#0a0e27", "fg": "#ffffff"}
        entry_style = {"font": ("Segoe UI", 11), "bg": "#0f1535", "fg": "white", "insertbackground": "white"}

        #---------- row 1 ----------------
        Label(form_frame, text="EMP ID:", **label_style).place(x=0,y=0)
        Entry(form_frame,textvariable=self.var_emp_id, **entry_style).place(x=100,y=0,width=180)

        Label(form_frame, text="GENDER:", **label_style).place(x=320,y=0)
        cmb_gender=ttk.Combobox(form_frame,textvariable=self.var_gender,
                               values=("Select","Male","Female","Other"),
                               state='readonly',font=("Segoe UI", 11))
        cmb_gender.place(x=430,y=0,width=180)
        cmb_gender.current(0)

        Label(form_frame, text="CONTACT:", **label_style).place(x=650,y=0)
        Entry(form_frame,textvariable=self.var_contact, **entry_style).place(x=760,y=0,width=180)

        #---------- row 2 ----------------
        Label(form_frame, text="NAME:", **label_style).place(x=0,y=40)
        Entry(form_frame,textvariable=self.var_name, **entry_style).place(x=100,y=40,width=180)

        Label(form_frame, text="D.O.B:", **label_style).place(x=320,y=40)
        Entry(form_frame,textvariable=self.var_dob, **entry_style).place(x=430,y=40,width=180)

        Label(form_frame, text="D.O.J:", **label_style).place(x=650,y=40)
        Entry(form_frame,textvariable=self.var_doj, **entry_style).place(x=760,y=40,width=180)

        #---------- row 3 ----------------
        Label(form_frame, text="EMAIL:", **label_style).place(x=0,y=80)
        Entry(form_frame,textvariable=self.var_email, **entry_style).place(x=100,y=80,width=180)

        Label(form_frame, text="PASSWORD:", **label_style).place(x=320,y=80)
        Entry(form_frame,textvariable=self.var_pass, **entry_style, show="*").place(x=430,y=80,width=180)

        Label(form_frame, text="USER TYPE:", **label_style).place(x=650,y=80)
        cmb_utype=ttk.Combobox(form_frame,textvariable=self.var_utype,
                              values=("Admin","Employee"),state='readonly',
                              font=("Segoe UI", 11))
        cmb_utype.place(x=760,y=80,width=180)
        cmb_utype.current(0)
        
        #---------- row 4 ----------------
        Label(form_frame, text="ADDRESS:", **label_style).place(x=0,y=120)
        self.txt_address=Text(form_frame,font=("Segoe UI", 11),bg="#0f1535",
                             fg="white",insertbackground="white")
        self.txt_address.place(x=100,y=120,width=280,height=60)

        Label(form_frame, text="SALARY:", **label_style).place(x=400,y=120)
        Entry(form_frame,textvariable=self.var_salary, **entry_style).place(x=480,y=120,width=180)
        
        #-------------- buttons -----------------
        btn_style = {"font": ("Consolas", 11, "bold"), "cursor": "hand2", 
                     "bd": 0, "fg": "white"}
        
        Button(form_frame, text="SAVE", command=self.add, bg="#2196f3", 
               **btn_style).place(x=700,y=130,width=110,height=35)
        Button(form_frame, text="UPDATE", command=self.update, bg="#4caf50", 
               **btn_style).place(x=820,y=130,width=110,height=35)
        Button(form_frame, text="DELETE", command=self.delete, bg="#f44336", 
               **btn_style).place(x=700,y=170,width=110,height=35)
        Button(form_frame, text="CLEAR", command=self.clear, bg="#607d8b", 
               **btn_style).place(x=820,y=170,width=110,height=35)

        #------------ employee details -------------
        Frame(self.root, bg="#00d4ff", height=2).place(x=0, y=340, width=1100)
        
        Label(self.root, text="» EMPLOYEE RECORDS", font=("Consolas", 12, "bold"),
              bg="#0a0e27", fg="#00d4ff").place(x=50, y=350)

        emp_frame=Frame(self.root,bd=2,relief=RIDGE,bg="#1a1f3a")
        emp_frame.place(x=50,y=380,width=1000,height=110)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#0f1535", foreground="white",
                       fieldbackground="#0f1535", borderwidth=0)
        style.configure("Treeview.Heading", background="#1a1f3a", 
                       foreground="#00d4ff", font=("Consolas", 10, "bold"))
        
        self.EmployeeTable=ttk.Treeview(emp_frame,
                                       columns=("eid","name","email","gender","contact","dob","doj","pass","utype","address","salary"),
                                       yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)
        
        self.EmployeeTable.heading("eid",text="EMP ID")
        self.EmployeeTable.heading("name",text="Name")
        self.EmployeeTable.heading("email",text="Email")
        self.EmployeeTable.heading("gender",text="Gender")
        self.EmployeeTable.heading("contact",text="Contact")
        self.EmployeeTable.heading("dob",text="D.O.B")
        self.EmployeeTable.heading("doj",text="D.O.J")
        self.EmployeeTable.heading("pass",text="Password")
        self.EmployeeTable.heading("utype",text="User Type")
        self.EmployeeTable.heading("address",text="Address")
        self.EmployeeTable.heading("salary",text="Salary")
        self.EmployeeTable["show"]="headings"
        
        self.EmployeeTable.column("eid",width=90)
        self.EmployeeTable.column("name",width=100)
        self.EmployeeTable.column("email",width=100)
        self.EmployeeTable.column("gender",width=100)
        self.EmployeeTable.column("contact",width=100)
        self.EmployeeTable.column("dob",width=100)
        self.EmployeeTable.column("doj",width=100)
        self.EmployeeTable.column("pass",width=100)
        self.EmployeeTable.column("utype",width=100)
        self.EmployeeTable.column("address",width=100)
        self.EmployeeTable.column("salary",width=100)
        
        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()

    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Employee ID is already assigned",parent=self.root)
                else:
                    cur.execute("insert into employee(eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                        self.var_emp_id.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0',END),
                        self.var_salary.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Added Successfully",parent=self.root)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from employee")
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete('1.0',END)
        self.txt_address.insert(END,row[9])
        self.var_salary.set(row[10])

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                else:
                    cur.execute("update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",(
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0',END),
                        self.var_salary.get(),
                        self.var_emp_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Updated Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from employee where eid=?",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Employee Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete('1.0',END)
        self.var_salary.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search By option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select * from employee where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")


if __name__=="__main__":
    root=Tk()
    obj=employeeClass(root)
    root.mainloop()