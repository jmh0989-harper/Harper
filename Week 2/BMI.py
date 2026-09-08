weight_lbs=float(input("How much do you weigh in pounds "))
height_feet = int(input("how tall are you in feet "))
height_inches = float(input("how tall you are in Inches excluding the feet you said previously "))
height_inches = height_feet * 12 + height_inches

bmi = (weight_lbs * 703) / (height_inches ** 2)
        
print(f"\nYour calculated BMI is: {round(bmi, 1)}")

print("\nLEGEND for BMI Scale \n A BMI of less than 18.5 is underweight \n A BMI of Greater than 18.8 and less than 24.9 is normal " \
"\n A BMI of Greater than 25 and less than 29.9 is overweight \n A BMI of Greater than 30 is Obese")