"""
Session 12 - Classes and Objects Exercise

Classes:
    Employee   - name, idNumber, department, position
    Patient    - name, address, phone and emergency contact info
    Procedure  - a medical procedure performed on a patient

Python does not support multiple constructors the way Java/C++ do, so the
three Employee constructors required by the assignment are handled with
default argument values in a single __init__:

    Employee("Susan Meyers", 47899, "Accounting", "Vice President")  # 4 args
    Employee("Mark Jones", 39119)                                    # 2 args
    Employee()                                                       # default
"""

from datetime import date


# ---------------------------------------------------------------------------
# Employee
# ---------------------------------------------------------------------------
class Employee:
    def __init__(self, name="", id_number=0, department="", position=""):
        self._name = name
        self._id_number = id_number
        self._department = department
        self._position = position

    # Accessors
    def get_name(self):
        return self._name

    def get_id_number(self):
        return self._id_number

    def get_department(self):
        return self._department

    def get_position(self):
        return self._position

    # Mutators
    def set_name(self, name):
        self._name = name

    def set_id_number(self, id_number):
        self._id_number = id_number

    def set_department(self, department):
        self._department = department

    def set_position(self, position):
        self._position = position

    def __str__(self):
        return (f"{self._name:<15}{self._id_number:<12}"
                f"{self._department:<15}{self._position}")


# ---------------------------------------------------------------------------
# Patient
# ---------------------------------------------------------------------------
class Patient:
    def __init__(self, first_name, middle_name, last_name,
                 address, city, state, zip_code, phone,
                 emergency_contact_name, emergency_contact_phone):
        self._first_name = first_name
        self._middle_name = middle_name
        self._last_name = last_name
        self._address = address
        self._city = city
        self._state = state
        self._zip_code = zip_code
        self._phone = phone
        self._emergency_contact_name = emergency_contact_name
        self._emergency_contact_phone = emergency_contact_phone

    # Accessors
    def get_first_name(self):
        return self._first_name

    def get_middle_name(self):
        return self._middle_name

    def get_last_name(self):
        return self._last_name

    def get_address(self):
        return self._address

    def get_city(self):
        return self._city

    def get_state(self):
        return self._state

    def get_zip_code(self):
        return self._zip_code

    def get_phone(self):
        return self._phone

    def get_emergency_contact_name(self):
        return self._emergency_contact_name

    def get_emergency_contact_phone(self):
        return self._emergency_contact_phone

    # Mutators
    def set_first_name(self, first_name):
        self._first_name = first_name

    def set_middle_name(self, middle_name):
        self._middle_name = middle_name

    def set_last_name(self, last_name):
        self._last_name = last_name

    def set_address(self, address):
        self._address = address

    def set_city(self, city):
        self._city = city

    def set_state(self, state):
        self._state = state

    def set_zip_code(self, zip_code):
        self._zip_code = zip_code

    def set_phone(self, phone):
        self._phone = phone

    def set_emergency_contact_name(self, name):
        self._emergency_contact_name = name

    def set_emergency_contact_phone(self, phone):
        self._emergency_contact_phone = phone

    def get_full_name(self):
        return f"{self._first_name} {self._middle_name} {self._last_name}"

    def __str__(self):
        return (
            f"Name:               {self.get_full_name()}\n"
            f"Address:            {self._address}\n"
            f"                    {self._city}, {self._state} {self._zip_code}\n"
            f"Phone:              {self._phone}\n"
            f"Emergency Contact:  {self._emergency_contact_name} "
            f"({self._emergency_contact_phone})"
        )


# ---------------------------------------------------------------------------
# Procedure
# ---------------------------------------------------------------------------
class Procedure:
    def __init__(self, procedure_name, procedure_date, practitioner, charge):
        self._procedure_name = procedure_name
        self._procedure_date = procedure_date
        self._practitioner = practitioner
        self._charge = charge

    # Accessors
    def get_procedure_name(self):
        return self._procedure_name

    def get_procedure_date(self):
        return self._procedure_date

    def get_practitioner(self):
        return self._practitioner

    def get_charge(self):
        return self._charge

    # Mutators
    def set_procedure_name(self, procedure_name):
        self._procedure_name = procedure_name

    def set_procedure_date(self, procedure_date):
        self._procedure_date = procedure_date

    def set_practitioner(self, practitioner):
        self._practitioner = practitioner

    def set_charge(self, charge):
        self._charge = charge

    def __str__(self):
        return (
            f"Procedure:    {self._procedure_name}\n"
            f"Date:         {self._procedure_date}\n"
            f"Practitioner: {self._practitioner}\n"
            f"Charge:       ${self._charge:,.2f}"
        )


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------
def main():
    # ----- Part 1: Employees -------------------------------------------------
    # Uses the 4-argument constructor for all three employees (per the data
    # table). The other two constructors are demonstrated afterwards.
    employee1 = Employee("Susan Meyers", 47899, "Accounting", "Vice President")
    employee2 = Employee("Mark Jones", 39119, "IT", "Programmer")
    employee3 = Employee("Joy Rogers", 81774, "Manufacturing", "Engineer")

    print("=" * 60)
    print("EMPLOYEES")
    print("=" * 60)
    print(f"{'Name':<15}{'ID Number':<12}{'Department':<15}{'Position'}")
    print("-" * 60)
    for emp in (employee1, employee2, employee3):
        print(f"{emp.get_name():<15}{emp.get_id_number():<12}"
              f"{emp.get_department():<15}{emp.get_position()}")

    # Demonstrate the other two constructors and the mutators
    print("\n--- Testing other constructors and mutators ---")
    two_arg_emp = Employee("Test Person", 12345)          # name + ID only
    default_emp = Employee()                               # defaults
    print(f"Two-arg constructor: name='{two_arg_emp.get_name()}', "
          f"id={two_arg_emp.get_id_number()}, "
          f"dept='{two_arg_emp.get_department()}', "
          f"position='{two_arg_emp.get_position()}'")
    print(f"Default constructor: name='{default_emp.get_name()}', "
          f"id={default_emp.get_id_number()}, "
          f"dept='{default_emp.get_department()}', "
          f"position='{default_emp.get_position()}'")

    default_emp.set_name("Updated Name")
    default_emp.set_id_number(99999)
    default_emp.set_department("HR")
    default_emp.set_position("Manager")
    print(f"After mutators:      {default_emp}")

    # ----- Part 2: Patient and Procedures ------------------------------------
    patient = Patient(
        first_name="John",
        middle_name="Michael",
        last_name="Doe",
        address="123 Main Street",
        city="Chicago",
        state="IL",
        zip_code="60601",
        phone="312-555-0142",
        emergency_contact_name="Jane Doe",
        emergency_contact_phone="312-555-0187",
    )

    today = date.today().strftime("%m/%d/%Y")
    procedure1 = Procedure("Physical Exam", today, "Dr. Irvine", 250.00)
    procedure2 = Procedure("X-ray", today, "Dr. Jamison", 500.00)
    procedure3 = Procedure("Blood test", today, "Dr. Smith", 200.00)
    procedures = [procedure1, procedure2, procedure3]

    print("\n" + "=" * 60)
    print("PATIENT INFORMATION")
    print("=" * 60)
    print(patient)

    print("\n" + "=" * 60)
    print("PROCEDURES")
    print("=" * 60)
    for number, proc in enumerate(procedures, start=1):
        print(f"\nProcedure #{number}")
        print("-" * 30)
        print(proc)

    total_charges = sum(proc.get_charge() for proc in procedures)
    print("\n" + "=" * 60)
    print(f"TOTAL CHARGES: ${total_charges:,.2f}")
    print("=" * 60)


if __name__ == "__main__":
    main()