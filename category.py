from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3

class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.title("Category Management | Command Center")
        self.root.config(bg="#0a0e27")
        self.root.resizable(True,True)
        self.root.focus_force()

        #------------ variables -------------
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
        
        #------------- TOP HEADER --------------
        header = Frame(self.root, bg="#1a1f3a", height=50)
        header.pack(side=TOP, fill=X)
        
        Label(header, text="CATEGORY MANAGEMENT MODULE", 
              font=("Consolas", 20, "bold"), bg="#1a1f3a", fg="#00d4ff").pack(pady=10)
        
        Frame(self.root, bg="#00d4ff", height=3).pack(side=TOP, fill=X)

        #-------------- Input Section ---------------
        input_frame = Frame(self.root, bg="#0a0e27")
        input_frame.place(x=50, y=80, width=650, height=120)
        
        Label(input_frame, text="CATEGORY NAME:", font=("Segoe UI", 14, "bold"),
              bg="#0a0e27", fg="#ffffff").place(x=0, y=20)
        
        Entry(input_frame, textvariable=self.var_name, font=("Segoe UI", 13),
              bg="#0f1535", fg="white", insertbackground="white").place(x=200, y=20, width=300)

        #-------------- Action Buttons -----------------
        btn_style = {"font": ("Consolas", 12, "bold"), "cursor": "hand2", 
                     "bd": 0, "fg": "white"}
        
        Button(input_frame, text="ADD", command=self.add, bg="#4caf50", 
               **btn_style).place(x=200, y=70, width=140, height=40)
        Button(input_frame, text="DELETE", command=self.delete, bg="#f44336", 
               **btn_style).place(x=360, y=70, width=140, height=40)

        #------------ Category Records Table -------------
        Frame(self.root, bg="#00d4ff", height=2).place(x=50, y=215, width=1000)
        
        Label(self.root, text="» CATEGORY RECORDS", font=("Consolas", 14, "bold"),
              bg="#0a0e27", fg="#00d4ff").place(x=50, y=225)

        cat_frame=Frame(self.root, bd=2, relief=RIDGE, bg="#1a1f3a")
        cat_frame.place(x=50, y=260, width=1000, height=150)

        scrolly=Scrollbar(cat_frame, orient=VERTICAL)
        scrollx=Scrollbar(cat_frame, orient=HORIZONTAL)
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#0f1535", foreground="white",
                       fieldbackground="#0f1535", borderwidth=0, rowheight=30)
        style.configure("Treeview.Heading", background="#1a1f3a", 
                       foreground="#00d4ff", font=("Consolas", 11, "bold"))
        
        self.CategoryTable=ttk.Treeview(cat_frame, columns=("cid","name"),
                                       yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)
        
        self.CategoryTable.heading("cid",text="CATEGORY ID")
        self.CategoryTable.heading("name",text="CATEGORY NAME")
        self.CategoryTable["show"]="headings"
        
        self.CategoryTable.column("cid",width=200, anchor=CENTER)
        self.CategoryTable.column("name",width=400, anchor=CENTER)
        
        self.CategoryTable.pack(fill=BOTH,expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()

        #----------------- Bottom Info ---------------------
        Label(self.root, text="» Click on any record to select and delete",
              font=("Segoe UI", 10), bg="#0a0e27", fg="#7f8fa6").place(x=50, y=420)

    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Category Name must be required",parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Category already present",parent=self.root)
                else:
                    cur.execute("insert into category(name) values(?)",(
                        self.var_name.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Category Added Successfully",parent=self.root)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from category")
            rows=cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def clear(self):
        self.var_name.set("")
        self.show()

    def get_data(self,ev):
        f=self.CategoryTable.focus()
        content=(self.CategoryTable.item(f))
        row=content['values']
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])
    
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","Select category from the list",parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Category",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Category Deleted Successfully",parent=self.root)
                        self.clear()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")


if __name__=="__main__":
    root=Tk()
    obj=categoryClass(root)
    root.mainloop()