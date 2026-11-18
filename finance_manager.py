from datetime import datetime
from transaction import Transaction
from storage import (
    load_transactions,
    save_transactions,
    load_budgets,
    save_budgets
)


# FinanceManager კლასი მართავს ტრანზაქციებსა და ბიუჯეტებს.
# აქ ხდება მონაცემების დამატება, წაშლა, შეცვლა, ძებნა და შეჯამება.

class FinanceManager:

    # კონსტრუქტორი ქმნის ტრანზაქციების სიას და ტვირთავს შენახულ მონაცემებს.
    # JSON-დან მიღებული მონაცემებით იქმნება Transaction ობიექტები.
    def __init__(self):
        self.transactions = []
        self.budgets = load_budgets()

        saved_transactions = load_transactions()

        for data in saved_transactions:
            transaction = Transaction(
                data["amount"],
                data["category"],
                data["transaction_type"],
                data["date"],
                data.get("comment", "")
            )

            self.transactions.append(transaction)

    # ქმნის ახალ ტრანზაქციას და ინახავს ფაილში.
    # თუ შენახვა ვერ მოხერხდა, დამატებულ ჩანაწერს სიიდან შლის.
    def add_transaction(self, amount, category, transaction_type, comment=""):
        transaction = Transaction(
            amount,
            category,
            transaction_type,
            comment=comment
        )

        self.transactions.append(transaction)

        if save_transactions(self.get_transactions_data()):
            return True

        self.transactions.pop()
        return False

    # ყველა Transaction ობიექტს ლექსიკონად გარდაქმნის.
    # მიღებული სია გამოიყენება JSON ფაილში შესანახად.
    def get_transactions_data(self):
        result = []

        for transaction in self.transactions:
            result.append(transaction.to_dict())

        return result

    # შლის ტრანზაქციას მითითებული ინდექსით.
    # თუ ფაილში შენახვა ვერ მოხერხდა, წაშლილ ჩანაწერს აბრუნებს.
    def delete_transaction(self, index):
        if 0 <= index < len(self.transactions):
            transaction = self.transactions.pop(index)

            if save_transactions(self.get_transactions_data()):
                return True

            self.transactions.insert(index, transaction)

        return False

    # ცვლის ტრანზაქციის თანხას, კატეგორიასა და კომენტარს.
    # წარუმატებელი შენახვის შემთხვევაში ძველ მონაცემებს აღადგენს.
    def update_transaction(self, index, amount, category, comment):
        if 0 <= index < len(self.transactions):
            transaction = self.transactions[index]

            old_amount = transaction.amount
            old_category = transaction.category
            old_comment = transaction.comment

            transaction.amount = amount
            transaction.category = category
            transaction.comment = comment

            if save_transactions(self.get_transactions_data()):
                return True

            transaction.amount = old_amount
            transaction.category = old_category
            transaction.comment = old_comment

        return False

    # ფილტრავს ტრანზაქციებს კატეგორიის, თარიღის ან ტიპის მიხედვით.
    # თუ რომელიმე პარამეტრი None-ია, მისი შემოწმება არ ხდება.
    def filter_transactions(self, category=None, date=None,
                            transaction_type=None):
        result = []

        for transaction in self.transactions:
            matches = True

            if category is not None:
                if transaction.category.lower() != category.lower():
                    matches = False

            if date is not None:
                if transaction.date != date:
                    matches = False

            if transaction_type is not None:
                if transaction.transaction_type != transaction_type:
                    matches = False

            if matches:
                result.append(transaction)

        return result

    # ითვლის მთლიან შემოსავალს, გასავალსა და ბალანსს.
    # სურვილის შემთხვევაში შეუძლია მხოლოდ გადაცემული სიის შეჯამება.
    def summary(self, transactions=None):
        if transactions is None:
            transactions = self.transactions

        income = 0
        expense = 0

        for transaction in transactions:
            if transaction.transaction_type == "income":
                income += transaction.amount

            elif transaction.transaction_type == "expense":
                expense += transaction.amount

        income = round(income, 2)
        expense = round(expense, 2)
        balance = round(income - expense, 2)

        return income, expense, balance

    # ითვლის შემოსავალსა და გასავალს თითოეული კატეგორიისთვის.
    # შედეგს აბრუნებს ლექსიკონის სახით.
    def category_summary(self):
        result = {}

        for transaction in self.transactions:
            category = transaction.category

            if category not in result:
                result[category] = {
                    "income": 0,
                    "expense": 0
                }

            if transaction.transaction_type == "income":
                result[category]["income"] += transaction.amount

            elif transaction.transaction_type == "expense":
                result[category]["expense"] += transaction.amount

        return result

    # აბრუნებს მხოლოდ მითითებული თვის ტრანზაქციებს.
    # არასწორი თარიღის შემთხვევაში continue გადადის შემდეგ ჩანაწერზე.
    def monthly_transactions(self, month):
        result = []

        for transaction in self.transactions:
            try:
                date = datetime.strptime(
                    transaction.date, "%Y-%m-%d"
                )

                transaction_month = date.strftime("%m.%Y")

                if transaction_month == month:
                    result.append(transaction)

            except ValueError:
                continue

        return result

    # ადგენს ან ცვლის კატეგორიის თვიურ ლიმიტს.
    # თუ შენახვა ვერ მოხერხდა, აღადგენს ძველ ბიუჯეტებს.
    def set_budget(self, category, amount):
        old_budgets = self.budgets.copy()

        self.budgets[category] = amount

        if save_budgets(self.budgets):
            return True

        self.budgets = old_budgets
        return False

    # პოულობს მითითებული კატეგორიის ლიმიტს.
    # კატეგორიის სახელის შედარებისას ასოების ზომას არ ითვალისწინებს.
    def budget_for(self, category):
        for name, limit in self.budgets.items():
            if name.lower() == category.lower():
                return limit

        return None

    # ითვლის კონკრეტულ კატეგორიაში მითითებული თვის მთლიან გასავალს.
    # შედეგს აბრუნებს ორ ათწილადამდე დამრგვალებულს.
    def category_expense_for_month(self, category, month):
        total = 0

        transactions = self.monthly_transactions(month)

        for transaction in transactions:
            if transaction.category.lower() == category.lower():
                if transaction.transaction_type == "expense":
                    total += transaction.amount

        return round(total, 2)