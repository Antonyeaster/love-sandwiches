import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPRED_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPRED_CLIENT.open("love_sandwiches")

def get_sales_data():
    """
    Get sales data input from the user
    """

    print("Please enter your sales data from the last market.")
    print("Data should be six numbers, separated by a commas.")
    print("Example: 10,15,2,6,9,4\n")

    data_str = input("Enter your data here: ")
    print(f"The data provided is {data_str}")

get_sales_data()