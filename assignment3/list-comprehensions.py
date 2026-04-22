import csv

# task 3 List Comprehensions Practice

# read the contents of the employees.csv file into a list of lists
with open("../csv/employees.csv", "r") as file:
    reader = csv.reader(file)
    lines = list(reader)


# list comprehension to create a list of employee names
full_names = [f"{row[1]} {row[2]}" for row in lines[1:]]  # skip the header row
print("All Employee Names:")
print(full_names)

# List comprehension for names containing the letter "e"
full_names_2 = [full_name2 for full_name2 in full_names if "e" in full_name2.lower()]
print("\nNames containing the letter 'e':")
print(full_names_2)
