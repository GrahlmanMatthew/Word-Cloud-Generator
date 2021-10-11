import os

# Allows you to prompt the user for a filename (string input) and returns the path providing the file exists
def user_input_filename(prompt):
    value = ""
    while value == "":
        print("\n%s: " % prompt)
        value = input()
        if os.path.isfile('./input/' + str(value)):
            return './input/' + str(value)
        else:
            print("Invalid file name! (ensure the photo is in the input folder)")
            value = ''

# Allows you to prompt the user for an integer input between a lower and upper bound
def user_input_integer(prompt, lower_b, upper_b):
    value = -1
    while value == -1:
        print("\n%s between %d - %d: " % (prompt, lower_b, upper_b))
        value = int(input())
        if value >= lower_b and value <= upper_b:
            return value
        else:
            value = -1