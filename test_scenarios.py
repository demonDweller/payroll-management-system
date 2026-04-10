"""
Manual test scenarios for the payroll system
Run these to verify functionality
"""

def test_scenario_1_basic_workflow():
    """
    Test: Add employee → Clock in → Clock out → Process payroll
    """
    print("\n=== TEST SCENARIO 1: Basic Workflow ===")
    print("1. Add a new employee")
    print("2. Clock in the employee")
    print("3. Wait a few seconds")
    print("4. Clock out the employee")
    print("5. Process payroll")
    print("6. View payroll logs")
    print("\n✅ Expected: Employee shows hours worked and correct pay")

def test_scenario_2_prevent_double_clock():
    """
    Test: Try to clock in twice without clocking out
    """
    print("\n=== TEST SCENARIO 2: Prevent Double Clock-in ===")
    print("1. Clock in employee")
    print("2. Try to clock in again")
    print("\n✅ Expected: Error message 'already clocked in'")

def test_scenario_3_overtime_calculation():
    """
    Test: Employee works >40 hours in a week
    """
    print("\n=== TEST SCENARIO 3: Overtime Calculation ===")
    print("1. Add employee with rate $20/hr")
    print("2. Simulate 45 hours worked (via multiple shifts)")
    print("3. Process payroll")
    print("\n✅ Expected: 40 * 20 + 5 * 30 = $950")

def test_scenario_4_employee_persistence():
    """
    Test: Exit and restart system
    """
    print("\n=== TEST SCENARIO 4: Data Persistence ===")
    print("1. Add employee")
    print("2. Exit system")
    print("3. Restart system")
    print("4. List employees")
    print("\n✅ Expected: Employee still exists")

if __name__ == "__main__":
    print("MANUAL TEST SCENARIOS")
    print("Run these by using the actual system")
    test_scenario_1_basic_workflow()
    test_scenario_2_prevent_double_clock()
    test_scenario_3_overtime_calculation()
    test_scenario_4_employee_persistence()