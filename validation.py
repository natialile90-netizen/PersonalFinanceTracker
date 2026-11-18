from datetime import datetime


# ამოწმებს მომხმარებლის მიერ შეყვანილ თანხას.
# თანხა უნდა იყოს რიცხვი და ნულზე მეტი.
# არასწორი მონაცემის შემთხვევაში შეყვანა მეორდება.
def read_amount(message="შეიყვანეთ თანხა: "):
    while True:
        try:
            amount = float(input(message))

            if amount > 0:
                return amount

            print("თანხა უნდა იყოს ნულზე მეტი.")

        except ValueError:
            print("შეიყვანეთ სწორი რიცხვი.")


# ამოწმებს ტექსტურ მონაცემს, მაგალითად კატეგორიის სახელს.
# strip() აშორებს ზედმეტ გამოტოვებებს და ცარიელ ტექსტს არ იღებს.
def read_text(message):
    while True:
        text = input(message).strip()

        if text:
            return text

        print("ველი არ უნდა იყოს ცარიელი.")


# ამოწმებს, რომ შეყვანილი მნიშვნელობა იყოს მთელი რიცხვი
# და მოთავსდეს minimum და maximum საზღვრებს შორის.
def read_number(message, minimum, maximum):
    while True:
        try:
            number = int(input(message))

            if minimum <= number <= maximum:
                return number

            print("აირჩიეთ რიცხვი", minimum, "-დან", maximum, "-მდე.")

        except ValueError:
            print("შეიყვანეთ მთელი რიცხვი.")


# ამოწმებს თარიღს ფორმატით დღე.თვე.წელი.
# სწორ თარიღს გარდაქმნის ფორმატში წელი-თვე-დღე,
# რათა პროგრამაში ყველა თარიღი ერთნაირად შეინახოს.
def read_date():
    while True:
        date = input("შეიყვანეთ თარიღი (დღე.თვე.წელი): ")

        try:
            valid_date = datetime.strptime(date, "%d.%m.%Y")
            return valid_date.strftime("%Y-%m-%d")

        except ValueError:
            print("თარიღის არასწორი ფორმატი.")


# ამოწმებს მომხმარებლის მიერ შეყვანილ თვესა და წელს.
# strptime ამოწმებს ფორმატს, strftime კი აბრუნებს თვე.წელი ფორმატს.
def read_month():
    while True:
        month = input("შეიყვანეთ თვე (თვე.წელი): ")

        try:
            valid_month = datetime.strptime(month, "%m.%Y")
            return valid_month.strftime("%m.%Y")

        except ValueError:
            print("თვე არასწორად არის მითითებული.")


# ტრანზაქციის ინგლისურ ტიპს გარდაქმნის ქართულ დასახელებად.
# გამოიყენება მომხმარებლისთვის ინფორმაციის ქართულად საჩვენებლად.
def type_name(transaction_type):
    if transaction_type == "income":
        return "შემოსავალი"

    elif transaction_type == "expense":
        return "გასავალი"

    return transaction_type


# შენახულ თარიღს წელი-თვე-დღე ფორმატიდან
# გარდაქმნის დღე.თვე.წელი ფორმატში ეკრანზე გამოსატანად.
# თუ გარდაქმნა ვერ მოხერხდა, აბრუნებს საწყის მნიშვნელობას.
def normalize_date(date):
    try:
        valid_date = datetime.strptime(date, "%Y-%m-%d")
        return valid_date.strftime("%d.%m.%Y")

    except ValueError:
        return date
