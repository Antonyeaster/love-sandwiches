import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint


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
    run a while loop to get valid data from the user in the terminal.
    which must be a string of 6 characters
    The while loop will keep running until valid data is entered.
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


def update_sales_worksheet(data):
    """
    Updata sales worksheet, add new row with data provided
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Calculate the stock amount against the sold amount to see our surplus,
    - Any positive values means items wasted
    - Any negative values means more sandwiches made x the negative value
    """

    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data


def main():
    """
    Run all program functions
    """

    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)


print("Welcome to Love Sandwiches Data Automation")
main()