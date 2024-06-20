import sqlite3


class DatabaseCarts:
    def __init__(self, path_to_db="allData.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        with sqlite3.connect(self.path_to_db) as connection:
            # connection.set_trace_callback(logger)
            cursor = connection.cursor()
            data = None
            cursor.execute(sql, parameters)
            if commit:
                connection.commit()
            if fetchall:
                data = cursor.fetchall()
            if fetchone:
                data = cursor.fetchone()
        return data

    def create_table_cart(self):
        sql = """
        CREATE TABLE Carts (
            user_id INT,
            product_id TEXT,
            product_name TEXT,
            product_price INT,
            count INT
            );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def formatArgs(sql, parameters: dict):
        if len(parameters) == 1:
            bat = " AND "
        else:
            bat = ", "
        sql += bat.join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_product_cart(self,user_id: int, product_id: str, product_name: str, product_price: str, count: int):
        sql = """
        INSERT INTO Carts(user_id, product_id, product_name, product_price, count) 
        VALUES(?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, product_id, product_name, product_price, count), commit=True)

    def update_cart_info(self, user_id, product_id, **kwargs):
        sql = "UPDATE Carts SET "
        sql, parameters = self.formatArgs(sql, kwargs)
        sql += " WHERE user_id = ? AND product_id = ?;"
        parameters += (user_id, product_id)
        return self.execute(sql, parameters=parameters, commit=True)

    def select_user_cart(self, user_id: int, **kwargs):
        sql = f"SELECT * FROM Carts WHERE user_id = '{user_id}'"
        sql, parameters = self.formatArgs(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_all_cart(self):
        sql = f"SELECT * FROM Carts"
        return self.execute(sql, fetchall=True)

    def delete_cart_product(self, user_id,  product_id):
        self.execute(sql=f"DELETE FROM Carts WHERE user_id = '{user_id}' AND product_id = '{product_id}'", commit=True)


# def logger(statement):
#     print(f"""
# _____________________________________________________
# Executing:
# {statement}
# _____________________________________________________
# """)

# ALTER TABLE Users ADD user_wallet INT DEFAULT 0
