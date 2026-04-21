import logging

# Task 1 Writing and Testing a Decorator

# set up logging
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def logger_decorator(func):
    def wrapper_logger(*args, **kwargs):
       # execute the function and capture the result
       result = func(*args, **kwargs)
       # identify the parameters passed to the function
       pos_params = list(args) if args else "none"
       kw_params = kwargs if kwargs else "none"

       # construct the log message
       log_message = (
           f"\nFunction {func.__name__}\n" 
           f"Positional parameters: {pos_params}\n"
           f"Keyword parameters: {kw_params}\n"
           f"Result: {result}"
       )

       # write the log message to the log file
       logger.log(logging.INFO, log_message)

       return result
    
    return wrapper_logger


# function 1: No parameters, returns nothing
@logger_decorator
def greet():
    print("Hello, World!")


# function 2: One parameter (variable positional arguments), returns true
@logger_decorator
def pos_args_func(*args):
    return True

# function 3: Multiple parameters (variable keyword arguments), returns logger_decorator
@logger_decorator
def kw_args_func(**kwargs):
    return logger_decorator



# mainline code to test the decorated functions
if __name__ == "__main__":
    # calling the above functions with different parameters to test the logging
    greet()
    pos_args_func(1, 2, 3)
    kw_args_func(a=1, b=2, c=3) 



# Task 2: A Decorator that Takes an Argument