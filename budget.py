from math import floor
from itertools import zip_longest


class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def get_balance(self):
        return sum([transaction["amount"] for transaction in self.ledger])

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if not self.check_funds(amount):
            return False

        self.deposit(-amount, description)
        return True

    def transfer(self, amount, category):
        if not self.check_funds(amount):
            return False

        self.withdraw(amount, f"Transfer to {category.name}")
        category.deposit(amount, f"Transfer from {self.name}")
        return True

    def __str__(self):
        name_len = len(self.name)
        num_stars = 30 - name_len

        title = "*" * (num_stars // 2) + self.name + "*" * (num_stars - num_stars // 2)

        ledger_lines = []
        for trans in self.ledger:
            desc = trans["description"][:23]
            amount = f'{trans["amount"]:.2f}'
            spaces = " " * (30 - len(desc) - len(amount))

            ledger_lines.append(desc + spaces + amount)

        total = f"Total: {self.get_balance():.2f}"

        return "\n".join([title, *ledger_lines, total])


def create_spend_chart(categories):
    def withdrawal_filter(trans):
        return trans["amount"] < 0

    data = [
        {
            "name": category.name,
            "spent": sum(
                [
                    trans["amount"]
                    for trans in [*filter(withdrawal_filter, category.ledger)]
                ]
            ),
        }
        for category in categories
    ]

    total_spent = sum([category["spent"] for category in data])

    # Calculate percentage of total spend for each category rounded down to nearest 10
    for category in data:
        category["percent"] = floor(10 * category["spent"] / total_spent) * 10

    y_axis = [100 - x for x in range(0, 110, 10)]

    rows = ["Percentage spent by category"]

    for percent in y_axis:
        dots = ["o" if category["percent"] >= percent else " " for category in data]

        rows.append(
            " " * (3 - len(str(percent))) + str(percent) + "| " + "  ".join(dots) + "  "
        )

    rows.append(" " * 4 + "-" * (len(rows[-1]) - 4))

    vertical_names = zip_longest(
        *[category["name"] for category in data], fillvalue=" "
    )

    for row in vertical_names:
        rows.append(" " * 5 + "  ".join(row) + "  ")

    return "\n".join(rows)

