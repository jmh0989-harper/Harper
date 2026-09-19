# Group member: James Heinrihcs, Alana Heinrichs

# functions that are related to processing different variables
def height_process(feet, inch):
    height = (feet * 12) + inch
    print(f"Total height: {height} inches")
    return height

def bmi_process(weight, height):
    bmi = (weight / height ** 2) * 703
    print(f"BMI: {bmi:.1f}")
    return bmi

def report_process(bmi):
    # output
    if (bmi <= 18):
        return "Underweight"
    elif (bmi >= 25.5):
        return "Overweight"
    else:
        return "within the normal range"

# same math as bmi_process, but without printing (used by the chart)
def bmi_new(weight, height):
    bmi = (weight / height ** 2) * 703
    bmi = round(bmi, 1)
    return bmi

# BMI table: heights 58-76 inches across the top, weights 100-250 lbs down the side
def make_chart():
    print("\nBMI Table")
    print("Height in inches across the top, weight in pounds down the side")

    # header row of heights
    print("      ", end="")
    for height in range(58, 77, 2):
        print(f"{height:>7}", end="")
    print()

    # one row per weight
    for weight in range(100, 251, 10):
        print(f"{weight:>6}", end="")
        for height in range(58, 77, 2):
            print(f"{bmi_new(weight, height):>7}", end="")
        print()
    print()

# keeps asking until the user types a valid number, or q to quit
def get_number(prompt, number_type, allow_zero=False):
    while True:
        print(prompt)
        entry = input()

        if entry.lower() == "q":
            return None

        try:
            value = number_type(entry)
        except ValueError:
            print("That is not a valid number. Please try again, or enter q to quit.")
            continue

        if value < 0 or (value == 0 and not allow_zero):
            print("Please enter a number greater than 0, or enter q to quit.")
            continue

        return value

# BMI ranges provided by https://www.who.int/data/gho/data/themes/topics/topic-details/GHO/body-mass-index


# start
print("Welcome to James & Alana's BMI Calculator")
print("Enter q at any prompt to quit the program.")

while True:
    # input
    weight = get_number("Enter your current Weight (lbs)", float)
    if weight is None:
        break

    feet = get_number("Enter your current Height (ft)", int)
    if feet is None:
        break

    inch = get_number("Enter your current Height (in)", int, allow_zero=True)
    if inch is None:
        break

    # call processes
    height = height_process(feet, inch)
    bmi = bmi_process(weight, height)
    report = report_process(bmi)

    # ranges
    print("BMI ranges provided by World Health Organization")
    print("BMI of 18 or lower - Underweight")
    print("BMI of 18.5 to 25 - Normal range")
    print("BMI of 25.5 or higher - Overweight")

    # report
    print(f"With a BMI of {bmi:.1f}, you are {report}.")

    # repeat or quit
    print("Would you like to calculate another BMI? (y/n)")
    again = input()
    if again.lower() != "y":
        break

# BMI table
make_chart()

print("Thank you for using James & Alana's BMI Calculator. Goodbye!")