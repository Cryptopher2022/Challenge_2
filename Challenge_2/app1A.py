"""
To initialize the program, we import the following libraries and sub-libraries
libraries:
pathlib
fire
questionary
csv

from within pathlib, the function in that library that we need is called Path
"""

from pathlib import Path
import fire
import questionary
import csv

"""
From filters that have been set up in a folder called "qualifier", we pull functions that we need:

load_csv
save_csv
calculate_monthly_debt_ratio
calculate_loan_to_value_ratio
filter_max_loan_size
filter_credit_score
filter_debt_to_income
filter_loan_to_value

These function are stored as filters in the file names shown below in the ./filters/ director

credit_score.py
debt_to_income.py
loan_to_value.py
max_loan_size.py
"""

from qualifier.utils.fileio import load_csv, save_csv

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value

# to qualifier.filters.csvresults export csvresults 

"""
The load_bank_data() function asks the User where to find the most current daily_rate_sheet.csv with has a list of the following information:

Lender,Max Loan Amount,Max LTV,Max DTI,Min Credit Score,Interest Rate

From this current data, the User can utilize the program to evaluate current loan availability from a number of different Lenders, and on what terms each offer.  

Ask for via the questionary function from the User:
 
        the file path to the latest banking data and load the CSV file.

Returns:
        The bank data from the data rate sheet CSV file and a variable from which to access it.
"""

def load_bank_data():
    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)

    return load_csv(csvpath)

"""
The save_bank_results() function does several tasks as requested by the user:

    1. Given that there are more then zero qualifying banks, the program asks 
    the User if they would like to save a list of the qualifying banks.
        A. if no, the program terminates.
        B. if Yes, the program continues to C., below
        C. The program prompts the User for a file name to save the qualifying banks 
        and loads the newly created .csv (specified) file in the ./data/ directory, 
        which the User is notified of during the request for the file name.
    2. If there are zero banks, the program says so and terminates.  
    
"""
def save_bank_results():
    save_results = questionary.text("Do you want to save the list of qualifying banks?").ask()
    if save_results == "No":
        exit()
    else:
        savepath = questionary.text("Where would you like to save the file (.csv):").ask()
        savepath = Path('location_results.csv')
        save_csv(savepath, save_qualifying_loans())
   
    return savepath
"""
    The get_applicant_info() function uses the questionary library to prompt the user for personal
    information that will be used in the evaluation of qualifying banks.  
"""
def get_applicant_info():
    
    credit_score = questionary.text("What's your credit score?").ask()    
    debt = questionary.text("What's your total monthly debt payments?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's the loan amount requested?").ask()
    home_value = questionary.text("What's the price of the new home?").ask()
    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return(credit_score, debt, income, loan_amount, home_value)

def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")
    if {len(bank_data_filtered)} == "0":
        print(f"There are no loans available.  Please try again.")
    
        

    return bank_data_filtered

"""
This section of the program uses the questionary library to as specified questions that
the customer wanted as criteria:

Do you want to save the list of qualifying loans?
    Yes, continues
    No, terminates the program

    For Yes,
        The program defines a folder in which to save the newly created user file and tell
        the User where they can find their list of banks.

        The program then takes the qualifying_loans (the list of filtered banks) and saves it
        to the file created by the User in CSV format.  
"""


def save_qualifying_loans(qualifying_loans):
    """Saves the qualifying loans to a CSV file.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """
    save_results = questionary.text("Do you want to save the list of qualifying banks?").ask()
    if save_results == "No":
        exit()
    else:
        savepath = []
        directory = "./data/"
        savepath = directory + questionary.text("Your CSV file will be in the './data/' folder. What would you like to call it? (.csv):").ask()
        with open(savepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(qualifying_loans)
            csvfile.close()
            pass 
    

def run():
    """The main function for running the script."""

    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()
    
    

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )
    # Save qualifying loans
    save_qualifying_loans(qualifying_loans)
    print(qualifying_loans)

    """The final output of the program is a screen listing of the banks found in 
    the Users newly created file"""
    

if __name__ == "__main__":
    fire.Fire(run)

