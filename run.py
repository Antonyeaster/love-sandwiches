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
    run a while loop to get valid data from the user in the terminal.
    which must be a string of 6 characters
    The while loop will keep running until valid data is entered.
    """

    while True:
        print("Please enter your sales data from the last market.")
        print("Data should be six numbers, separated by a commas.")
        print("Example: 10,15,2,6,9,4\n")

        data_str = input("Enter your data here:\n")
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


def update_worksheet(data, worksheet):
    """
    Receives a list of intergers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    update_to_worksheet = SHEET.worksheet(worksheet)
    update_to_worksheet.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")


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


def get_last_5_entries_sales():
    """
    Collects columns from data worksheet, collecting
    the last 5 entries for each sandwich and returns 
    the data in a list of lists
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])  
    return columns


def calculate_stock_data(data):
    """
    Calculating the average stock for each item type, and adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []
    
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """
    Run all program functions
    """

    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")


print("Welcome to Love Sandwiches Data Automation")
main()