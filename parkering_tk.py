import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import os

# Function to create the database and table
def create_db():
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                department TEXT,
                employee_number INT,
                car_reg1 TEXT,
                car_brand1 TEXT,
                car_reg2 TEXT,
                car_brand2 TEXT,
                user TEXT
                )""")
    conn.commit()
    conn.close()
create_db()
# Function to add an employee to the database
def add_employee():
    user = os.getlogin()
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute("INSERT INTO employees VALUES (:id, :first_name, :last_name, :department, :employee_number, :car_reg1, :car_brand1, :car_reg2, :car_brand2, :user)",
              {
                  'id': None,
                  'first_name': first_name_entry.get().title().strip(),
                  'last_name': last_name_entry.get().title().lstrip(),
                  'department': department_entry.get().capitalize().strip(),
                  'employee_number': employee_number_entry.get().strip(),
                  'car_reg1': car_reg1_entry.get().replace(' ', '').upper().strip(),
                  'car_brand1': car_brand1_entry.get().strip(),
                  'car_reg2': car_reg2_entry.get().replace(' ', '').upper().strip(),
                  'car_brand2': car_brand2_entry.get().strip(),
                  'user': user
              })
    if not validate_inputs():
        return
    conn.commit()
    conn.close()
    messagebox.showinfo("Info", "Ansatt er lagt til.")
    view_employees()

# Function to view all employees in the database
def view_employees():
    employees_list.delete(*employees_list.get_children())
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute("SELECT * FROM employees ORDER BY id DESC")
    rows = c.fetchall()
    for row in rows:
        employees_list.insert("", tk.END, values=row)
    conn.close()

# Function to clear the input fields
def clear_fields():
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    department_entry.delete(0, tk.END)
    employee_number_entry.delete(0, tk.END)
    car_reg1_entry.delete(0, tk.END)
    car_brand1_entry.delete(0, tk.END)
    car_reg2_entry.delete(0, tk.END)
    car_brand2_entry.delete(0, tk.END)

def validate_inputs():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    department = department_entry.get()
    employee_number = employee_number_entry.get()
    car_reg1 = car_reg1_entry.get()
    car_brand1 = car_brand1_entry.get()
    
    if not first_name or not last_name or not department or not employee_number or not car_reg1 or not car_brand1:
        messagebox.showerror("Error", "Alle feltene må fylles ut.")
        return False
    return True

def edit_validate_inputs(first_name_entry, last_name_entry, department_entry, employee_number_entry, car_reg1_entry, car_brand1_entry):
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    department = department_entry.get()
    employee_number = employee_number_entry.get()
    car_reg1 = car_reg1_entry.get()
    car_brand1 = car_brand1_entry.get()
    
    if not first_name or not last_name or not department or not employee_number or not car_reg1 or not car_brand1:
        messagebox.showerror("Error", "Alle feltene må fylles ut.")
        return False
    return True

# Function to edit an employee in the database
def edit_employee():
    selected_item = employees_list.selection()
    if not selected_item:
        messagebox.showerror("Error", "Ingen ansatt er valgt.")
        return
    employee = employees_list.item(selected_item)["values"]
    # Open a new window to edit the employee's information
    global edit_window
    edit_window = tk.Toplevel(root)
    edit_window.title("Rediger ansatt")
    edit_window.geometry("400x410")
    # Labels for the edit window
    id_label = tk.Label(edit_window, text="ID:")
    first_name_label = tk.Label(edit_window, text="Fornavn:")
    last_name_label = tk.Label(edit_window, text="Etternavn:")
    department_label = tk.Label(edit_window, text="Avdeling:")
    employee_number_label = tk.Label(edit_window, text="Ansattnummer:")
    car_reg1_label = tk.Label(edit_window, text="Bilreg 1:")
    car_brand1_label = tk.Label(edit_window, text="Bilmerke 1:")
    car_reg2_label = tk.Label(edit_window, text="Bilreg 2:")
    car_brand2_label = tk.Label(edit_window, text="Bilmerke 2:")

    # Entry fields for the edit window
    id_entry = tk.Entry(edit_window)
    id_entry.insert(0, employee[0])
    first_name_entry = tk.Entry(edit_window)
    first_name_entry.insert(0, employee[1])
    last_name_entry = tk.Entry(edit_window)
    last_name_entry.insert(0, employee[2])
    department_entry = tk.Entry(edit_window)
    department_entry.insert(0, employee[3])
    employee_number_entry = tk.Entry(edit_window)
    employee_number_entry.insert(0, employee[4])
    car_reg1_entry = tk.Entry(edit_window)
    car_reg1_entry.insert(0, employee[5])
    car_brand1_entry = tk.Entry(edit_window)
    car_brand1_entry.insert(0, employee[6])
    car_reg2_entry = tk.Entry(edit_window)
    car_reg2_entry.insert(0, employee[7])
    car_brand2_entry = tk.Entry(edit_window)
    car_brand2_entry.insert(0, employee[8])

    # Button to save the changes
    save_button = tk.Button(edit_window, text="Lagre", command=lambda: save_changes(selected_item, id_entry, first_name_entry, last_name_entry, department_entry, employee_number_entry, car_reg1_entry, car_brand1_entry, car_reg2_entry, car_brand2_entry))

    # Grid layout for the edit window
    id_label.grid(row=0, column=0, padx=10, pady=10)
    id_entry.grid(row=0, column=1, padx=10, pady=10)
    first_name_label.grid(row=1, column=0, padx=10, pady=10)
    first_name_entry.grid(row=1, column=1, padx=10, pady=10)
    last_name_label.grid(row=2, column=0, padx=10, pady=10)
    last_name_entry.grid(row=2, column=1, padx=10, pady=10)
    department_label.grid(row=3, column=0, padx=10, pady=10)
    department_entry.grid(row=3, column=1, padx=10, pady=10)
    employee_number_label.grid(row=4, column=0, padx=10, pady=10)
    employee_number_entry.grid(row=4, column=1, padx=10, pady=10)
    car_reg1_label.grid(row=5, column=0, padx=10, pady=10)
    car_reg1_entry.grid(row=5, column=1, padx=10, pady=10)
    car_brand1_label.grid(row=6, column=0, padx=10, pady=10)
    car_brand1_entry.grid(row=6, column=1, padx=10, pady=10)
    car_reg2_label.grid(row=7, column=0, padx=10, pady=10)
    car_reg2_entry.grid(row=7, column=1, padx=10, pady=10)
    car_brand2_label.grid(row=8, column=0, padx=10, pady=10)
    car_brand2_entry.grid(row=8, column=1, padx=10, pady=10)
    save_button.grid(row=9, column=1, padx=10, pady=0, sticky="e")
    delete_button = tk.Button(edit_window, text="Slett", command=delete_employee)
    delete_button.grid(row=9, column=1, padx=10, pady=0, sticky="w")

# Function to delete an employee from the database
def delete_employee():
    selected_item = employees_list.selection()
    if not selected_item:
        messagebox.showerror("Error", "Ingen ansatt er valgt.")
        return
    employee = employees_list.item(selected_item)["values"]
    confirm = messagebox.askyesno("Bekreftelse", "Er du sikker på at du vil slette denne ansatte?")
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute("DELETE FROM employees WHERE id=?", (employee[0],))
    conn.commit()
    conn.close()
    first_name = employee[1]
    last_name = employee[2]
    if confirm:
        employees_list.delete(selected_item)
        clear_fields()
        messagebox.showinfo("Info", f"{first_name} {last_name} er slettet.")
        edit_window.destroy()

def save_changes(selected_item, id_entry, first_name_entry, last_name_entry, department_entry, employee_number_entry, car_reg1_entry, car_brand1_entry, car_reg2_entry, car_brand2_entry):
    if messagebox.askyesno("Lagre endringer", "Vil du lagre endringene?"):
        if edit_validate_inputs(first_name_entry, last_name_entry, department_entry, employee_number_entry, car_reg1_entry, car_brand1_entry):
            conn = sqlite3.connect('employees.db')
            c = conn.cursor()
            c.execute("UPDATE employees SET first_name=?, last_name=?, department=?, employee_number=?, car_reg1=?, car_brand1=?, car_reg2=?, car_brand2=? WHERE id=?", (
                first_name_entry.get(),
                last_name_entry.get(),
                department_entry.get(),
                employee_number_entry.get(),
                car_reg1_entry.get(),
                car_brand1_entry.get(),
                car_reg2_entry.get(),
                car_brand2_entry.get(),
                id_entry.get()
            ))
            conn.commit()
            conn.close()
        else:
            return
        employees_list.item(selected_item, values=(
            id_entry.get(), 
            first_name_entry.get(), 
            last_name_entry.get(), 
            department_entry.get(), 
            employee_number_entry.get(), 
            car_reg1_entry.get(), 
            car_brand1_entry.get(),
            car_reg2_entry.get(), 
            car_brand2_entry.get()
        ))

        messagebox.showinfo("Info", "Ansatt er redigert.")
        edit_window.destroy()
    else:
        # Ikke lagre endringene
        pass

'''
def select_employee(event):
    cur_item = employees_list.focus()
    contents = [employees_list.item(cur_item, "values")]
    for row in contents:
        first_name_entry.delete(0, tk.END)
        first_name_entry.insert(0, row[0])
        last_name_entry.delete(0, tk.END)
        last_name_entry.insert(0, row[1])
        department_entry.delete(0, tk.END)
        department_entry.insert(0, row[2])
        employee_number_entry.delete(0, tk.END)
        employee_number_entry.insert(0, row[3])
        car_reg1_entry.delete(0, tk.END)
        car_reg1_entry.insert(0, row[4])
        car_brand1_entry.delete(0, tk.END)
        car_brand1_entry.insert(0, row[5])
        car_reg2_entry.delete(0, tk.END)
        car_reg2_entry.insert(0, row[6])
        car_brand2_entry.delete(0, tk.END)
        car_brand2_entry.insert(0, row[7])
'''

def load_data():
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees ORDER BY id DESC")
    data = cursor.fetchall()

    for row in data:
        employees_list.insert("", tk.END, values=row)

    conn.commit()
    conn.close()

def search_employees(*args):
    search_text = search_entry.get().strip()
    employees_list.delete(*employees_list.get_children())
    if not search_text:
        conn = sqlite3.connect('employees.db')
        c = conn.cursor()
        c.execute("SELECT * FROM employees WHERE first_name LIKE ? OR last_name LIKE ? OR department LIKE ? OR employee_number LIKE ? OR car_reg1 LIKE ? OR car_brand1 LIKE ? OR car_reg2 LIKE ? OR car_brand2 LIKE ? OR user LIKE ? ORDER BY id DESC", ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%',))
        rows = c.fetchall()
        for row in rows:
            employees_list.insert("", tk.END, values=row)
        conn.close()
    else:
        conn = sqlite3.connect('employees.db')
        c = conn.cursor()
        c.execute("SELECT * FROM employees WHERE first_name LIKE ? OR last_name LIKE ? OR department LIKE ? OR employee_number LIKE ? OR car_reg1 LIKE ? OR car_brand1 LIKE ? OR car_reg2 LIKE ? OR car_brand2 LIKE ? OR user LIKE ? ORDER BY id DESC", ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%',))
        rows = c.fetchall()
        for row in rows:
            employees_list.insert("", tk.END, values=row)
        conn.close()

def sort_treeview_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(key=lambda t: t[0], reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: sort_treeview_column(tv, col, not reverse))
    
# Create the main window
root = tk.Tk()
root.title("Parkeringsregister")

# Create the input fields
first_name_label = tk.Label(root, text="Fornavn:")
first_name_label.grid(row=1, column=0, padx=10, pady=10)
first_name_entry = tk.Entry(root)
first_name_entry.grid(row=1, column=1, padx=10, pady=10)

last_name_label = tk.Label(root, text="Etternavn:")
last_name_label.grid(row=2, column=0, padx=10, pady=10)
last_name_entry = tk.Entry(root)
last_name_entry.grid(row=2, column=1, padx=10, pady=10)

department_label = tk.Label(root, text="Avdeling:")
department_label.grid(row=3, column=0, padx=10, pady=10)
department_entry = tk.Entry(root)
department_entry.grid(row=3, column=1, padx=10, pady=10)

employee_number_label = tk.Label(root, text="Ansattnummer:")
employee_number_label.grid(row=4, column=0, padx=10, pady=10)
employee_number_entry = tk.Entry(root)
employee_number_entry.grid(row=4, column=1, padx=10, pady=10)

car_reg1_label = tk.Label(root, text="Bilreg 1:")
car_reg1_label.grid(row=5, column=0, padx=10, pady=10)
car_reg1_entry = tk.Entry(root)
car_reg1_entry.grid(row=5, column=1, padx=10, pady=10)

car_brand1_label = tk.Label(root, text="Bilmerke 1:")
car_brand1_label.grid(row=6, column=0, padx=10, pady=10)
car_brand1_entry = tk.Entry(root)
car_brand1_entry.grid(row=6, column=1, padx=10, pady=10)

car_reg2_label = tk.Label(root, text="Bilreg 2:")
car_reg2_label.grid(row=7, column=0, padx=10, pady=10)
car_reg2_entry = tk.Entry(root)
car_reg2_entry.grid(row=7, column=1, padx=10, pady=10)

car_brand2_label = tk.Label(root, text="Bilmerke 2:")
car_brand2_label.grid(row=8, column=0, padx=10, pady=10)
car_brand2_entry = tk.Entry(root)
car_brand2_entry.grid(row=8, column=1, padx=10, pady=10)

# Create the submit button
submit_button = tk.Button(root, text="Legg til", command=add_employee)
submit_button.grid(row=9, column=0, padx=10, pady=10)

# Create the update button
update_button = tk.Button(root, text="Oppdater ansatt", command=edit_employee)
update_button.grid(row=9, column=2, padx=10, pady=10)

# Create the clear button
clear_button = tk.Button(root, text="Tøm feltene", command=clear_fields)
clear_button.grid(row=9, column=1, padx=10, pady=10, sticky="w")

# Create the list of employees
employees_list = ttk.Treeview(root, columns=("id", "first_name", "last_name", "department", "employee_number", "car_reg1", "car_brand1", "car_reg2", "car_brand2", "user"), height=20, selectmode="extended", show="headings")
employees_list.grid(row=1, column=2, rowspan=8, padx=10, pady=10, sticky="nsew")


# Set up the columns for the list of employees
employees_list.heading("id", text="ID", anchor=tk.W)
employees_list.column("id", stretch=tk.NO, width=40, anchor=tk.W)
employees_list.heading("first_name", text="Fornavn", anchor=tk.W, command=lambda: sort_treeview_column(employees_list, "first_name", False))
employees_list.column("first_name", stretch=tk.NO, width=120, anchor=tk.W)
employees_list.heading("last_name", text="Etternavn", anchor=tk.W, command=lambda: sort_treeview_column(employees_list, "last_name", False))
employees_list.column("last_name", stretch=tk.NO, width=120, anchor=tk.W)
employees_list.heading("department", text="Avdeling", anchor=tk.W, command=lambda: sort_treeview_column(employees_list, "department", False))
employees_list.column("department", stretch=tk.NO, width=100, anchor=tk.W)
employees_list.heading("employee_number", text="Ansattnummer", anchor=tk.W, command=lambda: sort_treeview_column(employees_list, "employee_number", False))
employees_list.column("employee_number", stretch=tk.NO, width=100, anchor=tk.W)
employees_list.heading("car_reg1", text="Bilreg 1", anchor=tk.W, command=lambda: sort_treeview_column(employees_list, "car_reg1", False))
employees_list.column("car_reg1", stretch=tk.NO, width=100, anchor=tk.W)
employees_list.heading("car_brand1", text="Bilmerke 1", anchor=tk.W, command=lambda: sort_treeview_column(employees_list, "car_brand1", False))
employees_list.column("car_brand1", stretch=tk.NO, width=100, anchor=tk.W)
employees_list.heading("car_reg2", text="Bilreg 2", anchor=tk.W, command=lambda: sort_treeview_column(employees_list, "car_reg2", False))
employees_list.column("car_reg2", stretch=tk.NO, width=100, anchor=tk.W)
employees_list.heading("car_brand2", text="Bilmerke 2", anchor=tk.W, command=lambda: sort_treeview_column(employees_list, "car_brand2", False))
employees_list.column("car_brand2", stretch=tk.NO, width=100, anchor=tk.W)
employees_list.heading("user", text="Lagt inn av", anchor=tk.W, command=lambda: sort_treeview_column(employees_list, "user", False))
employees_list.column("user", stretch=tk.NO, width=100, anchor=tk.W)

# Create the scrollbar
scrollbar = tk.Scrollbar(root)
scrollbar.grid(row=0, column=3, rowspan=8, sticky="ns")

# Attach the scrollbar to the list of employees
employees_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=employees_list.yview)

# Bind the double click event to the employees_list
#employees_list.bind("<Double-1>", command=edit_employee)

# Load the data from the database
load_data()

#search_button = tk.Button(root, text="Søk", command=search_employees)
#search_button.grid(row=0, column=3, padx=5)

search_entry = tk.Entry(root)
search_entry_label = tk.Label(root, text="Søk i databasen:")
search_entry_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")
search_entry.grid(row=0, column=2, padx=110, pady=10, sticky="w")
search_entry.bind("<KeyRelease>", search_employees)

root.mainloop()

