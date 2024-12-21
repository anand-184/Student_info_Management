
import os
os.environ['TCL_LIBRARY'] = r'C:\Users\Hp\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Hp\AppData\Local\Programs\Python\Python313\tcl\tk8.6'

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image,ImageTk
import sqlite3 as sql 

#Database created
con = sql.connect("Student.db")
cur=con.cursor()
#Table Created [B.Tech]
cur.execute('''CREATE TABLE IF NOT EXISTS [B.Tech]                    
(stu_id INTEGER PRIMARY KEY ,stu_name TEXT NOT NULL, stu_contact TEXT max(10) , stu_branch TEXT , stu_aggregate FLOAT)''')  
con.commit()
con.close()

tree =None

#function add_stuDB()
def add_stuDB(stu_name_entry, stu_contact_entry, stu_branch_entry, stu_aggregate_entry, stu_id_entry):
    stu_id = stu_id_entry.get().strip()
    stu_name = stu_name_entry.get().strip()
    stu_contact = stu_contact_entry.get().strip()
    stu_branch = stu_branch_entry.get().strip()
    stu_aggregate = stu_aggregate_entry.get().strip()

    if not (stu_name and stu_contact and stu_id):
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return

    con = sql.connect("Student.db")
    cur = con.cursor()

    # If student ID exists, update the student record
    cur.execute("SELECT * FROM [B.Tech] WHERE stu_id = ?", (stu_id,))
    existing_student = cur.fetchone()

    if existing_student:  # Update existing student
        cur.execute("""UPDATE [B.Tech] SET stu_name = ?, stu_contact = ?, stu_branch = ?, stu_aggregate = ?
                       WHERE stu_id = ?""", (stu_name, stu_contact, stu_branch, stu_aggregate, stu_id))
        messagebox.showinfo("Success", "Student updated successfully.")
    else:  # Add new student
        cur.execute("""INSERT INTO [B.Tech] (stu_id, stu_name, stu_contact, stu_branch, stu_aggregate)
                       VALUES (?, ?, ?, ?, ?)""", 
                       (stu_id, stu_name, stu_contact, stu_branch, stu_aggregate))
        messagebox.showinfo("Success", "Student added successfully.")

    con.commit()
    con.close()
        
    



def add_stu(stu_id =None,stu_name=None,stu_contact=None,stu_branch=None,stu_aggregate=None):
    add_stu_win = tk.Tk()
    add_stu_win.title('ADD Student ')
    add_stu_win.geometry('300x250')
    stu_label = tk.Label(add_stu_win,text="Student Name",font=("Times new Roman",12))
    stu_label.grid(row=0,column=0,pady=(5,5))
    stu_name_val = tk.Entry(add_stu_win,width=25,font=("Times New Roman",12))
    stu_name_val.grid(row=0,column=1,pady=(3,3))
    stu_contact_label= tk.Label(add_stu_win,text="Student Contact",font=("Times new Roman",12))
    stu_contact_label.grid(row=1,column=0,pady=(2,2))
    stu_contact= tk.Entry(add_stu_win,width=25,font=("Times new Roman",12))
    stu_contact.grid(row=1,column=1,pady=(2,2))
    stu_branch_label=tk.Label(add_stu_win,text="Student Branch",font=("Times new Roman",12))
    stu_branch_label.grid(row=2,column=0,pady=(2,2))
    stu_branch=tk.Entry(add_stu_win,width=25,font=("Times New Roman",12))
    stu_branch.grid(row=2,column=1,pady=(2,2),padx=(2,2))
    stu_aggregate_label=tk.Label(add_stu_win,text="Student Aggregate",font=("Times new Roman",12))
    stu_aggregate_label.grid(row=3,column=0,pady=(2,2))
    stu_aggregate=tk.Entry(add_stu_win,width=25,font=("Times New Roman",12))
    stu_aggregate.grid(row=3,column=1,pady=(2,2),padx=(2,2))

    stu_id_label=tk.Label(add_stu_win,text="Student Id",font=("Times new Roman",12))
    stu_id_label.grid(row=4,column=0,pady=(2,2))
    stu_id=tk.Entry(add_stu_win,width=25,font=("Times New Roman",12))
    stu_id.grid(row=4,column=1,pady=(2,2),padx=(2,2))
    
    

    if stu_name:
        stu_name_val.insert(0, stu_name)
    if stu_contact:
        stu_contact.insert(0, stu_contact)
    if stu_branch:
        stu_branch.insert(0, stu_branch)
    if stu_aggregate:
        stu_aggregate.insert(0, stu_aggregate)
    if stu_id:
        stu_id.insert(0,stu_id)    

    submit_button=tk.Button(add_stu_win,text="ADD",font=("Times new Roman",12),command=lambda:add_stuDB(stu_name_val,stu_contact,stu_branch,stu_aggregate,stu_id),fg="white",background="#90EE90")
    submit_button.grid(row=5,column=0,columnspan=2,pady=(10,5))
    add_stu_win.mainloop()

def delete_stu()  :
    selected_item = tree.selection() 
    if not selected_item:
        messagebox.showwarning("Selection Error","Select the entry first to delete") 
    item_values= tree.item(selected_item)["values"]
    stu_id = item_values[0]
    confirm = messagebox.askyesno("Delete Record",f"Do you really want to delete the record of: {stu_id} ?")
    if confirm:
        con = sql.connect("Student.db")
        cur = con.cursor()
        cur.execute("DELETE FROM [B.tech] WHERE stu_id=?", (stu_id,))
        con.commit()
        con.close()

        tree.delete(selected_item)

def update_stu():
    selected_item = tree.selection()  # Get selected item in the Treeview
    if selected_item:
        item = tree.item(selected_item)
        stu_id = item['values'][0]
        stu_name = item['values'][1]
        stu_contact = item['values'][2]
        stu_branch = item['values'][3]
        stu_aggregate = item['values'][4]

    add_stu(stu_id,stu_name,stu_contact,stu_branch,stu_aggregate)
    updated_values = (stu_id, stu_name, stu_contact, stu_branch, stu_aggregate)
    tree.item(selected_item, values=updated_values)
  


def view_data():
    con = sql.connect("Student.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM [B.Tech]")
    records = cur.fetchall()
    con.close()

    view_data_win = tk.Tk()
    view_data_win.title("Student List")
    view_data_win.geometry("600x400")

    style = ttk.Style()
    style.configure("Treeview", font=("Times New Roman", 14))
    style.configure("Treeview.Heading", font=("Times New Roman", 14, "bold"))

    global tree
    tree = ttk.Treeview(view_data_win, columns=("stu_id", "stu_name", "stu_contact", "stu_branch", "stu_aggregate"), show='headings')
    tree.heading("stu_id", text="Student ID")
    tree.heading("stu_name", text="Student Name")
    tree.heading("stu_contact", text="Contact")
    tree.heading("stu_branch", text="Branch")
    tree.heading("stu_aggregate", text="Aggregate")

    for stu in records:
        tree.insert("", tk.END, values=stu)

    tree.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    scrollbar = ttk.Scrollbar(view_data_win, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    delete_btn = tk.Button(view_data_win, text="Delete", command=delete_stu, font=("Times New Roman", 12), fg="white", background="#FF7F7F")
    delete_btn.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

    add_btn = tk.Button(view_data_win, text="ADD Student", command=add_stu, font=("Times New Roman", 12), fg="white", background="#90EE90")
    add_btn.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

    update_btn = tk.Button(view_data_win, text="Update", command=update_stu, font=("Times New Roman", 12), fg="white", background="sky blue")
    update_btn.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

    view_data_win.mainloop()
  



def view_stu(stu_id_entry, stu_name_entry):
    stu_id = stu_id_entry.get().strip()
    stu_name = stu_name_entry.get().strip()

    if not stu_id or not stu_name:  
        messagebox.showwarning("Input Error", "Please enter both Student ID and Student Name.")
        return

    con = sql.connect("Student.db")
    cur = con.cursor()

    cur.execute("SELECT * FROM [B.Tech] WHERE stu_id = ? AND stu_name = ?", (stu_id, stu_name))  
    student = cur.fetchone() 

    print("Fetched Student:", student)  

    con.commit()
    con.close()

    if student:
        view_stu_win = tk.Tk()
        view_stu_win.title("Student Details")
        view_stu_win.geometry("500x400")

        style = ttk.Style()
        style.configure("Treeview", font=("Times New Roman", 16))  
        style.configure("Treeview.Heading", font=("Times New Roman", 16, "bold")) 

        global tree 
        tree = ttk.Treeview(view_stu_win, columns=("stu_id", "stu_name", "stu_contact", "stu_branch", "stu_aggregate"), show='headings')

    
        tree.heading("stu_id", text="Student ID", anchor="w")
        tree.heading("stu_name", text="Student Name", anchor="w")
        tree.heading("stu_contact", text="Contact", anchor="w")
        tree.heading("stu_branch", text="Branch", anchor="w")
        tree.heading("stu_aggregate", text="Aggregate", anchor="w")

        tree.insert("", tk.END, values=student)

        tree.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        view_stu_win.grid_columnconfigure(0, weight=1)
        view_stu_win.grid_rowconfigure(0, weight=1)

        delete_btn = tk.Button(view_stu_win, text="Delete", command=delete_stu, font=("Times New Roman", 12), fg="white", background="#FF7F7F")
        delete_btn.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        
        update_btn = tk.Button(view_stu_win, text="Update", command=update_stu, font=("Times New Roman", 12), fg="white", background="sky blue")
        update_btn.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

        view_stu_win.grid_rowconfigure(1, weight=0)
    else:
        messagebox.showwarning("Error", "No student found with the provided ID and Name.")




def stu_main_win():
    stu_main_win= tk.Tk() 
    stu_main_win.title('STUDENT')
    stu_main_win.geometry('500x300')
    h1= tk.Label(stu_main_win,text="Student Credentials👨🏻‍🎓",font=("Times New Roman",20),fg="brown")
    h1.grid(row=0,column=2,pady=(5,1),sticky='ew')
    h2= tk.Label(stu_main_win,text="Read-> Learn-> Manage....",font=("Lucida handwriting",10))
    h2.grid(row=1,column=2,padx=(5,5),sticky='ew')
    stu_label = tk.Label(stu_main_win,text="Student ID",font=("Times New Roman",12))
    stu_label.grid(row=2,column=1,padx=(1,1),pady=(2,2))
    stu_id = tk.Entry(stu_main_win,width=30,font=("Times New Roman",12))
    stu_id.grid(row=2,column=2,padx=(1,1))
    name_label = tk.Label(stu_main_win,text="Student Name",font=("Times New Roman",12))
    name_label.grid(row=3,column=1,padx=(1,1),pady=(2,2))
    stu_val = tk.Entry(stu_main_win,width=30,font=("Times New Roman",12))
    stu_val.grid(row=3,column=2,padx=(1,1))
    search_btn= tk.Button(stu_main_win,text="Search",font=("Times New Roman",12),fg="brown",command=lambda:view_stu(stu_id,stu_val))
    search_btn.grid(row=4,column=2,pady=(5,5),padx=(2,2))
    stu_list_btn = tk.Button(stu_main_win,text="Student List 🧾",font=("Times new Roman",12),command=view_data,fg="brown")
    stu_list_btn.grid(row=4,column=3,pady=(4,4))
    add_stu_btn= tk.Button(stu_main_win,text="ADD Student 📖",font=("Times New Roman",12),command=add_stu,fg="brown")
    add_stu_btn.grid(row=5,column=3)
    stu_main_win.mainloop() 

def add_userDB(user_id_entry, user_name_entry, password_entry):
    user_id = user_id_entry.get().strip()
    user_name = user_name_entry.get().strip()
    user_password = password_entry.get().strip()

    if not user_id or not user_name or not user_password:
        messagebox.showerror("Input Error", "Please enter all details")
        return

    con = sql.connect("user.db")
    cur = con.cursor()
    
    cur.execute("SELECT * FROM USERS WHERE user_id = ?", (user_id,))
    existing_user = cur.fetchone()
    if existing_user:
        messagebox.showerror("Duplicate Error", "User ID already exists.")
        con.close()
        return

    cur.execute("""INSERT INTO USERS (user_id, user_name, password) values(?, ?, ?)""", 
                (user_id, user_name, user_password))
    con.commit()
    con.close()

    messagebox.showinfo("Success", "User added successfully")

    user_id_entry.delete(0, tk.END)
    user_name_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def add_user():
    add_user_win=tk.Tk()
    add_user_win.geometry("400x400")
    add_user_win.title("ADD USER")
    user_id_label = tk.Label(add_user_win,text="User ID ",font=("Times new Roman",12))
    user_id_label.grid(row=0,column=0,pady=(5,5))
    user_id_val = tk.Entry(add_user_win,width=25,font=("Times New Roman",12))
    user_id_val.grid(row=0,column=1,pady=(3,3))
    user_name_label= tk.Label(add_user_win,text="User Name",font=("Times new Roman",12))
    user_name_label.grid(row=1,column=0,pady=(2,2))
    user_name= tk.Entry(add_user_win,width=25,font=("Times new Roman",12))
    user_name.grid(row=1,column=1,pady=(2,2))
    password_label=tk.Label(add_user_win,text="Password",font=("Times new Roman",12))
    password_label.grid(row=2,column=0,pady=(2,2))
    password=tk.Entry(add_user_win,width=25,font=("Times New Roman",12))
    password.grid(row=2,column=1,pady=(2,2),padx=(2,2))

    submit_button=tk.Button(add_user_win,text="ADD",font=("Times new Roman",12),command=lambda:add_userDB(user_id_val,user_name,password),fg="white",background="#90EE90")
    submit_button.grid(row=4,column=0,columnspan=2,pady=(10,5))
    add_user_win.mainloop()
    
         
            

def goto_stu_main_win(user_id_entry, password_entry):
    user_id = user_id_entry.get().strip()
    user_password = password_entry.get().strip()

    if not user_id or not user_password:
        messagebox.showwarning("Input Error", "Please enter both user ID and password.")
        return


    con = sql.connect("user.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM USERS WHERE user_id = ? AND password = ?", (user_id, user_password))
    user = cur.fetchone()
    con.commit()  
    con.close()

    if user:  
        stu_main_win()
    else: 
        messagebox.showwarning("Error", "Invalid User ID or Password")
  



main_win=tk.Tk()
main_win.title("Log In")
main_win.geometry("500x500")
original_image1 = Image.open(r"C:\Users\Hp\OneDrive\Desktop\college mgmt.png")
resized_image1 = original_image1.resize((150, 150))
banner_img1 = ImageTk.PhotoImage(resized_image1)
image_label1 = tk.Label(main_win,image=banner_img1)
image_label1.grid(row=0,column=1)
image_label1=banner_img1
h1=tk.Label(main_win,text="User Id",font=("Times New Roman",16))
h1.grid(row=1,column=0,sticky="nsew",padx=(2,2),pady=(2,2))
user_id = tk.Entry(main_win,width=25,font=("Times New Roman",16))
user_id.grid(row=1,column=1,padx=(2,2),pady=(2,2))
h2=tk.Label(main_win,text="Password",font=("Times New Roman",16))
h2.grid(row=2,column=0,padx=(2,2),pady=(2,2))
password=tk.Entry(main_win,width=25,font=("Times New Roman",16))
password.grid(row=2,column=1,padx=(2,2),pady=(2,2))
add_user_btn=tk.Button(main_win,text="ADD USER",font=("times new roman",14,"bold"),background="brown",fg="white",command=add_user)
add_user_btn.grid(row=3,column=2,padx=(4,4),pady=(4,4))
user_list_btn=tk.Button(main_win,text="User List",font=("times new roman",14,"bold"),background="brown",fg="white")
user_list_btn.grid(row=4,column=2,padx=(4,4),pady=(4,4))
Log_in_btn=tk.Button(main_win,text="Log In",font=("times new roman",14,"bold"),command=lambda:goto_stu_main_win(user_id,password))
Log_in_btn.grid(row=4,column=1,padx=(4,4),pady=(4,4))

main_win.mainloop()



   

