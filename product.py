from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3

class productClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.title("Product Management | Command Center")
        self.root.config(bg="#0a0e27")
        self.root.resizable(True,True)
        self.root.focus_force()
        
        #----------- variables -------------
        self.var_cat=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()
        self.var_pid=StringVar()
        self.var_sup=StringVar()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        #------------- TOP HEADER --------------
        header = Frame(self.root, bg="#1a1f3a", height=50)
        header.pack(side=TOP, fill=X)
        
        Label(header, text="PRODUCT MANAGEMENT MODULE", 
              font=("Consolas", 20, "bold"), bg="#1a1f3a", fg="#00d4ff").pack(pady=10)
        
        Frame(self.root, bg="#00d4ff", height=3).pack(side=TOP, fill=X)

        #---------- LEFT PANEL: Form -------------
        product_Frame=Frame(self.root, bg="#0a0e27")
        product_Frame.place(x=20, y=70, width=440, height=420)

        Label(product_Frame, text="» PRODUCT DETAILS", font=("Consolas", 12, "bold"),
              bg="#0a0e27", fg="#00d4ff").pack(anchor=W, pady=5)

        label_style = {"font": ("Segoe UI", 11), "bg": "#0a0e27", "fg": "#ffffff"}
        entry_style = {"font": ("Segoe UI", 11), "bg": "#0f1535", "fg": "white", "insertbackground": "white"}

        Label(product_Frame, text="Category", **label_style).place(x=10, y=40)
        cmb_cat=ttk.Combobox(product_Frame, textvariable=self.var_cat, 
                            values=self.cat_list, state='readonly', font=("Segoe UI", 11))
        cmb_cat.place(x=130, y=40, width=280)
        cmb_cat.current(0)

        Label(product_Frame, text="Supplier", **label_style).place(x=10, y=80)
        cmb_sup=ttk.Combobox(product_Frame, textvariable=self.var_sup, 
                            values=self.sup_list, state='readonly', font=("Segoe UI", 11))
        cmb_sup.place(x=130, y=80, width=280)
        cmb_sup.current(0)

        Label(product_Frame, text="Name", **label_style).place(x=10, y=120)
        Entry(product_Frame, textvariable=self.var_name, **entry_style).place(x=130, y=120, width=280)

        Label(product_Frame, text="Price", **label_style).place(x=10, y=160)
        Entry(product_Frame, textvariable=self.var_price, **entry_style).place(x=130, y=160, width=280)

        Label(product_Frame, text="Quantity", **label_style).place(x=10, y=200)
        Entry(product_Frame, textvariable=self.var_qty, **entry_style).place(x=130, y=200, width=280)

        Label(product_Frame, text="Status", **label_style).place(x=10, y=240)
        cmb_status=ttk.Combobox(product_Frame, textvariable=self.var_status, 
                               values=("Active","Inactive"), state='readonly', font=("Segoe UI", 11))
        cmb_status.place(x=130, y=240, width=280)
        cmb_status.current(0)

        #-------------- buttons -----------------
        btn_style = {"font": ("Consolas", 10, "bold"), "cursor": "hand2", 
                     "bd": 0, "fg": "white"}
        
        Button(product_Frame, text="SAVE", command=self.add, bg="#2196f3", 
               **btn_style).place(x=10, y=300, width=95, height=40)
        Button(product_Frame, text="UPDATE", command=self.update, bg="#4caf50", 
               **btn_style).place(x=115, y=300, width=95, height=40)
        Button(product_Frame, text="DELETE", command=self.delete, bg="#f44336", 
               **btn_style).place(x=220, y=300, width=95, height=40)
        Button(product_Frame, text="CLEAR", command=self.clear, bg="#607d8b", 
               **btn_style).place(x=325, y=300, width=95, height=40)

        #---------- RIGHT PANEL: Search & Table -------------
        SearchFrame=Frame(self.root, bg="#1a1f3a", bd=0)
        SearchFrame.place(x=480, y=70, width=600, height=50)

        Label(SearchFrame, text="SEARCH:", font=("Consolas", 11, "bold"),
              bg="#1a1f3a", fg="#00d4ff").place(x=10, y=12)

        cmb_search=ttk.Combobox(SearchFrame, textvariable=self.var_searchby,
                               values=("Select","Category","Supplier","Name"),
                               state='readonly', font=("Segoe UI", 11))
        cmb_search.place(x=90, y=10, width=150)
        cmb_search.current(0)

        Entry(SearchFrame, textvariable=self.var_searchtxt, font=("Segoe UI", 11),
              bg="#0f1535", fg="white", insertbackground="white").place(x=250, y=10, width=180)
        
        Button(SearchFrame, text="SEARCH", command=self.search, 
               font=("Consolas", 10, "bold"), bg="#00d4ff", fg="#0a0e27",
               cursor="hand2", bd=0).place(x=440, y=9, width=140, height=30)

        #------------ product details table -------------
        Frame(self.root, bg="#00d4ff", height=2).place(x=480, y=130, width=600)
        
        Label(self.root, text="» PRODUCT RECORDS", font=("Consolas", 12, "bold"),
              bg="#0a0e27", fg="#00d4ff").place(x=480, y=140)

        product_frame=Frame(self.root, bd=2, relief=RIDGE, bg="#1a1f3a")
        product_frame.place(x=480, y=170, width=600, height=320)

        scrolly=Scrollbar(product_frame, orient=VERTICAL)
        scrollx=Scrollbar(product_frame, orient=HORIZONTAL)
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#0f1535", foreground="white",
                       fieldbackground="#0f1535", borderwidth=0)
        style.configure("Treeview.Heading", background="#1a1f3a", 
                       foreground="#00d4ff", font=("Consolas", 9, "bold"))
        
        self.ProductTable=ttk.Treeview(product_frame,
                                      columns=("pid","Category","Supplier","name","price","qty","status"),
                                      yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)
        
        self.ProductTable.heading("pid", text="P ID")
        self.ProductTable.heading("Category", text="Category")
        self.ProductTable.heading("Supplier", text="Supplier")
        self.ProductTable.heading("name", text="Name")
        self.ProductTable.heading("price", text="Price")
        self.ProductTable.heading("qty", text="Qty")
        self.ProductTable.heading("status", text="Status")
        self.ProductTable["show"]="headings"
        
        self.ProductTable.column("pid", width=60)
        self.ProductTable.column("Category", width=100)
        self.ProductTable.column("Supplier", width=100)
        self.ProductTable.column("name", width=100)
        self.ProductTable.column("price", width=80)
        self.ProductTable.column("qty", width=60)
        self.ProductTable.column("status", width=80)
        
        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()
        self.fetch_cat_sup()

    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select name from category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            cur.execute("select name from supplier")
            sup=cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
    
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup=="Select" or self.var_sup=="Empty":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute("Select * from product where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Product already present",parent=self.root)
                else:
                    cur.execute("insert into product(Category,Supplier,name,price,qty,status) values(?,?,?,?,?,?)",(
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product Added Successfully",parent=self.root)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def get_data(self,ev):
        f=self.ProductTable.focus()
        content=(self.ProductTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Please select product from list",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    cur.execute("update product set Category=?,Supplier=?,name=?,price=?,qty=?,status=? where pid=?",(
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                        self.var_pid.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product Updated Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Select Product from the list",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Product Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
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
                cur.execute("select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

if __name__=="__main__":
    root=Tk()
    obj=productClass(root)
    root.mainloop()