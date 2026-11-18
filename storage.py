import json

# JSON ფაილების სახელები, სადაც ინახება ტრანზაქციები და ბიუჯეტები
TRANSACTIONS_FILE = "transactions.json"
BUDGETS_FILE = "budgets.json"


# მონაცემების JSON ფაილში შენახვა.
# ფაილი იხსნება ჩაწერის რეჟიმში და მონაცემები ინახება ქართულ ტექსტთან ერთად.
# წარმატების შემთხვევაში აბრუნებს True-ს, შეცდომისას — False-ს.
def save_data(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return True

    except OSError:
        print("მონაცემების შენახვისას მოხდა შეცდომა.")
        return False


# JSON ფაილიდან შენახული მონაცემების წაკითხვა.
# თუ ფაილი არ არსებობს ან არასწორი ფორმატი აქვს,
# ფუნქცია აბრუნებს წინასწარ განსაზღვრულ default მნიშვნელობას.
def load_data(filename, default):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        return default

    except json.JSONDecodeError:
        print("JSON ფაილის ფორმატი არასწორია.")
        return default

    except OSError:
        print("ფაილის წაკითხვისას მოხდა შეცდომა.")
        return default


# ტრანზაქციების შენახვა transactions.json ფაილში
def save_transactions(transactions):
    return save_data(TRANSACTIONS_FILE, transactions)


# ტრანზაქციების ჩატვირთვა JSON ფაილიდან.
# თუ ფაილი არ არსებობს, ბრუნდება ცარიელი სია.
def load_transactions():
    return load_data(TRANSACTIONS_FILE, [])


# კატეგორიების ბიუჯეტების შენახვა budgets.json ფაილში
def save_budgets(budgets):
    return save_data(BUDGETS_FILE, budgets)


# ბიუჯეტების ჩატვირთვა JSON ფაილიდან.
# თუ ფაილი არ არსებობს, ბრუნდება ცარიელი ლექსიკონი.
def load_budgets():
    return load_data(BUDGETS_FILE, {})