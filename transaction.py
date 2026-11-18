from datetime import datetime

# Transaction კლასში ინახება თანხა, კატეგორია, ტიპი, თარიღი და კომენტარი.
class Transaction:


    def __init__(self, amount, category, transaction_type, date=None, comment=""):
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type

        # თუ თარიღი არ არის მითითებული, ავტომატურად ინახება დღევანდელი თარიღი.
        # წინააღმდეგ შემთხვევაში გამოიყენება გადმოცემული თარიღი.
        if date is None:
            self.date = datetime.now().strftime("%Y-%m-%d")
        else:
            self.date = date

        # კომენტარი არასავალდებულოა და შეიძლება ცარიელიც იყოს.
        self.comment = comment

    # to_dict მეთოდი ობიექტის მონაცემებს ლექსიკონად გარდაქმნის,რომ ტრანზაქციის მონაცემები JSON ფაილში შევინახოთ.
    # return აბრუნებს ლექსიკონს შესაბამისი გასაღებებითა და მნიშვნელობებით.
    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "transaction_type": self.transaction_type,
            "date": self.date,
            "comment": self.comment
        }
