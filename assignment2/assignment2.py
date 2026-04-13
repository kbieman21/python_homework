import csv
import traceback
import assignment2 as a2

# Task 2: Read a CSV File
def read_employees():
    # declare an empty dictionary to store employee data and an empty list to store the dictionaries
    employee_dict={}
    list_row = []
    try:
        with open("../csv/employees.csv", "r") as csvfile:
                reader = csv.reader(csvfile)

                for index, row in enumerate(reader):
                    if index == 0:
                        # store the first row as a list to use as keys for the dictionaries
                        employee_dict["fields"] = row
                    else:
                        # Add all susbsequent rows to the list rows
                        list_row.append(row)

                    # add the list of lists to the employee_dict
                employee_dict["rows"] = list_row

                return employee_dict
                
    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}") 


# call the function and store in the global variable employee
employees = read_employees()

# print to verify the function works
print(employees)


# Task 3: Find the Column Index
def column_index(column_name):
   
   return employees["fields"].index(column_name)

# call the function for "employee_id" and store in the global variable employee
employee_id_column = column_index("employee_id")

# print to verify the function works
print("The index for employee_id is : " + str(employee_id_column))
 

# Task 4: Find the Employee First Name
def first_name(row_number):
    # find which column index belongs to 'first_name'
    col_index = column_index("first_name")
    return employees["rows"][row_number][col_index]



# Task 5: Find the Employee: a Function in a Function
def employee_find(employee_id):
    # filter the rows
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id
    # filter() applies employee_match to every row in the employees["rows"] list
    # We wrap it in list() to convert the filter object back into a list of matches
    matches = list(filter(employee_match, employees["rows"]))
    
    return matches


# Task 6: Find the Employee with a Lambda
def employee_find_2(employee_id):
    matches = list(filter(lambda row: int(row[employee_id_column]) == employee_id, employees["rows"]))
    return matches

    

# Task 7: Sort the Rows by last_name Using a Lambda
def sort_by_last_name():
    # find the column index for last_name
    last_name_index = column_index("last_name")
    # Sort the rows in place using a lambda as the key
    # 'row' is passed into the lambda, and we return the item at last_name_index
    employees["rows"].sort(key=lambda row: row[last_name_index])

    # return the sorted rows
    return employees["rows"]


sort_by_last_name()

print(employees)


# Task 8: Create a dict for an Employee
def employee_dict(row):
    # use zip to pair field header with the row data
    employee_data = dict(zip(employees["fields"], row))

    # Remove the employee_id key as requested
    if "employee_id" in employee_data:
        del employee_data["employee_id"]

    return employee_data


# Task 9: A dict of dicts, for All Employees
def all_employees_dict():
    # create an empty dictionary to store the employee dicts
    all_employees = {}

    for row in employees["rows"]:
        # use the employee_id as the key and the employee_dict as the value
        all_employees[row[employee_id_column]] = employee_dict(row)

    return all_employees
    
