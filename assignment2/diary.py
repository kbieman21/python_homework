#Task 1: Dairy

import traceback

try:
    #open the file for appending ('a') using a with statement to ensure it gets closed
    with open("diary.txt", "a") as diary:

        #check first prompt
        first_prompt = True

        while True:
            if first_prompt:
                response = input("What happened today?")
                first_prompt = False
            else:
                response = input("What else ")

           
         # Write the input to the file with a newline
            diary.write(response + "\n")

         # Exit the loop if the special phrase is entered
            if response == "done for now":
                break
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