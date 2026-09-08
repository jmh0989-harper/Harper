weight_lbs=float(input("Enter your weight in pounds (lbs): "))
height_feet = int(input("Enter your height in feet (ft): "))
height_inches = float(input("Enter your height in inches (in): "))
height_inches = height_feet * 12 + height_inches

bmi = (weight_lbs * 703) / (height_inches ** 2)
        
print("\nYour calculated BMI is: {round(bmi, 1)}")

print("\nLEGEND for BMI Scale \n A BMI of less than 18.5 is underweight \n A BMI of Greater than 18.8 and less than 24.9 is normal " \
"\n A BMI of Greater than 25 and less than 29.9 is overweight \n A BMI of Greater than 30 is Obese")