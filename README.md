# Activity: Add questionary to the Loan Qualifier App

In this activity, you'll use Questionary to enhance your loan qualifier app.

## Background

Using the Questionary library, you can add even more functionality to your loan qualifier application. Usability and interactivity are hallmarks of good software development. The easier it is for a user to interact with your application, the more inclined they are to use it.

Your task in this activity is to improve the usability of your loan qualifier application with the help of Questionary.


## Instructions

Use the files in the Unsolved folder to complete the following steps.

#### Import Questionary and Access Data File

1. Open `app.py`, and add `questionary` to the imports list at the top of the file.

2. Review the code changes that were made regarding the import of `daily_rate_sheet.csv`. Rather than hardcoding the file path, Questionary is used to input the location via the CLI. The following steps were taken to make this change:

    * The hardcoded file path for the `daily_rate_sheet.csv`file was removed from the `load_bank_data()` function call.

    * Inside the `load_bank-data()` function, a Questionary prompt was added to get input from the user. In the line where the value for `csvpath` was set, the `file_path` variable was replaced with the following Questionary prompt: `questionary.text("Enter a file path to a rate-sheet (.csv):").ask()`

        The new function appears as follows:

        ```python
        def load_bank_data():
            """Ask for the file path to the latest banking data and load the CSV file.

            Returns:
                The bank data from the data rate sheet CSV file.
            """

        csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
        csvpath = Path(csvpath)

        return load_csv(csvpath)
        ```

3. Open the command line and run your loan qualifier app with the following code:

    ```shell
    python app.py --credit_score=750 --debt=5000 --income=20000
    ```

4. When prompted for your CSV file path, enter `./data/daily_rate_sheet.csv`.

Now we can dynamically set the location of the `daily_rates_sheet.csv` file.

#### Prompt the User for Loan Information

Next, you'll create a dialog in a new function named `get_applicant_info()` that will prompt the user for their loan information. Complete the following steps:

1. In `app.py`, in the `run()` function, remove the parameters for `credit_score`, `debt`, and `income`.

2. In the comment above where `credit_score` is defined, change the comment from `# **Set** the applicant's information` to `# **Get** the applicant's information`.

3. Remove all of the defined values for `credit_score`, `debt`, `income`,`loan_amount`, and `home_value`, and set all equal to a new function named `get_applicant_info()`.

    ```python
    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()
    ```

This function will prompt the user via the command line for the applicant's information, then return it so that you can set the values for `credit_score`, `debt`, `income`,`loan_amount`, and `home_value`.





THIS IS ADDED TEXT TO ENSURE CLONING IS WORKING