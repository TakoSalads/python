


def main():

    #bills
    insurance = 240.41
    car_payment = 200.00
    phone_bill = 83.26
    overall = insurance + car_payment + phone_bill

    #pay
    salary = 1382.18 * 2
    pay = salary

    #savings
    tfsa = 7000 // 12
    posttfsa = pay - tfsa
    savingp = 12 * posttfsa * 0.70
    spending = 12 * posttfsa * 0.30

    #final pay
    sum = pay - overall

    

    print("Budget: \n")
    print(f"Insurance: {insurance}")
    print(f"Phone Bill: {phone_bill}")
    print(f"Car Payment: {car_payment}")  
    print(f"Bill Total: {overall}\n")
    print(f"Salary: {pay}")
    print(f"{pay} - {overall}\n")
    print(f"Montly Budget: {spending}")
    print(f"Savings: {savingp}")
    print(f"TFSA Payment: {tfsa}")

main()