import random
import sqlite3
import tkinter
from tkinter import *
from tkinter import messagebox

root = tkinter.Tk()
top = tkinter.Toplevel()


username = StringVar()
password = StringVar()


with sqlite3.connect("todoList.db") as db:
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS user(username TEXT NOT NULL, password TEXT NOT NULL)")
    cursor.execute("SELECT * FROM user")
    db.commit()

entry_username = Entry(top, text="")
entry_password = Entry(top, text="")


def login():
    find_user = "SELECT * FROM user WHERE username = ? AND password = ?"
    cursor.execute(find_user, [(entry_username.get()), (entry_password.get())])
    results = cursor.fetchall()
    if results:
        root.deiconify()
        top.destroy()
    else:
        messagebox.showerror("Username doesn't exist", "Username error")


def signup():
    find_user = "SELECT * FROM user WHERE username = ?"
    cursor.execute(find_user, [(entry_username.get())])
    if cursor.fetchall():
        messagebox.showerror("Username already exits", "user name taken")

    else:
        messagebox.showinfo("Success", "Account Created")
    insert = '''INSERT INTO user(username,password) VALUES(?,?)'''
    cursor.execute(insert, (entry_username.get(), entry_password.get()))
    db.commit()


button_login = Button(top, text="Login", command=login)
button_signup = Button(top, text="SignUp", command=signup)


root.configure(bg='white')
root.title('TODO LIST')
root.geometry('350x230')
top.title('Login')
top.geometry('350x230')

tasks = ["Use add to Add new task", "Delete completed/unnecessary task", "Enjoy"]


def update_listbox():
    clear_listbox()
    for task in tasks:
        lb_tasks.insert("end", task)


def clear_listbox():
    lb_tasks.delete(0, "end")


def add_task():
    new_task = text_input.get()
    if new_task != "":
        tasks.append(new_task)
        update_listbox()
        text_input.delete(0, "end")
        lbl_display["text"] = "Task added: %s" % new_task
    else:
        lbl_display["text"] = "Blank Task??"


def delete_all():
    confirm = messagebox.askyesnocancel("Delete All Task?", "Confirm to delete all tasks?")
    if confirm:
        lbl_display["text"] = "All Task Deleted"
        global tasks
        tasks = []
        update_listbox()


def delete_single():
    task_selected = lb_tasks.get("active")
    if task_selected in tasks:
        tasks.remove(task_selected)
    update_listbox()
    lbl_display["text"] = "Task Deleted: %s" % task_selected


def sort_asc():
    tasks.sort()
    update_listbox()
    lbl_display["text"] = "Task order in ascending"


def sort_desc():
    tasks.sort()
    tasks.reverse()
    update_listbox()
    lbl_display["text"] = "Task order in descending"


def random_choose():
    lbl_display["text"] = ""
    task = random.choice(tasks)
    lbl_display["text"] = task


def pending_task():
    number_task = len(tasks)
    message = "Task Pending are: %s" % number_task
    lbl_display["text"] = message


def exit_app():
    lbl_display["text"] = ""
    confirm = messagebox.askyesno("EXIT", "Confirm to close?")
    if confirm:
        exit()


lbl_title = tkinter.Label(root, text="LIST", bg="white")
lbl_title.grid(row=0, column=0)

lbl_display = tkinter.Label(root, text="", bg="white")
lbl_display.grid(row=1, column=0)

text_input = tkinter.Entry(root, width=30)
text_input.grid(row=2, column=0)

add_task_button = tkinter.Button(root, width="12", text="Add New Task", fg="green", bg="white", command=add_task)
add_task_button.grid(row=1, column=1)

delete_all_button = tkinter.Button(root, width="12", text="Delete All Task", fg="red", bg="white", command=delete_all)
delete_all_button.grid(row=2, column=1)

delete_single_button = tkinter.Button(root, width="12", text="Delete", fg="red", bg="white", command=delete_single)
delete_single_button.grid(row=3, column=1)

sort_asc_button = tkinter.Button(root, text="Sort Asc", fg="blue", bg="white", width="12", command=sort_asc)
sort_asc_button.grid(row=4, column=1)

sort_desc_button = tkinter.Button(root, text="Sort Desc", fg="blue", bg="white", width="12", command=sort_desc)
sort_desc_button.grid(row=5, column=1)

random_button = tkinter.Button(root, text="Random Task", fg="green", width="12", bg="white", command=random_choose)
random_button.grid(row=6, column=1)

number_task__button = tkinter.Button(root, text="Pending Task", fg="blue", width="12", bg="white", command=pending_task)
number_task__button.grid(row=7, column=1)

exit_button = tkinter.Button(root, text="Exit", fg="red", bg="white", width="12", command=exit_app)
exit_button.grid(row=8, column=1)

lb_tasks = tkinter.Listbox(root, width=40)
lb_tasks.grid(row=3, column=0, rowspan=100)

icon = tkinter.PhotoImage(file='icon.png')
root.tk.call('wm', 'iconphoto', root._w, icon)
top.tk.call('wm','iconphoto', root._w, icon)

entry_username.pack()
entry_password.pack()
button_login.pack()
button_signup.pack()


root.withdraw()
root.mainloop()
