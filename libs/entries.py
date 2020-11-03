class Entry:

    dict_entries = {
        "Fruit": 22,
        "Plain": 14,
        "Cinnamon": 4,
        "Cheese": 21
    }

    def new_entry(self, deal, price):
        self.dict_entries[deal] = price


entry = Entry()

deal = "Apfel"
price = 2
entry.new_entry(deal, price)

print(entry.dict_entries)
