from tkinter import *
from tkinter import ttk
import pymysql
from tkinter import messagebox

class Student:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System - UEM, Jaipur")

        # Fullscreen window setup
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.configure(bg="#1E1E2F")

        # Styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox",
                        fieldbackground="#2D2F3A",
                        background="#2D2F3A",
                        foreground="white",
                        font=("Helvetica", 12))

        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="white",
                        font=("Helvetica", 11))

        style.map("Treeview",
                  background=[('selected', '#F9AA33')],
                  foreground=[('selected', 'black')])

        style.configure("Treeview.Heading",
                        background="#F9AA33",
                        foreground="black",
                        font=("Helvetica", 12, "bold"))

        # Title
        title = Label(self.root, text="UEM Jaipur | Student Management System", font=("Helvetica", 32, "bold"),
                      bg="#2D2F3A", fg="#F9AA33", pady=20)
        title.pack(fill=X)

        # Variables
        self.Branch_var = StringVar()
        self.Semester_var = StringVar()
        self.Roll_No_var = StringVar()
        self.Name_var = StringVar()
        self.Contact_var = StringVar()
        self.D_O_B_var = StringVar()
        self.E_mail_var = StringVar()
        self.Mid_term_1_var = StringVar()
        self.Mid_term_2_var = StringVar()
        self.End_term_var = StringVar()
        self.Search_by = StringVar()
        self.Search_txt = StringVar()

        # Manage Frame
        Manage_Frame = Frame(self.root, bg="#393E46", bd=5)
        Manage_Frame.place(x=30, y=120, width=520, height=800)

        m_title = Label(Manage_Frame, text="Student Details", bg="#393E46", fg="white",
                        font=("Helvetica", 22, "bold"))
        m_title.grid(row=0, columnspan=2, pady=20)

        fields = [
            ("Branch", self.Branch_var, ("B.Tech", "M.Tech", "BCA", "MCA", "MBA", "BPT")),
            ("Semester", self.Semester_var, ("1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th")),
            ("Roll No.", self.Roll_No_var),
            ("Name", self.Name_var),
            ("Contact", self.Contact_var),
            ("D.O.B", self.D_O_B_var),
            ("E.mail", self.E_mail_var),
            ("Mid-term 1", self.Mid_term_1_var),
            ("Mid-term 2", self.Mid_term_2_var),
            ("End-term", self.End_term_var),
        ]

        for i, (label_text, var, *extra) in enumerate(fields):
            Label(Manage_Frame, text=label_text, bg="#393E46", fg="white", font=("Helvetica", 13, "bold"))\
                .grid(row=i+1, column=0, pady=10, padx=10, sticky="w")

            if extra:
                combo = ttk.Combobox(Manage_Frame, textvariable=var, font=("Helvetica", 12), state="readonly", width=25)
                combo["values"] = extra[0]
                combo.grid(row=i+1, column=1, pady=10, padx=10, sticky="w")
            else:
                Entry(Manage_Frame, textvariable=var, font=("Helvetica", 12), bd=3, relief=GROOVE, width=28).grid(row=i+1, column=1, pady=10, padx=10, sticky="w")

        # Buttons
        btn_Frame = Frame(Manage_Frame, bg="#393E46")
        btn_Frame.place(x=50, y=550, width=400)

        buttons = [
            ("Add", self.add_students),
            ("Update", self.update_data),
            ("Delete", self.delete_data),
            ("Clear", self.clear)
        ]

        for i, (text, cmd) in enumerate(buttons):
            Button(btn_Frame, text=text, width=15, command=cmd, bg="#F9AA33", fg="black", font=("Helvetica", 12, "bold"))\
                .grid(row=i//2, column=i%2, padx=10, pady=10)

        # Detail Frame
        Detail_Frame = Frame(self.root, bd=5, bg="#393E46")
        Detail_Frame.place(x=580, y=120, width=1320, height=800)

        lbl_search = Label(Detail_Frame, text="Search By", bg="#393E46", fg="white", font=("Helvetica", 14, "bold"))
        lbl_search.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        combo_search = ttk.Combobox(Detail_Frame, textvariable=self.Search_by, font=("Helvetica", 13), state="readonly", width=15)
        combo_search["values"] = ("Branch", "Semester", "Roll_No", "Name", "Contact")
        combo_search.grid(row=0, column=1, padx=10, pady=10)

        txt_search = Entry(Detail_Frame, textvariable=self.Search_txt, font=("Helvetica", 13), bd=3, relief=GROOVE, width=25)
        txt_search.grid(row=0, column=2, padx=10, pady=10)

        Button(Detail_Frame, text="Search", command=self.Search_data, width=12, bg="#F9AA33", fg="black", font=("Helvetica", 12, "bold")).grid(row=0, column=3, padx=10)
        Button(Detail_Frame, text="Show All", command=self.fetch_data, width=12, bg="#F9AA33", fg="black", font=("Helvetica", 12, "bold")).grid(row=0, column=4, padx=10)

        # Table Frame
        Table_Frame = Frame(Detail_Frame, bd=4, relief=RIDGE, bg="white")
        Table_Frame.place(x=10, y=60, width=900, height=600)

        scroll_x = Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_Frame, orient=VERTICAL)
        self.Student_table = ttk.Treeview(Table_Frame, columns=("Branch", "Semester", "Roll No.", "Name", "Contact", "D.O.B", "E.mail", "Mid-term-1", "Mid-term-2", "End-term"),
                                          xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Student_table.xview)
        scroll_y.config(command=self.Student_table.yview)

        for col in self.Student_table["columns"]:
            self.Student_table.heading(col, text=col)

        self.Student_table['show'] = 'headings'
        self.Student_table.pack(fill=BOTH, expand=1)
        self.Student_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()

    # Backend Functions (add_students, fetch_data, clear, get_cursor, update_data, delete_data, Search_data)
    # [Same as in your original code, include below this point...]
       
    # ========== Function Definitions Below ===========

    def add_students(self):
        if self.Roll_No_var.get() == "" or self.Name_var.get() == "":
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="stm")
            cur = con.cursor()
            cur.execute("INSERT INTO student VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                self.Branch_var.get(),
                self.Semester_var.get(),
                self.Roll_No_var.get(),
                self.Name_var.get(),
                self.Contact_var.get(),
                self.D_O_B_var.get(),
                self.E_mail_var.get(),
                self.Mid_term_1_var.get(),
                self.Mid_term_2_var.get(),
                self.End_term_var.get()
            ))
            con.commit()
            con.close()
            self.fetch_data()
            self.clear()
            messagebox.showinfo("Success", "Record added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}")

    def fetch_data(self):
        con = pymysql.connect(host="localhost", user="root", passwd="", database="stm")
        cur = con.cursor()
        cur.execute("select * from student")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.Student_table.delete(*self.Student_table.get_children())
            for row in rows:
                self.Student_table.insert('', END, values=row)
            con.commit()
        con.close()

    def clear(self):
        self.Branch_var.set("")
        self.Semester_var.set("")
        self.Roll_No_var.set("")
        self.Name_var.set("")
        self.Contact_var.set("")
        self.D_O_B_var.set("")
        self.E_mail_var.set("")
        self.Mid_term_1_var.set("")
        self.Mid_term_2_var.set("")
        self.End_term_var.set("")

    def get_cursor(self, ev):
        cursor_row = self.Student_table.focus()
        contents = self.Student_table.item(cursor_row)
        row = contents["values"]
        self.Branch_var.set(row[0])
        self.Semester_var.set(row[1])
        self.Roll_No_var.set(row[2])
        self.Name_var.set(row[3])
        self.Contact_var.set(row[4])
        self.D_O_B_var.set(row[5])
        self.E_mail_var.set(row[6])
        self.Mid_term_1_var.set(row[7])
        self.Mid_term_2_var.set(row[8])
        self.End_term_var.set(row[9])

    def update_data(self):
        con = pymysql.connect(host="localhost", user="root", password="", database="stm")
        cur = con.cursor()
        cur.execute("update student set Branch=%s,Semester=%s,Name=%s,Contact=%s,DOB=%s,E_Mail=%s,Mid_term_1=%s,Mid_term_2=%s,End_term=%s where Roll_No=%s", (
            self.Branch_var.get(),
            self.Semester_var.get(),
            self.Name_var.get(),
            self.Contact_var.get(),
            self.D_O_B_var.get(),
            self.E_mail_var.get(),
            self.Mid_term_1_var.get(),
            self.Mid_term_2_var.get(),
            self.End_term_var.get(),
            self.Roll_No_var.get()
        ))
        con.commit()
        self.fetch_data()
        self.clear()
        con.close()

    def delete_data(self):
        con = pymysql.connect(host="localhost", user="root", database="stm")
        cur = con.cursor()
        cur.execute("delete from student where Roll_No=%s", self.Roll_No_var.get())
        con.commit()
        con.close()
        self.fetch_data()
        self.clear()

    def Search_data(self):
        con = pymysql.connect(host="localhost", user="root", database="stm")
        cur = con.cursor()
        cur.execute("select * from student where "+str(self.Search_by.get())+" LIKE '%"+str(self.Search_txt.get())+"%'")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.Student_table.delete(*self.Student_table.get_children())
            for row in rows:
                self.Student_table.insert('', END, values=row)
            con.commit()
        con.close()


root = Tk()
root.state('zoomed')
ob = Student(root)
root.mainloop()







