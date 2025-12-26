from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile

class billClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1400x750+100+50")
        self.root.title("Billing System | Command Center")
        self.root.resizable(True,True)
        self.root.config(bg="#0a0e27")
        self.cart_list=[]
        self.chk_print=0

        #------------- TOP HEADER --------------
        header = Frame(self.root, bg="#1a1f3a", height=60)
        header.pack(side=TOP, fill=X)
        
        # Logo and title
        try:
            self.icon_title = PhotoImage(file="Inventory-Management-System/images/logo1.png")
            Label(header, text="BILLING SYSTEM", image=self.icon_title, compound=LEFT,
                  font=("Consolas", 24, "bold"), bg="#1a1f3a", fg="#00d4ff").pack(side=LEFT, padx=20)
        except:
            Label(header, text="💳 BILLING SYSTEM",
                  font=("Consolas", 24, "bold"), bg="#1a1f3a", fg="#00d4ff").pack(side=LEFT, padx=20)
        
        # Logout button
        btn_logout=Button(header, text="LOGOUT ►", font=("Segoe UI", 11, "bold"),
                         bg="#ff4757", fg="white", cursor="hand2", bd=0,
                         activebackground="#ee2f3c", activeforeground="white",
                         padx=20, pady=10)
        btn_logout.pack(side=RIGHT, padx=20)
        
        # Accent line
        Frame(self.root, bg="#00d4ff", height=3).pack(side=TOP, fill=X)

        #------------ clock -----------------
        self.lbl_clock=Label(self.root, text="System Online • Loading...",
                            font=("Segoe UI", 11), bg="#0f1535", fg="#7f8fa6")
        self.lbl_clock.pack(side=TOP, fill=X, pady=5)

        #------------ footer -----------------
        lbl_footer=Label(self.root, text="IMS v2.0 • Developed by Keerthana Pathipati • Support: keerthanapathipati236@gmail.com",
                        font=("Segoe UI", 9), bg="#0a0e27", fg="#535c68")
        lbl_footer.pack(side=BOTTOM, fill=X, pady=10)

        #-------------- LEFT: Product frame -----------------
        ProductFrame1=Frame(self.root, bd=0, relief=FLAT, bg="#0a0e27")
        ProductFrame1.place(x=20, y=110, width=420, height=600)

        Label(ProductFrame1, text="» PRODUCT CATALOG", font=("Consolas", 14, "bold"),
              bg="#0a0e27", fg="#00d4ff").pack(side=TOP, fill=X, pady=5)
        
        self.var_search=StringVar()

        # Search section
        ProductFrame2=Frame(ProductFrame1, bd=2, relief=RIDGE, bg="#1a1f3a")
        ProductFrame2.place(x=0, y=35, width=420, height=90)

        Label(ProductFrame2, text="SEARCH PRODUCTS", font=("Segoe UI", 11, "bold"),
              bg="#1a1f3a", fg="#00d4ff").place(x=10, y=10)
        
        Label(ProductFrame2, text="Product Name:", font=("Segoe UI", 10),
              bg="#1a1f3a", fg="#ffffff").place(x=10, y=45)
        Entry(ProductFrame2, textvariable=self.var_search, font=("Segoe UI", 11),
              bg="#0f1535", fg="white", insertbackground="white").place(x=120, y=43, width=170)
        
        Button(ProductFrame2, text="SEARCH", command=self.search, 
               font=("Consolas", 9, "bold"), bg="#2196f3", fg="white",
               cursor="hand2", bd=0).place(x=300, y=40, width=100, height=25)
        Button(ProductFrame2, text="SHOW ALL", command=self.show,
               font=("Consolas", 9, "bold"), bg="#4caf50", fg="white",
               cursor="hand2", bd=0).place(x=300, y=10, width=100, height=25)

        # Product table
        ProductFrame3=Frame(ProductFrame1, bd=2, relief=RIDGE, bg="#1a1f3a")
        ProductFrame3.place(x=0, y=135, width=420, height=410)

        scrolly=Scrollbar(ProductFrame3, orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3, orient=HORIZONTAL)
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#0f1535", foreground="white",
                       fieldbackground="#0f1535", borderwidth=0, rowheight=25)
        style.configure("Treeview.Heading", background="#1a1f3a", 
                       foreground="#00d4ff", font=("Consolas", 10, "bold"))
        
        self.product_Table=ttk.Treeview(ProductFrame3,
                                       columns=("pid","name","price","qty","status"),
                                       yscrollcommand=scrolly.set,
                                       xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)
        
        self.product_Table.heading("pid", text="ID")
        self.product_Table.heading("name", text="Product Name")
        self.product_Table.heading("price", text="Price")
        self.product_Table.heading("qty", text="Qty")
        self.product_Table.heading("status", text="Status")
        self.product_Table["show"]="headings"
        
        self.product_Table.column("pid", width=50, anchor=CENTER)
        self.product_Table.column("name", width=150)
        self.product_Table.column("price", width=80, anchor=CENTER)
        self.product_Table.column("qty", width=60, anchor=CENTER)
        self.product_Table.column("status", width=80, anchor=CENTER)
        
        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)

        Label(ProductFrame1, text="💡 Enter 0 quantity to remove product from cart",
              font=("Segoe UI", 9), bg="#0a0e27", fg="#7f8fa6").place(x=0, y=555)

        self.show()

        #-------------- CENTER: Customer & Calculator ---------------
        self.var_cname=StringVar()
        self.var_contact=StringVar()

        # Customer details
        CustomerFrame=Frame(self.root, bd=2, relief=RIDGE, bg="#1a1f3a")
        CustomerFrame.place(x=460, y=110, width=480, height=90)

        Label(CustomerFrame, text="» CUSTOMER DETAILS", font=("Consolas", 12, "bold"),
              bg="#1a1f3a", fg="#00d4ff").pack(side=TOP, fill=X, pady=5, padx=10)

        Label(CustomerFrame, text="Name:", font=("Segoe UI", 11),
              bg="#1a1f3a", fg="#ffffff").place(x=10, y=40)
        Entry(CustomerFrame, textvariable=self.var_cname, font=("Segoe UI", 11),
              bg="#0f1535", fg="white", insertbackground="white").place(x=80, y=38, width=170)
        
        Label(CustomerFrame, text="Contact:", font=("Segoe UI", 11),
              bg="#1a1f3a", fg="#ffffff").place(x=260, y=40)
        Entry(CustomerFrame, textvariable=self.var_contact, font=("Segoe UI", 11),
              bg="#0f1535", fg="white", insertbackground="white").place(x=330, y=38, width=140)

        # Calculator & Cart container
        Cal_Cart_Frame=Frame(self.root, bd=0, relief=FLAT, bg="#0a0e27")
        Cal_Cart_Frame.place(x=460, y=210, width=480, height=390)

        #--------------- Calculator ---------------------
        self.var_cal_input=StringVar()

        Cal_Frame=Frame(Cal_Cart_Frame, bd=2, relief=RIDGE, bg="#1a1f3a")
        Cal_Frame.place(x=0, y=0, width=230, height=390)

        Label(Cal_Frame, text="» CALCULATOR", font=("Consolas", 11, "bold"),
              bg="#1a1f3a", fg="#00d4ff").pack(fill=X, pady=5)

        self.txt_cal_input=Entry(Cal_Frame, textvariable=self.var_cal_input,
                                 font=('Consolas', 14, 'bold'), bd=5,
                                 relief=GROOVE, state='readonly', justify=RIGHT,
                                 bg="#0f1535", fg="#00d4ff", insertbackground="#00d4ff")
        self.txt_cal_input.pack(fill=X, padx=10, pady=5)

        btn_frame = Frame(Cal_Frame, bg="#1a1f3a")
        btn_frame.pack(expand=True, fill=BOTH, padx=10, pady=5)

        btn_style = {"font": ('Consolas', 12, 'bold'), "bd": 2, "cursor": "hand2",
                    "bg": "#0f1535", "fg": "#ffffff", "activebackground": "#00d4ff",
                    "activeforeground": "#0a0e27"}

        # Calculator buttons
        Button(btn_frame, text='7', command=lambda:self.get_input(7), **btn_style).grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        Button(btn_frame, text='8', command=lambda:self.get_input(8), **btn_style).grid(row=0, column=1, padx=2, pady=2, sticky="nsew")
        Button(btn_frame, text='9', command=lambda:self.get_input(9), **btn_style).grid(row=0, column=2, padx=2, pady=2, sticky="nsew")
        Button(btn_frame, text='+', command=lambda:self.get_input('+'), bg="#4caf50", fg="white", font=('Consolas', 12, 'bold'), bd=2, cursor="hand2").grid(row=0, column=3, padx=2, pady=2, sticky="nsew")

        Button(btn_frame, text='4', command=lambda:self.get_input(4), **btn_style).grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        Button(btn_frame, text='5', command=lambda:self.get_input(5), **btn_style).grid(row=1, column=1, padx=2, pady=2, sticky="nsew")
        Button(btn_frame, text='6', command=lambda:self.get_input(6), **btn_style).grid(row=1, column=2, padx=2, pady=2, sticky="nsew")
        Button(btn_frame, text='-', command=lambda:self.get_input('-'), bg="#ff9800", fg="white", font=('Consolas', 12, 'bold'), bd=2, cursor="hand2").grid(row=1, column=3, padx=2, pady=2, sticky="nsew")

        Button(btn_frame, text='1', command=lambda:self.get_input(1), **btn_style).grid(row=2, column=0, padx=2, pady=2, sticky="nsew")
        Button(btn_frame, text='2', command=lambda:self.get_input(2), **btn_style).grid(row=2, column=1, padx=2, pady=2, sticky="nsew")
        Button(btn_frame, text='3', command=lambda:self.get_input(3), **btn_style).grid(row=2, column=2, padx=2, pady=2, sticky="nsew")
        Button(btn_frame, text='*', command=lambda:self.get_input('*'), bg="#9c27b0", fg="white", font=('Consolas', 12, 'bold'), bd=2, cursor="hand2").grid(row=2, column=3, padx=2, pady=2, sticky="nsew")

        Button(btn_frame, text='0', command=lambda:self.get_input(0), **btn_style).grid(row=3, column=0, padx=2, pady=2, sticky="nsew")
        Button(btn_frame, text='C', command=self.clear_cal, bg="#f44336", fg="white", font=('Consolas', 12, 'bold'), bd=2, cursor="hand2").grid(row=3, column=1, padx=2, pady=2, sticky="nsew")
        Button(btn_frame, text='=', command=self.perform_cal, bg="#2196f3", fg="white", font=('Consolas', 12, 'bold'), bd=2, cursor="hand2").grid(row=3, column=2, padx=2, pady=2, sticky="nsew")
        Button(btn_frame, text='/', command=lambda:self.get_input('/'), bg="#607d8b", fg="white", font=('Consolas', 12, 'bold'), bd=2, cursor="hand2").grid(row=3, column=3, padx=2, pady=2, sticky="nsew")

        for i in range(4):
            btn_frame.grid_rowconfigure(i, weight=1)
            btn_frame.grid_columnconfigure(i, weight=1)

        #------------------ Cart frame --------------------
        Cart_Frame=Frame(Cal_Cart_Frame, bd=2, relief=RIDGE, bg="#1a1f3a")
        Cart_Frame.place(x=240, y=0, width=240, height=390)
        
        self.cartTitle=Label(Cart_Frame, text="» CART [0]", 
                            font=("Consolas", 11, "bold"), bg="#1a1f3a", fg="#00d4ff")
        self.cartTitle.pack(side=TOP, fill=X, pady=5)

        scrolly=Scrollbar(Cart_Frame, orient=VERTICAL)
        scrollx=Scrollbar(Cart_Frame, orient=HORIZONTAL)
        
        self.CartTable=ttk.Treeview(Cart_Frame,
                                    columns=("pid","name","price","qty"),
                                    yscrollcommand=scrolly.set,
                                    xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        
        self.CartTable.heading("pid", text="ID")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="Qty")
        self.CartTable["show"]="headings"
        
        self.CartTable.column("pid", width=40, anchor=CENTER)
        self.CartTable.column("name", width=100)
        self.CartTable.column("price", width=60, anchor=CENTER)
        self.CartTable.column("qty", width=40, anchor=CENTER)
        
        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        #-------------- Add to cart widgets ---------------
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()

        Add_CartWidgets_Frame=Frame(self.root, bd=2, relief=RIDGE, bg="#1a1f3a")
        Add_CartWidgets_Frame.place(x=460, y=610, width=480, height=100)

        Label(Add_CartWidgets_Frame, text="» ADD TO CART", font=("Consolas", 11, "bold"),
              bg="#1a1f3a", fg="#00d4ff").pack(fill=X, pady=3, padx=10)

        # Product details row
        details_frame = Frame(Add_CartWidgets_Frame, bg="#1a1f3a")
        details_frame.pack(fill=X, padx=10, pady=5)

        Label(details_frame, text="Product:", font=("Segoe UI", 9),
              bg="#1a1f3a", fg="#ffffff").grid(row=0, column=0, sticky=W)
        Entry(details_frame, textvariable=self.var_pname, font=("Segoe UI", 9),
              bg="#0f1535", fg="white", state='readonly', width=18).grid(row=0, column=1, padx=5)

        Label(details_frame, text="Price:", font=("Segoe UI", 9),
              bg="#1a1f3a", fg="#ffffff").grid(row=0, column=2, sticky=W)
        Entry(details_frame, textvariable=self.var_price, font=("Segoe UI", 9),
              bg="#0f1535", fg="white", state='readonly', width=10).grid(row=0, column=3, padx=5)

        Label(details_frame, text="Qty:", font=("Segoe UI", 9),
              bg="#1a1f3a", fg="#ffffff").grid(row=0, column=4, sticky=W)
        Entry(details_frame, textvariable=self.var_qty, font=("Segoe UI", 9),
              bg="#0f1535", fg="white", insertbackground="white", width=8).grid(row=0, column=5, padx=5)

        # Stock and buttons
        button_frame = Frame(Add_CartWidgets_Frame, bg="#1a1f3a")
        button_frame.pack(fill=X, padx=10, pady=5)

        self.lbl_inStock=Label(button_frame, text="In Stock: -",
                              font=("Segoe UI", 9, "bold"), bg="#1a1f3a", fg="#00ff88")
        self.lbl_inStock.pack(side=LEFT)

        Button(button_frame, text="ADD | UPDATE", command=self.add_update_cart,
               font=("Consolas", 10, "bold"), bg="#4caf50", fg="white",
               cursor="hand2", bd=0, padx=15, pady=5).pack(side=RIGHT, padx=5)
        
        Button(button_frame, text="CLEAR", command=self.clear_cart,
               font=("Consolas", 10, "bold"), bg="#607d8b", fg="white",
               cursor="hand2", bd=0, padx=15, pady=5).pack(side=RIGHT)

        #------------------- RIGHT: Bill Area -------------------
        billFrame=Frame(self.root, bd=2, relief=RIDGE, bg="#1a1f3a")
        billFrame.place(x=960, y=110, width=420, height=490)

        Label(billFrame, text="» INVOICE", font=("Consolas", 14, "bold"),
              bg="#1a1f3a", fg="#00d4ff").pack(side=TOP, fill=X, pady=5)
        
        scrolly=Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area=Text(billFrame, yscrollcommand=scrolly.set,
                               font=("Courier", 10), bg="#0f1535", fg="#ffffff",
                               insertbackground="white")
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #------------------- Billing summary & buttons -----------------------
        billMenuFrame=Frame(self.root, bd=2, relief=RIDGE, bg="#1a1f3a")
        billMenuFrame.place(x=960, y=610, width=420, height=100)

        # Summary labels
        summary_frame = Frame(billMenuFrame, bg="#1a1f3a")
        summary_frame.pack(fill=X, padx=5, pady=5)

        self.lbl_amnt=Label(summary_frame, text="Bill Amount\n₹ 0",
                           font=("Consolas", 11, "bold"), bg="#6c5ce7", fg="white",
                           width=13, pady=8)
        self.lbl_amnt.pack(side=LEFT, padx=3)

        self.lbl_discount=Label(summary_frame, text="Discount (5%)\n₹ 0",
                               font=("Consolas", 11, "bold"), bg="#00b894", fg="white",
                               width=13, pady=8)
        self.lbl_discount.pack(side=LEFT, padx=3)

        self.lbl_net_pay=Label(summary_frame, text="Net Pay\n₹ 0",
                              font=("Consolas", 11, "bold"), bg="#00d4ff", fg="#0a0e27",
                              width=13, pady=8)
        self.lbl_net_pay.pack(side=LEFT, padx=3)

        # Action buttons
        button_frame = Frame(billMenuFrame, bg="#1a1f3a")
        button_frame.pack(fill=X, padx=5, pady=5)

        btn_style = {"font": ("Consolas", 11, "bold"), "cursor": "hand2", 
                     "bd": 0, "fg": "white", "pady": 8}

        Button(button_frame, text="GENERATE BILL", command=self.generate_bill,
               bg="#2196f3", width=13, **btn_style).pack(side=LEFT, padx=3)
        
        Button(button_frame, text="PRINT", command=self.print_bill,
               bg="#4caf50", width=13, **btn_style).pack(side=LEFT, padx=3)
        
        Button(button_frame, text="CLEAR ALL", command=self.clear_all,
               bg="#f44336", width=13, **btn_style).pack(side=LEFT, padx=3)

        self.update_date_time()

#---------------------- All functions ------------------------------
    def get_input(self, num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        try:
            result=self.var_cal_input.get()
            self.var_cal_input.set(eval(result))
        except:
            messagebox.showerror("Error", "Invalid calculation", parent=self.root)
            self.var_cal_input.set('')

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error", "Search input required", parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%' and status='Active'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        if row:
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.lbl_inStock.config(text=f"In Stock: {str(row[3])}")
            self.var_stock.set(row[3])
            self.var_qty.set('1')
    
    def get_data_cart(self, ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']
        if row:
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.var_qty.set(row[3])
            self.lbl_inStock.config(text=f"In Stock: {str(row[4])}")
            self.var_stock.set(row[4])
        
    def add_update_cart(self):
        if self.var_pid.get()=="":
            messagebox.showerror("Error", "Please select product from list", parent=self.root)
        elif self.var_qty.get()=="":
            messagebox.showerror("Error", "Quantity is required", parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror("Error", "Insufficient stock", parent=self.root)
        else:
            price_cal=self.var_price.get()
            cart_data=[self.var_pid.get(), self.var_pname.get(), price_cal,
                      self.var_qty.get(), self.var_stock.get()]
            
            present="no"
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present="yes"
                    break
                index_+=1
                
            if present=="yes":
                op=messagebox.askyesno("Confirm", 
                    "Product already in cart\nUpdate or Remove?", parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        self.cart_list[index_][3]=self.var_qty.get()
            else:
                self.cart_list.append(cart_data)
                
            self.show_cart()
            self.bill_update()

    def bill_update(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f"Bill Amount\n₹ {str(round(self.bill_amnt, 2))}")
        self.lbl_discount.config(text=f"Discount (5%)\n₹ {str(round(self.discount, 2))}")
        self.lbl_net_pay.config(text=f"Net Pay\n₹ {str(round(self.net_pay, 2))}")
        self.cartTitle.config(text=f"» CART [{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def generate_bill(self):
        if self.var_cname.get()=="" or self.var_contact.get()=="":
            messagebox.showerror("Error", "Customer details required", parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error", "Please add products to cart", parent=self.root)
        else:
            self.bill_top()
            self.bill_middle()
            self.bill_bottom()

            fp=open(f'Inventory-Management-System/bill/{str(self.invoice)}.txt', 'w')
            fp.write(self.txt_bill_area.get('1.0', END))
            fp.close()
            messagebox.showinfo("Success", f"Bill #{self.invoice} generated successfully!", 
                              parent=self.root)
            self.chk_print=1

    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
{'='*50}
          IMS - INVENTORY MANAGEMENT SYSTEM
{'='*50}
 Invoice No: {str(self.invoice)}
 Date: {str(time.strftime("%d/%m/%Y  %I:%M:%S %p"))}
{'='*50}
 Customer Name: {self.var_cname.get()}
 Contact: {self.var_contact.get()}
{'='*50}
 Product Name              Qty    Price
{'='*50}
'''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{'='*50}
 Bill Amount                      ₹ {round(self.bill_amnt, 2)}
 Discount (5%)                    ₹ {round(self.discount, 2)}
 Net Pay                          ₹ {round(self.net_pay, 2)}
{'='*50}
 Thank you for shopping with us!
 Support: keerthanapathipati236@gmail.com
{'='*50}
'''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def bill_middle(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status="Inactive"
                else:
                    status="Active"
                price=float(row[2])*int(row[3])
                price=str(round(price, 2))
                
                # Format product name to fit width
                name_display = name[:22].ljust(22)
                qty_display = str(row[3]).rjust(6)
                price_display = f"₹ {price}".rjust(10)
                
                self.txt_bill_area.insert(END, 
                    f"\n {name_display}{qty_display}{price_display}")
                
                # Update product quantity in database
                cur.execute("update product set qty=?, status=? where pid=?",
                           (qty, status, pid))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def clear_cart(self):
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.lbl_inStock.config(text="In Stock: -")
        self.var_stock.set("")

    def clear_all(self):
        del self.cart_list[:]
        self.clear_cart()
        self.show()
        self.show_cart()
        self.var_cname.set("")
        self.var_contact.set("")
        self.chk_print=0
        self.txt_bill_area.delete('1.0', END)
        self.cartTitle.config(text="» CART [0]")
        self.var_search.set("")
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        self.lbl_amnt.config(text="Bill Amount\n₹ 0")
        self.lbl_discount.config(text="Discount (5%)\n₹ 0")
        self.lbl_net_pay.config(text="Net Pay\n₹ 0")
        
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S %p")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"System Online • {date_} • {time_}")
        self.lbl_clock.after(200, self.update_date_time)

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo("Print", "Preparing to print...", parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file, 'w').write(self.txt_bill_area.get('1.0', END))
            os.startfile(new_file, 'print')
        else:
            messagebox.showwarning("Print", "Please generate bill first", parent=self.root)

if __name__=="__main__":
    root=Tk()
    obj=billClass(root)
    root.mainloop()