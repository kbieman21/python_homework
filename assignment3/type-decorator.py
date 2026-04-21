# Task 2 A Decorator that Takes an Argument

def type_converter(type_of_output):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # execute the function and capture the result
            result = func(*args, **kwargs)
            # convert and return the result to the specified type
            return type_of_output(result)           
        return wrapper
    return decorator


# function 1: Returns 5, but gets converted to a string
@type_converter(str)
def return_int():
    return 5

# function 2: Returns "not a number", but tries to convert to an int
@type_converter(int)
def return_string():
    return "not a number"

# mainline code to test the decorated functions
if __name__ == "__main__":
    y = return_int()
    print(type(y).__name__)

    try:
        y = return_string()
        print("shouldn't get here!")
    except ValueError:
        print("can't convert that string to an integer!") 