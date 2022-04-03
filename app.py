from pathlib import Path
import fire
import questionary
import csv

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


def load_bank_data():
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
        The bank data from the data rate sheet CSV file.
    """

    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)

    return load_csv(csvpath)

def save_bank_results():
    # Ask for the file path to the latest banking data and load the CSV file.

    # Returns:
    #    The bank data from the data rate sheet CSV file.

# THIS IS THE PRINT RESULTS QUESTION AND SECOND QUESTION AND THEN SAVE TO FILE    

    save_results = questionary.text("Do you want to save the list of qualifying banks?").ask()
    if save_results == "No":
        exit()
    else:
        savepath = questionary.text("Where would you like to save the file (.csv):").ask()
        savepath = Path('location_results.csv')
        save_csv(savepath, save_qualifying_loans())

   
    return savepath
"""
def export_to_csv():
    z = save_bank_results(csvresults)
    f = open('./data/csvresults', 'w')
    writer = csv.writer(f)
    writer.writerow(f)
    f.close()
    
    return z 
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

    # Calculate the monthly debt ratio
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
        #savepath = Path(savepath)
        #save_csv(savepath, save_qualifying_loans())

    #csvpath = []
    #csvpath = Path('qualifying_loans.csv')
    #save_csv(csvpath, qualifying_loans)


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

    #save_bank_results1 = save_bank_results(qualifying_loans)
    #print(save_bank_results1)
    

if __name__ == "__main__":
    fire.Fire(run)

# Command Line Instruction
# python app.py --credit_score=750 --debt=5000 --income=20000
# python app.py --credit_score=805 --debt=3000 --income=8000
