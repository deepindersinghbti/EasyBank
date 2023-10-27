from pathlib import Path
from os import getcwd

balance = 0
print("Welcome to EasyBank!")
def check_for_file():
    """Check if the data file exists and create it if not"""
    directory_path = getcwd()
    file_path = Path(directory_path) / "data.txt"

    if not file_path.exists():
        with open("data.txt", "w"):
            pass

def get_choice():
    """Ask the user if he/she would like to register or login"""
    while True:
        try:
            choice = int(input("Enter 0 for new and 1 for an existing user: "))
            if choice in (0, 1):
                return choice
            else:
                print("Invalid input.")
        except ValueError:
            print("Invalid input.")

def input_valid_username(prompt):
    """Prompt for a valid username without whitespaces or zero length"""
    while True:
        new_username = input(prompt).strip()
        if not new_username:
            print("Username length cannot be zero.")
        elif ' ' in new_username or '\t' in new_username:
            print("Username cannot contain whitespaces.")
        else:
            return new_username

def input_valid_password(prompt):
    """Prompt for a valid password with minimum length of 6 characters"""
    while True:
        new_password = input(prompt).strip()
        if len(new_password) < 6:
            print("Password must be at least 6 characters long.")
        elif ' ' in new_password or '\t' in new_password:
            print("Password cannot contain whitespaces.")
        else:
            return new_password

def register():
    '''Lets the user create a username and a password'''
    new_username = input_valid_username("Enter a username: ")

    with open('data.txt', 'a+') as file:
        file.seek(0)
        lines = [line.strip().split('\t') for line in file]

        # Check if user exists
        user_exists = any(user and user[0] == new_username for user in lines)

        while user_exists:
            print("Username already taken! Please choose another.")
            new_username = input_valid_username("Enter a username: ")
            user_exists = any(user and user[0] == new_username for user in lines)

        file.write(new_username + '\t')

    # Set password
    new_password = input_valid_password("Set your password: ") 
    confirm = input_valid_password("Confirm your password: ")
    
    while new_password != confirm:
        print("Passwords do not match. Please confirm your password again.")
        confirm = input_valid_password("Confirm your password: ")

    with open('data.txt', 'a+') as file:
        file.write(new_password + '\t')
    
    # Account number
    while True:
        try:
            new_account = int(input("Enter your account number: "))
            break
        except:
            print("Please enter a valid 12-digit account number.")
    
    while len(str(new_account)) != 12:
        print("Account number must consist of 12 digits.")
        try:
            new_account = int(input("Enter your account number: "))
            break
        except:
            print("Please enter a valid 12-digit account number.")
            
    
    account_exists = any(user and user[2] == new_username for user in lines)
    while account_exists:
        print("Account number already exists! Please enter another one or login.")
        try:
            new_account = int(input("Enter your account number: "))
            break
        except:
            print("Please enter a valid 12-digit account number.")
        

    with open('data.txt', 'a+') as file:
        file.seek(0)
        file.write(str(new_account) + '\t')
        file.write('0\n')

    print("Registration successful. Please re-run and choose the login option.")

def login_operations():
    '''Lets the user login and perform operations after registration'''
    existing_username = input_valid_username("Enter your username: ")

    with open('data.txt', 'r') as file:
        file.seek(0)
        lines = [line.strip().split() for line in file]

        # Check if user exists
        user_data = next((user for user in lines if user and user[0] == existing_username), None)

        if user_data is not None:
            balance = float(user_data[3])

            existing_password = input_valid_password("Enter your password: ")

            if existing_password == user_data[1]:
                print("Access Granted!")
                print("Select an option:")
                print("1. Add funds")
                print("2. Withdraw funds")
                print("3. Transfer funds")
                print("4. Check balance")

                fx_choice = int(input("Enter your choice: "))

                if fx_choice == 1:
                    deposit_amt = float(input("Enter amount to deposit: "))
                    while deposit_amt <= 0:
                        print("Please enter a number greater than zero.")
                        deposit_amt = float(input("Enter amount to deposit: "))
                    while deposit_amt > 20000:
                        print("You can only deposit a maximum of Rs. 20,000 at a time.")
                        deposit_amt = float(input("Enter amount to deposit: "))

                    for user in lines:
                        if user and user[0] == existing_username:
                            user[3] = str(float(user[3]) + round(deposit_amt, 2))

                    with open('data.txt', 'w+') as file:
                        file.seek(0)
                        for l in lines:
                            file.write('\t'.join(l) + '\n')

                    print(f"Rs. {deposit_amt} successfully deposited.")
                elif fx_choice == 2:
                    withdrawal_amt = float(input("Enter amount to withdraw: ").strip())
                    while withdrawal_amt <= 0:
                        print("Withdrawal amount cannot be smaller than or equal to zero.")
                        withdrawal_amt = float(input("Enter amount to withdraw: ").strip())
                    while withdrawal_amt > 10000:
                        print("You cannot withdraw more than Rs. 10,000 at a time.")
                        withdrawal_amt = float(input("Enter amount to withdraw: ").strip())
                    while withdrawal_amt > balance:
                        print(f"Insufficient funds in account. Please enter at most Rs. {balance}")
                        withdrawal_amt = float(input("Enter amount to withdraw: ").strip())

                    for user in lines:
                        if user and user[0] == existing_username:
                            user[3] = str(float(user[3]) - round(withdrawal_amt, 2))

                    with open('data.txt', 'w+') as file:
                        file.seek(0)
                        for l in lines:
                            file.write('\t'.join(l) + '\n')

                    print(f"Rs. {withdrawal_amt} successfully withdrawn.")
                elif fx_choice == 3:
                    beneficiary_name = input("Enter beneficiary username: ").strip()
                    beneficiary_name_check = next((user for user in lines if user and user[0] == beneficiary_name and user[0] != existing_username), None)
                    while beneficiary_name_check is None :
                        print("User not found.")
                        beneficiary_name = input("Enter beneficiary username: ").strip()
                        beneficiary_name_check = next((user for user in lines if user and user[0] == beneficiary_name and user[0] != existing_username), None)

                    while True:
                        try:
                            beneficiary_account = int(input("Enter beneficiary account number: ").strip())
                            while len(str(beneficiary_account)) != 12:
                                print("Please enter a valid 12-digit account number.")
                            break
                        except Exception as e:
                            print("Invalid account number.")
                            print(f"Exception {type(e).__name__} occurred: {str(e)}")

                    beneficiary_account_check = next((user for user in lines if user and user[2] == str(beneficiary_account)), None)
                    while beneficiary_account_check is None:
                        print("Account number does not exist.")
                        beneficiary_account = int(input("Enter beneficiary account number: ").strip())
                        beneficiary_account_check = next((user for user in lines if user and user[2] == str(beneficiary_account)))

                    while True:
                        try:
                            beneficiary_account_confirm = int(input("Confirm beneficiary account number: ").strip())
                            while beneficiary_account_confirm != beneficiary_account:
                                print("Account numbers do not match.")
                                beneficiary_account_confirm = int(input("Confirm beneficiary account number: ").strip())
                            break
                        except:
                            print("Invalid input.")

                    while True:
                        try:
                            transfer_amt = round(float(input("Enter transfer amount: ").strip()), 2)
                            break
                        except:
                            print("Invalid amount.")
                            transfer_amt = round(float(input("Enter transfer amount: ").strip()), 2)

                    while transfer_amt <= 0:
                        print("Transfer amount cannot be smaller than or equal to zero.")
                        transfer_amt = round(float(input("Enter transfer amount: ").strip()), 2)
                    while transfer_amt > balance:
                        print(f"Insufficient funds in account. Please enter at most Rs. {balance}")
                        transfer_amt = round(float(input("Enter transfer amount: ").strip()), 2)

                    # Credit to beneficiary
                    for user in lines:
                        if user and user[0] == beneficiary_name and user[2] == str(beneficiary_account_confirm):
                            user[3] = str(float(user[3]) + transfer_amt)

                    # Debit from payee
                    for user in lines:
                        if user and user[0] == existing_username:
                            user[3] = str(float(user[3]) - transfer_amt)
                    balance -= transfer_amt  # Update user's balance

                    with open('data.txt', 'w+') as file:
                        file.seek(0)
                        for l in lines:
                            file.write('\t'.join(l) + '\n')
                    print(f"Rs. {transfer_amt} successfully transferred.")
                elif fx_choice == 4:
                    print(f"Account balance is Rs. {balance}")
                else:
                    print("Error.")


if __name__ == '__main__':
    check_for_file()
    choice = get_choice()
    if choice == 0:
        register()
    elif choice == 1:
        login_operations()