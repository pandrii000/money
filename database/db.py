import sqlite3


SQL_CREATE_TABLE_BALANCES = \
'''
CREATE TABLE BALANCES
(
    BALANCE_ID INTEGER PRIMARY KEY ASC,
    BALANCE_NAME VARCHAR(100),
    BALANCE_AMOUNT DECIMAL
);
'''

SQL_CREATE_TABLE_CATEGORIES = \
'''
CREATE TABLE CATEGORIES
(
    CATEGORY_ID INTEGER PRIMARY KEY ASC,
    CATEGORY_NAME VARCHAR(100),
    CATEGORY_IS_INCOME BOOLEAN,
    CATEGORY_PARENT_ID INTEGER OPTIONAL,
    FOREIGN KEY(CATEGORY_PARENT_ID) REFERENCES CATEGORIES(CATEGORY_ID)
);
'''

SQL_CREATE_TABLE_TRANSACTIONS = \
'''
CREATE TABLE TRANSACTIONS
(
    TRANSACTION_ID INTEGER PRIMARY KEY ASC,
    TRANSACTION_BALANCE_ID INTEGER,
    TRANSACTION_DATE DATE,
    TRANSACTION_AMOUNT DECIMAL,
    TRANSACTION_IS_INCOME BOOLEAN,
    TRANSACTION_CATEGORY_ID INTEGER,
    TRANSACTION_DESCRIPTION VARCHAR(500),
    FOREIGN KEY(TRANSACTION_BALANCE_ID) REFERENCES BALANCES(BALANCE_ID),
    FOREIGN KEY(TRANSACTION_CATEGORY_ID) REFERENCES CATEGORIES(CATEGORY_ID)
);
'''

BALANCE_KEYS = ['balance_id', 'balance_name', 'balance_amount']
CATEGORY_KEYS = ['category_id', 'category_name', 'category_is_income', 'category_parent_id']
TRANSACTION_KEYS = [
    'transaction_id',
    'transaction_balance_id',
    'transaction_date',
    'transaction_amount',
    'transaction_is_income',
    'transaction_category_id',
    'transaction_description',
]


class MoneyDB:
    def __init__(self, filename):
        self.filename = filename

    def create_db(self):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()

        curs.execute("DROP TABLE IF EXISTS BALANCES")
        curs.execute("DROP TABLE IF EXISTS CATEGORIES")
        curs.execute("DROP TABLE IF EXISTS TRANSACTIONS")

        curs.execute(SQL_CREATE_TABLE_BALANCES)
        curs.execute(SQL_CREATE_TABLE_CATEGORIES)
        curs.execute(SQL_CREATE_TABLE_TRANSACTIONS)

        conn.commit()
        conn.close()

    def insert_balance(self, name, amount):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()

        curs.execute(
            "INSERT INTO BALANCES (BALANCE_NAME, BALANCE_AMOUNT) VALUES (?, ?)",
            (name, amount))

        conn.commit()
        conn.close()

    def insert_category(self, name, is_income, category_parent_id=None):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()

        curs.execute((
            "INSERT INTO CATEGORIES (CATEGORY_NAME, CATEGORY_IS_INCOME, CATEGORY_PARENT_ID)" +
            "VALUES (?, ?, ?)"),
            (name, is_income, category_parent_id))

        conn.commit()
        conn.close()

    def insert_transaction(self, balance_id, date, amount, is_income, category_id, description):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()

        curs.execute((
            "INSERT INTO TRANSACTIONS (TRANSACTION_BALANCE_ID, TRANSACTION_DATE, " +
            "TRANSACTION_AMOUNT, TRANSACTION_IS_INCOME, TRANSACTION_CATEGORY_ID, TRANSACTION_DESCRIPTION" +
            ") VALUES (?, ?, ?, ?, ?, ?)"),
            (balance_id, date, amount, is_income, category_id, description))

        conn.commit()
        conn.close()

    def get_balances(self):
        conn = sqlite3.connect(self.filename) 
        curs = conn.cursor()

        curs.execute('SELECT t.BALANCE_ID, t.BALANCE_NAME, t.BALANCE_AMOUNT FROM BALANCES t')
        balances = [dict(zip(BALANCE_KEYS, values)) for values in curs.fetchall()]

        conn.commit()
        conn.close()

        return balances

    def get_categories(self):
        conn = sqlite3.connect(self.filename) 
        curs = conn.cursor()

        curs.execute(
        '''
        SELECT t.CATEGORY_ID, t.CATEGORY_NAME, t.CATEGORY_IS_INCOME, t.CATEGORY_PARENT_ID FROM CATEGORIES t
        ''')
        categories = [dict(zip(CATEGORY_KEYS, values)) for values in curs.fetchall()]

        conn.commit()
        conn.close()

        return categories

    def get_transactions(self):
        conn = sqlite3.connect(self.filename) 
        curs = conn.cursor()

        curs.execute(
        '''
        SELECT
            t.TRANSACTION_ID,
            t.TRANSACTION_BALANCE_ID,
            t.TRANSACTION_DATE,
            t.TRANSACTION_AMOUNT,
            t.TRANSACTION_IS_INCOME,
            t.TRANSACTION_CATEGORY_ID,
            t.TRANSACTION_DESCRIPTION
        FROM TRANSACTIONS t
        '''
        )
        transactions = [dict(zip(TRANSACTION_KEYS, values)) for values in curs.fetchall()]

        conn.commit()
        conn.close()

        return transactions

    def get_transactions_by_balance_name(self, name):
        balance_id = self.get_balance_by_name(name)['balance_id']

        conn = sqlite3.connect(self.filename) 
        curs = conn.cursor()

        curs.execute(
        '''
        SELECT
            t.TRANSACTION_ID,
            t.TRANSACTION_BALANCE_ID,
            t.TRANSACTION_DATE,
            t.TRANSACTION_AMOUNT,
            t.TRANSACTION_IS_INCOME,
            t.TRANSACTION_CATEGORY_ID,
            t.TRANSACTION_DESCRIPTION
        FROM TRANSACTIONS t
        WHERE t.TRANSACTION_BALANCE_ID={}
        '''.format(balance_id)
        )
        transactions = [dict(zip(TRANSACTION_KEYS, values)) for values in curs.fetchall()]

        conn.commit()
        conn.close()

        return transactions

    def get_balance_by_id(self, balance_id):
        conn = sqlite3.connect(self.filename) 
        curs = conn.cursor()

        curs.execute(
        '''
        SELECT t.BALANCE_ID, t.BALANCE_NAME, t.BALANCE_AMOUNT FROM BALANCES t WHERE t.BALANCE_ID=\'{name}\'
        '''.format(name=balance_id))
        db_output = curs.fetchone()

        if db_output is None:
            balance = None
        else:
            balance = dict(zip(BALANCE_KEYS, db_output))

        conn.commit()
        conn.close()

        return balance

    def get_balance_by_name(self, name):
        conn = sqlite3.connect(self.filename) 
        curs = conn.cursor()

        curs.execute(
        '''
        SELECT t.BALANCE_ID, t.BALANCE_NAME, t.BALANCE_AMOUNT FROM BALANCES t WHERE t.BALANCE_NAME=\'{name}\'
        '''.format(name=name))
        db_output = curs.fetchone()

        if db_output is None:
            balance = None
        else:
            balance = dict(zip(BALANCE_KEYS, db_output))

        conn.commit()
        conn.close()

        return balance

    def get_category_by_name(self, name):
        conn = sqlite3.connect(self.filename) 
        curs = conn.cursor()

        curs.execute('''
            SELECT t.CATEGORY_ID, t.CATEGORY_NAME, t.CATEGORY_IS_INCOME, t.CATEGORY_PARENT_ID
            FROM CATEGORIES t
            WHERE t.CATEGORY_NAME=\'{name}\'
        '''.format(name=name))
        db_output = curs.fetchone()

        if db_output is None:
            category = None
        else:
            category = dict(zip(CATEGORY_KEYS, db_output))

        conn.commit()
        conn.close()

        return category

    def update_balance(self, name):
        transactions = self.get_transactions_by_balance_name(name)
        amount = 0
        for t in transactions:
            sign = 1 if t['transaction_is_income'] else -1
            amount += sign * t['transaction_amount']

        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()

        curs.execute('''
            UPDATE BALANCES
            SET BALANCE_AMOUNT = {}
            WHERE BALANCE_NAME = \'{}\';
        '''.format(amount, name))

        conn.commit()
        conn.close()

    def update_balances(self):
        balances = self.get_balances()
        for balance in balances:
            self.update_balance(balance['balance_name'])


if __name__ == '__main__':
    db = MoneyDB('./database/money.db')
    db.create_db()

    db.insert_balance('UAH', 23.4)
    db.insert_balance('USD', 3.4)
    print(db.get_balance_by_name('UAH'))
    print(db.get_balance_by_name('USD'))
    print(db.get_balance_by_name('SD'))
    print(db.get_balances())

    db.insert_category('Eating Outside', False)
    print(db.get_category_by_name('Eating Outside'))

    db.insert_category('Food', False)
    db.insert_category('Salary', True)
    print(db.get_categories())

    db.insert_transaction(1, '2021-08-22 16:44', 20.2, False, 0, 'Some txt')
    db.insert_transaction(1, '2021-08-23 16:44', 24.2, True, 0, 'Some txt')
    db.insert_transaction(2, '2021-08-24 16:44', 24.2, True, 0, 'Some txt')
    print(db.get_transactions())

    print(db.get_transactions_by_balance_name('UAH'))

    print(db.update_balance('UAH'))
    print(db.update_balances())
    print(db.get_balances())
