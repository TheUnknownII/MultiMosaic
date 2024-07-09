
from ObjectOriented_Examples.Examples.example1 import *

# Create an instance of BankAccount
account = BankAccount("Alice", 1000)

# Use the deposit method
account.deposit(500)

# Use the withdraw method
account.withdraw(200)

# Check the balance
print(f"Current balance: ${account.get_balance()}")

# Print the account details
print(account)
