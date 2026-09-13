# Group member: James Heinrihcs, Alana Heinrichs

# functions that are related to processing different variables
def height_process(feet, inch):
    height = (feet * 12) + inch
    print(f"Total height: {height} inches")
    return height

def bmi_process(weight,height):
    bmi = (weight/height** 2) * 703
    print(f"BMI: {bmi:.1f}")
    return bmi

def report_process(bmi):
    # output
    if (bmi <= 18): 
        return "Underweight"
    elif(bmi >= 25.5): 
        return "Overweight"
    else:
        return "within the normal range"

# BMI ranges provided by https://www.who.int/data/gho/data/themes/topics/topic-details/GHO/body-mass-index


# start
print("Welcome to James & Alana's BMI Calculator")

print("Enter your current Weight (lbs)")
weight = float(input())

print("Enter your current Height (ft)")
feet = int(input())

print("Enter your current Height (in)")
inch = int(input())

# call processes
height = height_process(feet,inch)
bmi = bmi_process(weight,height)
report = report_process(bmi)

# ranges
print("BMI ranges provided by World Health Organization")
print("BMI of 18 or lower - Underweight")
print("BMI of 18.5 to 25 - Normal range")
print("BMI of 25.5 or higher - Overweight")

# report
print(f"With a BMI of {bmi:.1f}, you are {report}.")
