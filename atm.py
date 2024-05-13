class Transaction:
    def __init__(self, amount, transaction_type):
        self.amount = amount
        self.transaction_type = transaction_type


class User:
    def __init__(self, user_id, pin):
        self.user_id = user_id
        self.pin = pin
        self.balance = 0
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(Transaction(amount, "Deposit"))

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append(Transaction(amount, "Withdraw"))
        else:
            print("Insufficient funds."+"\n")

    def transfer(self, amount, recipient):
        if amount <= self.balance:
            self.balance -= amount
            recipient.balance += amount
            self.transactions.append(Transaction(amount, "Transfer to " + recipient.user_id))
            recipient.transactions.append(Transaction(amount, "Transfer from " + self.user_id))
        else:
            print("Insufficient funds."+"\n")

    def display_transactions(self):
        print("Transaction History:")
        for transaction in self.transactions:
            print(f"{transaction.transaction_type}: ${transaction.amount}")


class ATM:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id, pin):
        if user_id not in self.users:
            self.users[user_id] = User(user_id, pin)
            

    def login(self, user_id, pin):
        if user_id in self.users:
            if self.users[user_id].pin == pin:
                print("Login successful!"+"\n")
                return self.users[user_id]
            else:
                print("Invalid PIN."+"\n")
        else:
            print("User not found."+"\n")
        return None


class TransactionProcessor:
    @staticmethod
    def process_deposit(user, amount):
        user.deposit(amount)
        print("Deposit successful."+"\n")

    @staticmethod
    def process_withdraw(user, amount):
        user.withdraw(amount)

    @staticmethod
    def process_transfer(sender, recipient, amount):
        sender.transfer(amount, recipient)
        print("Transfer successful."+"\n")


class ATMInterface:
    @staticmethod
    def display_balance(user):
        print("Your balance is:", user.balance,"\n")

    @staticmethod
    def display_menu():
        print("\n1. Display Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Display Transactions")
        print("6. Quit\n")

    @staticmethod
    def get_user_input(prompt):
        return input(prompt)

    @staticmethod
    def prompt_amount():
        return float(input("Enter amount: "))


def main():
    print("Welcome to Bank")
    print("----------------\n")
    atm = ATM()

    user_id = "user1"
    pin = "123"
    atm.add_user(user_id, pin)
    atm.add_user("user2", "321")

    user = None
    while not user:
        entered_user_id = ATMInterface.get_user_input("Enter user ID: ")
        entered_pin = ATMInterface.get_user_input("Enter pin: ")
        user = atm.login(entered_user_id, entered_pin)

    while True:
        ATMInterface.display_menu()
        choice = ATMInterface.get_user_input("Enter your choice: ")

        if choice == "1":
            ATMInterface.display_balance(user)
        elif choice == "2":
            amount = ATMInterface.prompt_amount()
            TransactionProcessor.process_deposit(user, amount)
        elif choice == "3":
            amount = ATMInterface.prompt_amount()
            TransactionProcessor.process_withdraw(user, amount)
        elif choice == "4":
            recipient_user_id = ATMInterface.get_user_input("Enter recipient user ID: ")
            recipient = atm.users.get(recipient_user_id)
            if recipient:
                amount = ATMInterface.prompt_amount()
                TransactionProcessor.process_transfer(user, recipient, amount)
            else:
                print("Recipient not found.\n")
        elif choice == "5":
            user.display_transactions()
        elif choice == "6":
            print("Thank you for using the ATM. Goodbye!\n")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()