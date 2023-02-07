import sqlite3
import random
import names

# Opprett en database-tilkobling
conn = sqlite3.connect('employees.db')
c = conn.cursor()

# Opprett en tabell
c.execute('''CREATE TABLE employees (id INTEGER PRIMARY KEY, 
                                      first_name TEXT, 
                                      last_name TEXT, 
                                      department TEXT, 
                                      employee_number INTEGER, 
                                      car_reg1 TEXT, 
                                      car_brand1 TEXT, 
                                      car_reg2 TEXT, 
                                      car_brand2 TEXT)''')

# Generer 1000 ansatte og legg dem inn i databasen
for i in range(1000):
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    department = random.choice(['Sales', 'Marketing', 'IT', 'Finance', 'HR'])
    employee_number = i + 1
    car_reg1 = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6)])
    car_brand1 = random.choice(['Toyota', 'BMW', 'Mercedes', 'Audi', 'Volvo'])
    car_reg2 = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6)])
    car_brand2 = random.choice(['Toyota', 'BMW', 'Mercedes', 'Audi', 'Volvo'])

    c.execute("INSERT INTO employees (first_name, last_name, department, employee_number, car_reg1, car_brand1, car_reg2, car_brand2) VALUES (?,?,?,?,?,?,?,?)",
              (first_name, last_name, department, employee_number, car_reg1, car_brand1, car_reg2, car_brand2))

# Lagre endringene og lukk tilkoblingen
conn.commit()
conn.close()
