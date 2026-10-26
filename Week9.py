
courses = {
    "Python": {"Alice", "Bob", "Charlie", "David"},
    "Database": {"Bob", "Eve", "Frank", "Alice"},
    "Networking": {"Charlie", "George", "Alice"},
    "Cybersecurity": {"David", "Eve", "Henry", "Charlie"},
}


print("Course Enrollments")
print("------------------")
for course, students in courses.items():
    print(f"{course}: {len(students)} students")
    print(f"  {sorted(students)}")


python_and_database = courses["Python"] & courses["Database"]
python_and_cyber = courses["Python"] & courses["Cybersecurity"]

print("\nStudents in Python and Database:")
for name in sorted(python_and_database):
    print(name)

print("\nStudents in Python and Cybersecurity:")
for name in sorted(python_and_cyber):
    print(name)


all_students = set().union(*courses.values())

print(f"\nTotal unique students: {len(all_students)}")
print("All Unique Students:")
for name in sorted(all_students):
    print(name)


only_one_course = set()
for student in all_students:
    count = sum(1 for students in courses.values() if student in students)
    if count == 1:
        only_one_course.add(student)

print("\nStudents taking only one course:")
for name in sorted(only_one_course):
    print(name)

# ---------------------------------------------------------------
# Step 6: User search feature
# ---------------------------------------------------------------
print()
search_name = input("Enter student name: ").strip().title()

if search_name in all_students:
    print(f"\n{search_name} is enrolled in:")
    for course, students in courses.items():
        if search_name in students:
            print(course)
else:
    print("Student not found.")