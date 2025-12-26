from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import os

class salesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.title("Sales Management | Command Center")
        self.root.config(bg="#0a0e27")
        self.root.resizable(True,True)
        self.root.focus_force()

        self.blll_list=[]
        self.var_invoice=StringVar()
        
        #------------- TOP HEADER --------------
        header = Frame(self.root, bg="#1a1f3a", height=50)
        header.pack(side=TOP, fill=X)
        
        Label(header, text="SALES MANAGEMENT MODULE", 
              font=("Consolas", 20, "bold"), bg="#1a1f3a", fg="#00d4ff").pack(pady=10)
        
        Frame(self.root, bg="#00d4ff", height=3).pack(side=TOP, fill=X)
        
        #-------------- Search Section ---------------
        search_frame = Frame(self.root, bg="#0a0e27")
        search_frame.place(x=50, y=70, width=1000, height=50)
        
        Label(search_frame, text="INVOICE NO:", font=("Consolas", 12, "bold"),
              bg="#0a0e27", fg="#00d4ff").place(x=0, y=12)
        
        Entry(search_frame, textvariable=self.var_invoice, font=("Segoe UI", 11),
              bg="#0f1535", fg="white", insertbackground="white").place(x=140, y=10, width=200)

        btn_style = {"font": ("Consolas", 10, "bold"), "cursor": "hand2", 
                     "bd": 0, "fg": "white"}
        
        Button(search_frame, text="SEARCH", command=self.search, bg="#2196f3", 
               **btn_style).place(x=360, y=8, width=120, height=35)
        Button(search_frame, text="CLEAR", command=self.clear, bg="#607d8b", 
               **btn_style).place(x=500, y=8, width=120, height=35)

        #----------------- Bill List -------------------
        Frame(self.root, bg="#00d4ff", height=2).place(x=50, y=130, width=250)
        
        Label(self.root, text="» INVOICE LIST", font=("Consolas", 11, "bold"),
              bg="#0a0e27", fg="#00d4ff").place(x=50, y=140)

        sales_Frame=Frame(self.root, bd=2, relief=RIDGE, bg="#1a1f3a")
        sales_Frame.place(x=50, y=170, width=250, height=310)

        scrolly=Scrollbar(sales_Frame, orient=VERTICAL)
        self.Sales_List=Listbox(sales_Frame, font=("Consolas", 11), 
                                bg="#0f1535", fg="white", 
                                yscrollcommand=scrolly.set,
                                selectbackground="#00d4ff",
                                selectforeground="#0a0e27")
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH, expand=1)
        self.Sales_List.bind("<ButtonRelease-1>", self.get_data)

        #--------------- Bill Display Area ----------------------
        Frame(self.root, bg="#00d4ff", height=2).place(x=320, y=130, width=450)
        
        Label(self.root, text="» BILL PREVIEW", font=("Consolas", 11, "bold"),
              bg="#0a0e27", fg="#00d4ff").place(x=320, y=140)

        bill_Frame=Frame(self.root, bd=2, relief=RIDGE, bg="#1a1f3a")
        bill_Frame.place(x=320, y=170, width=450, height=310)
        
        scrolly2=Scrollbar(bill_Frame, orient=VERTICAL)
        self.bill_area=Text(bill_Frame, bg="#0f1535", fg="white",
                           font=("Consolas", 10), yscrollcommand=scrolly2.set,
                           insertbackground="white")
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        #------------- Summary Info -----------------
        Frame(self.root, bg="#00d4ff", height=2).place(x=790, y=130, width=280)
        
        Label(self.root, text="» QUICK STATS", font=("Consolas", 11, "bold"),
              bg="#0a0e27", fg="#00d4ff").place(x=790, y=140)

        stats_frame = Frame(self.root, bg="#1a1f3a", bd=2, relief=RIDGE)
        stats_frame.place(x=790, y=170, width=280, height=310)
        
        Label(stats_frame, text="Total Bills", font=("Segoe UI", 12, "bold"),
              bg="#1a1f3a", fg="#ffffff").place(x=20, y=20)
        self.lbl_total_bills = Label(stats_frame, text="0", 
                                    font=("Consolas", 32, "bold"),
                                    bg="#1a1f3a", fg="#00d4ff")
        self.lbl_total_bills.place(x=20, y=60)
        
        Label(stats_frame, text="Selected Invoice", font=("Segoe UI", 11),
              bg="#1a1f3a", fg="#7f8fa6").place(x=20, y=140)
        self.lbl_selected = Label(stats_frame, text="None", 
                                 font=("Consolas", 12, "bold"),
                                 bg="#1a1f3a", fg="#ffffff")
        self.lbl_selected.place(x=20, y=170)
        
        Label(stats_frame, text="Database Status", font=("Segoe UI", 11),
              bg="#1a1f3a", fg="#7f8fa6").place(x=20, y=220)
        Label(stats_frame, text="● CONNECTED", font=("Consolas", 11, "bold"),
              bg="#1a1f3a", fg="#00ff88").place(x=20, y=250)
        
        self.show()

    def show(self):
        del self.blll_list[:]
        self.Sales_List.delete(0, END)
        bill_count = 0
        for i in os.listdir('Inventory-Management-System/bill'):
            if i.split('.')[-1]=='txt':
                self.Sales_List.insert(END, i)
                self.blll_list.append(i.split('.')[0])
                bill_count += 1
        self.lbl_total_bills.config(text=str(bill_count))

    def get_data(self, ev):
        index_=self.Sales_List.curselection()
        file_name=self.Sales_List.get(index_)
        self.lbl_selected.config(text=file_name.split('.')[0])
        self.bill_area.delete('1.0', END)
        fp=open(f'Inventory-Management-System/bill/{file_name}', 'r')
        for i in fp:
            self.bill_area.insert(END, i)
        fp.close()

    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice no. should be required",parent=self.root)
        else:
            if self.var_invoice.get() in self.blll_list:
                fp=open(f'Inventory-Management-System/bill/{self.var_invoice.get()}.txt', 'r')
                self.bill_area.delete('1.0', END)
                for i in fp:
                    self.bill_area.insert(END, i)
                fp.close()
                self.lbl_selected.config(text=self.var_invoice.get())
            else:
                messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete('1.0', END)
        self.lbl_selected.config(text="None")
        self.var_invoice.set("")


if __name__=="__main__":
    root=Tk()
    obj=salesClass(root)
    root.mainloop()