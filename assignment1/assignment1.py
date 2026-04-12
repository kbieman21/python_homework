# Write your code here.

#Task 1 Hello
def hello():
    return "Hello!"

hello()


#Task 2 Greet with a Formatted String
def greet(name):
    return "Hello, " + name + "!"

greet("Kibreab")


#Task 3 Calculator
def calc(a, b, operation = "multiply"):
    try:
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "int_divide":
            return a // b
        elif operation == "divide":
            return a / b
        elif operation == "modulo":
            return a % b
        elif operation == "power":
            return a ** b
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return "You can't " + operation + " those values!"
 

calc(5, 3, "add ")

#Task 4 Data Type Conversion
def data_type_conversion(value, target_type):
    try:
        if target_type == "int":
            return int(value)
        elif target_type == "float":
            return float(value)
        elif target_type == "str":
            return str(value)
        else:
            return "Invalid target type."
    except ValueError:
        return f"You can't convert {value} into a {target_type}."
    
    
data_type_conversion("str", "float")


#Task 5 Grading System, Using *args
def grade(score1, score2, score3):
    try:
        average = (score1 + score2 + score3) / 3
        if average >= 90:
            return "A"
        elif average >= 80:
            return "B"
        elif average >= 70:
            return "C"
        elif average >= 60:
            return "D"
        else:
            return "F"
    except TypeError:
        return "Invalid data was provided."
    
grade(75, 85, 95)

#Task 6 Use a For Loop with a Range
def repeat(string, count):
    result = ""
    for i in range(count):
        result += string
    return result

repeat("up,", 4)

#Task 7 Student Scores, Using **kwargs
def student_scores(operation, **kwargs):
    if operation == "mean":
        return sum(kwargs.values()) / len(kwargs)
    elif operation == "best":
        return max(kwargs, key=kwargs.get)
    else:
        return "Invalid operation."
    
student_scores("mean", student1=75, student2=85, student3=95)


#Task 8 Titleize, with String and List Operations
def titleize(string):
    little_words = ["a", "on", "an", "the", "of", "and", "is", "in"]
    words = string.split()
    result = []
    # 1. Check if it's the first or last word
    for i, word in enumerate(words):
        if i == 0 or i == len(words) -1:
            result.append(word.capitalize())

        elif word.lower() in little_words:
            result.append(word.lower())
        
        else:        
            result.append(word.capitalize()) 

    return " ".join(result)

titleize("hello world is my favorite place")


#Task 9 Hangman, with more String Operations
def hangman(secret, guess):
    result = ""
    for letter in secret:
        if letter in guess:
            result += letter
        else:
            result += "_"
    return result

hangman("alphabet","ab")

#Task 10 Pig Latin, Another String Manipulation Exercise
def pig_latin(sentence):
    vowels = "aeiou"
    words = sentence.split()
    result = []
    
    for word in words:
        if word[0] in vowels:
            result.append(word + "ay")

        elif word.startswith("qu"):
            result.append(word[2:] + "quay")
        else:
            first_vowel_index = 0
            for i, letter in enumerate(word):
                if letter in vowels:
                        if letter == "u" and i > 0 and word[i-1] == "q":
                            continue
                first_vowel_index = i
                break

            consonants = word[:first_vowel_index]
            rest_of_word = word[first_vowel_index:]
            result.append(rest_of_word + consonants + "ay")
    
    return " ".join(result)

pig_latin("hello")