import csv
import traceback
import assignment2 as a2
import os
import custom_module

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

    # Get the index for the ID so we can use it as the key
    id_idx = column_index("employee_id")

    # loop through every row in the global employees["rows"]
    for row in employees["rows"]:
        # get the ID to use as the key
        employee_id = row[id_idx]

        # now I can use the function from task 8 to get the data dictionary (without the ID) for this employee
        employee_data = employee_dict(row)

        # now assign the data to the ID key
        all_employees[employee_id] = employee_data
       

    return all_employees

# Call the function and print the final result
all_employees = all_employees_dict()
print(all_employees)
    


# Task 10: Use the os Module
def get_this_value():
    return os.getenv("THISVALUE")


# Task 11: Creating Your Own Module
def set_that_secret(new_secret):
   custom_module.set_secret(new_secret)


set_that_secret("kibreab is the best!")

#print out custom_module.secret
print(custom_module.secret)



# Task 12: Read minutes1.csv and minutes2.csv
def read_minutes():
    #minutes1 = dict()
    #minutes2 = dict()
    minutes1 = {"fields": [], "rows": []}
    minutes2 = {"fields": [], "rows": []}

    minutes1_path = "../csv/minutes1.csv"
    minutes2_path = "../csv/minutes2.csv"

    # read minutes1.csv
    try:
        with open(minutes1_path, "r") as csvfile:
            reader = csv.reader(csvfile)
            for index, row in enumerate(reader):
                if index == 0:
                    minutes1["fields"] = row
                else:
                    minutes1["rows"].append(tuple(row))
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

    # read minutes2.csv
    try:    
        with open(minutes2_path, "r") as csvfile:
            reader = csv.reader(csvfile)
            for index, row in enumerate(reader):
                if index == 0:
                    minutes2["fields"] = row
                else:
                    minutes2["rows"].append(tuple(row))
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

    return minutes1, minutes2

minutes1, minutes2 = read_minutes()

# print the dicts
print(minutes1)
print(minutes2)


# Task 13: Create minutes_set
def create_minutes_set():
    # convert the lists of tuples into sets
    minutes1_set = set(minutes1["rows"])
    minutes2_set = set(minutes2["rows"])

    # combine the sets using set union
    minutes_set = minutes1_set.union(minutes2_set)

    return minutes_set


# Store the result in the global variable minutes_set
minutes_set = create_minutes_set()


# Task 14: Convert to datetime
from datetime import datetime
def create_minutes_list():
   
    # conver the set to list
    temp_list = list(minutes_set)

    # I will use map() with lambda to transform each row
    mapped_list = map(lambda row: (row[0], datetime.strptime(row[1], "%B %d, %Y")), temp_list)

    # convert the map object back to a list and return it
    return list(mapped_list)

minutes_list = create_minutes_list()

print(minutes_list)

# Task 15: Write Out Sorted List
def write_sorted_list():
    minutes_list.sort(key=lambda row: row[1]) # sort by the datetime, which is the second item in the tuple

    # Convert datetime objects back to strings using strftime
    formatted_list = list(map(lambda row: (row[0], row[1].strftime("%B %d, %Y")), minutes_list))

    # Write to the new CSV file
    try:
        with open("./minutes.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(minutes1["fields"]) # write the header
            writer.writerows(formatted_list) # write the sorted rows
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


    # Return the converted list
    return formatted_list

sorted_minutes = write_sorted_list()