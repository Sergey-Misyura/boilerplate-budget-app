class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __repr__(self):     # string to print Category
        self.tabl = f'{self.name:*^30s}' + '\n'
        for elem in self.ledger:
            self.tabl = self.tabl + f"{elem['description']:<23.23s}" + f"{elem['amount']:>7.2f}"+'\n'
        self.tabl = self.tabl + 'Total: ' + f"{self.get_balance():.2f}"
        return self.tabl

    def deposit(self, amount, description=''):      # deposit entry
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=''):     # withdraws
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False

    def get_balance(self):  # return balance of category
        self.balance = 0
        for i in self.ledger:
            self.balance += i['amount']
        return self.balance

    def transfer(self, amount,  budget_category):   # transfer between categories
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {budget_category.name}')
            budget_category.deposit(amount, f'Transfer from {self.name}')
            return True
        else:
            return False

    def check_funds(self, amount):      # balance check
        if amount > self.get_balance():
            return False
        else:
            return True

    def spent_sum(self):    # sum of withdraws
        return sum([i['amount'] for i in self.ledger if i['amount'] < 0])

def create_spend_chart(categories):
    total_spent = sum([i.spent_sum() for i in categories])      # sum of withdraws in all Categories
    proc_spent_cat = [i.spent_sum()/total_spent*100 for i in categories]    # list of percent withdraws

    percentage = 'Percentage spent by category\n'
    for proc in range(100, -1, -10):            # draw a chart
        percentage += f'{str(proc):>3.3s}'+'|'
        for i in proc_spent_cat:
            if i >=proc:
                percentage += " o "
            else:
                percentage += "   "
        percentage += ' \n'

    percentage += ' ' * 4 + '-' + '---' * len(categories) +'\n'  # add ----- line to chart

    max_ln = 0      # defining the maximum length of categories
    for cat in categories:
        if len(cat.name) > max_ln:
            max_ln = len(cat.name)

    categ = ''      # adding category names to chart
    for let in range(max_ln):
        categ +=' ' * 4
        for i in categories:
            try:
                categ +=' '+i.name[let]+' '
            except Exception:
                categ +=' '*3
        categ +=' \n'
    categ = categ.rstrip('\n')
    return percentage+categ