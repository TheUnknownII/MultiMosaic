# Define the BankAccount class

class BankAccount:
    def __init__(self, owner, balance=0):
        """"Initialize the BankAccount with owner's name and initial balance"""
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        """"Deposit a scpecific amount into the account"""
        if amount > 0:
            self.balance += amount
            print(f"Deposited ${amount}. New balance: ${self.balance}")
        else:
            print(f"Deposit amount must be positive.")

    def withdraw(self, amount):
        """"Withdraw a specified amount from the account"""
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.balance}")
        elif amount > self.balance:
            print("Insufficient funds.")
        else:
            print("Withdrawal amount must be positive.")

    def get_balance(self):
        """"Return the current balance"""
        return self.balance
    
    def __str__(self):
        """Return a string representation of the account"""
        return f"BankAccount(owner={self.owner}, balance=${self.balance})"
    
# # Create an instance of BankAccount
# account = BankAccount("Alice", 1000)

# #Use the deposit method
# account.deposit(500)

# #Check the balance
# print(f"Current balance: ${account.get_balance()}")

# #Print the account details
# print(account)