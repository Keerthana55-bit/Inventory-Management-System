from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3

class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.title("Supplier Management | Command Center")
        self.root.config(bg="#0a0e27")
        self.root.resizable(True,True)
        self.root.focus_force()

        #------------ all variables --------------
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.var_sup_invoice=StringVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()
        
        #------------- TOP HEADER --------------
        header = Frame(self.root, bg="#1a1f3a", height=50)
        header.pack(side=TOP, fill=X)
        
        Label(header, text="SUPPLIER MANAGEMENT MODULE", 
              font=("Consolas", 20, "bold"), bg="#1a1f3a", fg="#00d4ff").pack(pady=10)
        
        Frame(self.root, bg="#00d4ff", height=3).pack(side=TOP, fill=X)

        #---------- Search Bar -------------
        search_bar = Frame(self.root, bg="#1a1f3a", height=45)
        search_bar.pack(side=TOP, fill=X, pady=10)
        
        Label(search_bar, text="SEARCH INVOICE:", font=("Consolas", 11, "bold"),
              bg="#1a1f3a", fg="#00d4ff").pack(side=LEFT, padx=50)
        
        Entry(search_bar, textvariable=self.var_searchtxt, font=("Segoe UI", 11),
              bg="#0f1535", fg="white", insertbackground="white").pack(side=LEFT, padx=10)
        
        Button(search_bar, command=self.search, text="SEARCH", 
               font=("Consolas", 10, "bold"), bg="#00d4ff", fg="#0a0e27",
               cursor="hand2", bd=0, padx=20, pady=8).pack(side=LEFT, padx=5)

        #-------------- Form Section ---------------
        form_frame = Frame(self.root, bg="#0a0e27")
        form_frame.place(x=50, y=120, width=620, height=360)

        label_style = {"font": ("Segoe UI", 12), "bg": "#0a0e27", "fg": "#ffffff"}
        entry_style = {"font": ("Segoe UI", 11), "bg": "#0f1535", "fg": "white", "insertbackground": "white"}

        #---------- Form Fields ----------------
        Label(form_frame, text="INVOICE NO:", **label_style).place(x=0, y=0)
        Entry(form_frame, textvariable=self.var_sup_invoice, **entry_style).place(x=130, y=0, width=200)
        
        Label(form_frame, text="NAME:", **label_style).place(x=0, y=45)
        Entry(form_frame, textvariable=self.var_name, **entry_style).place(x=130, y=45, width=200)
        
        Label(form_frame, text="CONTACT:", **label_style).place(x=0, y=90)
        Entry(form_frame, textvariable=self.var_contact, **entry_style).place(x=130, y=90, width=200)
        
        Label(form_frame, text="DESCRIPTION:", **label_style).place(x=0, y=135)
        self.txt_desc=Text(form_frame, font=("Segoe UI", 11), bg="#0f1535",
                          fg="white", insertbackground="white")
        self.txt_desc.place(x=130, y=135, width=470, height=120)
        
        #-------------- Action Buttons -----------------
        btn_style = {"font": ("Consolas", 11, "bold"), "cursor": "hand2", 
                     "bd": 0, "fg": "white"}
        
        Button(form_frame, text="SAVE", command=self.add, bg="#2196f3", 
               **btn_style).place(x=130, y=275, width=110, height=40)
        Button(form_frame, text="UPDATE", command=self.update, bg="#4caf50", 
               **btn_style).place(x=250, y=275, width=110, height=40)
        Button(form_frame, text="DELETE", command=self.delete, bg="#f44336", 
               **btn_style).place(x=370, y=275, width=110, height=40)
        Button(form_frame, text="CLEAR", command=self.clear, bg="#607d8b", 
               **btn_style).place(x=490, y=275, width=110, height=40)

        #------------ Supplier Records Table -------------
        Frame(self.root, bg="#00d4ff", height=2).place(x=680, y=115, width=400)
        
        Label(self.root, text="» SUPPLIER RECORDS", font=("Consolas", 12, "bold"),
              bg="#0a0e27", fg="#00d4ff").place(x=680, y=125)

        sup_frame=Frame(self.root, bd=2, relief=RIDGE, bg="#1a1f3a")
        sup_frame.place(x=680, y=155, width=400, height=325)

        scrolly=Scrollbar(sup_frame, orient=VERTICAL)
        scrollx=Scrollbar(sup_frame, orient=HORIZONTAL)
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#0f1535", foreground="white",
                       fieldbackground="#0f1535", borderwidth=0)
        style.configure("Treeview.Heading", background="#1a1f3a", 
                       foreground="#00d4ff", font=("Consolas", 10, "bold"))
        
        self.SupplierTable=ttk.Treeview(sup_frame,
                                       columns=("invoice","name","contact","desc"),
                                       yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)
        
        self.SupplierTable.heading("invoice",text="Invoice")
        self.SupplierTable.heading("name",text="Name")
        self.SupplierTable.heading("contact",text="Contact")
        self.SupplierTable.heading("desc",text="Description")
        self.SupplierTable["show"]="headings"
        
        self.SupplierTable.column("invoice",width=90)
        self.SupplierTable.column("name",width=100)
        self.SupplierTable.column("contact",width=100)
        self.SupplierTable.column("desc",width=100)
        
        self.SupplierTable.pack(fill=BOTH,expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()

    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Invoice no. is already assigned",parent=self.root)
                else:
                    cur.execute("insert into supplier(invoice,name,contact,desc) values(?,?,?,?)",(
                        self.var_sup_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0',END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Added Successfully",parent=self.root)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from supplier")
            rows=cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def get_data(self,ev):
        f=self.SupplierTable.focus()
        content=(self.SupplierTable.item(f))
        row=content['values']
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0',END)
        self.txt_desc.insert(END,row[3])

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                else:
                    cur.execute("update supplier set name=?,contact=?,desc=? where invoice=?",(
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0',END),
                        self.var_sup_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Updated Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice No. must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Supplier Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0',END)
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Invoice No. should be required",parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?",(self.var_searchtxt.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")


if __name__=="__main__":
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()