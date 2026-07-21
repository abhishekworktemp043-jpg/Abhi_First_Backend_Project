class BankAccount:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError('amount cannot be negative')
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            raise ValueError('Not enough funds')
    def print_info(self):
        print(self.name)
        print(self.balance)

    def __str__(self):
        return f"{self.name}'s account - Balance: {self.balance}"

class SavingsAccount(BankAccount):
    def __init__(self, name, balance=0,interest_rate=0.06):
        super().__init__(name, balance)
        self.interest_rate = interest_rate
    def pay_with_interest(self):
        interest = self.balance * self.interest_rate
        self.deposit(interest)

if __name__ == '__main__':

    account1 = BankAccount("Abhishek", 10000)

    account1.deposit(100)
    account1.withdraw(10)
    account1.print_info()

    print("##################################################")

    saving_account1 = SavingsAccount("Zara", 10000)
    saving_account1.pay_with_interest()
    saving_account1.print_info()
    print("##################################################")
    print(account1)
    print("##################################################")
    print(saving_account1)
