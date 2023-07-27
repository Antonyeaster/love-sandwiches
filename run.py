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

    while True:
        print("Please enter your sales data from the last market.")
        print("Data should be six numbers, separated by a commas.")
        print("Example: 10,15,2,6,9,4\n")

        data_str = input("Enter your data here: ")
        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print("data is valid")
            break
    
    return sales_data

def validate_data(values):
    """
    Inside the Try, converts all sting values to intergers
    Raises ValueError if strings can not be converted to int,
    or if there aren't exactly 6 values.

    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values are required, you provided {len(values)}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")
        return False

    return True


data = get_sales_data()
