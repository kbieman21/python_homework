# Task 1: Complex JOINs with Aggregation
import os
import sqlite3

# Define path to the lesson database
db_path = '../db/lesson.db'

def fetch_top_orders():
    conn = None
    try:
        # 1. Open the database connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 2. Define the SQL statement
        query = '''
            SELECT 
                orders.order_id, 
                SUM(products.price * line_items.quantity) AS total_price
            FROM orders
            JOIN line_items ON orders.order_id = line_items.order_id
            JOIN products ON line_items.product_id = products.product_id
            GROUP BY orders.order_id
            ORDER BY orders.order_id
            LIMIT 5;
        '''
        
        # 3. Issue the SQL statement
        cursor.execute(query)
        results = cursor.fetchall()
        
        # 4. Print out the results cleanly
        print("Order ID | Total Price")
        print("-" * 23)
        for row in results:
            print(f"Order {row[0]:<3} | ${row[1]:,.2f}")
     
    except sqlite3.Error as e:
        print(f"A database error occurred: {e}")
        
    finally:
        # 5. Close the database connection safely
        if conn:
            conn.close()
            print("\nDatabase connection closed.")



# Task 2: Understanding Subqueries
def fetch_customer_averages():
    conn = None
    try:
        # 1. Open the database connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 2. Define the Subquery statement
        query = '''
            SELECT 
                customers.customer_name,
                AVG(order_totals.total_price) AS average_total_price
            FROM customers
            LEFT JOIN (
                SELECT 
                    orders.customer_id AS customer_id_b,
                    SUM(products.price * line_items.quantity) AS total_price
                FROM orders
                JOIN line_items ON orders.order_id = line_items.order_id
                JOIN products ON line_items.product_id = products.product_id
                GROUP BY orders.order_id
            ) AS order_totals ON customers.customer_id = order_totals.customer_id_b
            GROUP BY customers.customer_id;
        '''
        
        # 3. Issue the SQL statement
        cursor.execute(query)
        results = cursor.fetchall()
        
        # 4. Print out the results cleanly
        print("\n=== Task 2: Customer Average Order Spending ===")
        print(f"{'Customer Name':<20} | {'Avg Order Price':<15}")
        print("-" * 38)
        for row in results:
            # Handle customers who haven't placed an order yet (their avg will be None)
            avg_price = row[1] if row[1] is not None else 0.0
            print(f"{row[0]:<20} | ${avg_price:,.2f}")
            
    except sqlite3.Error as e:
        print(f"A database error occurred in Task 2: {e}")
    finally:
        # 5. Close the database connection safely
        if conn:
            conn.close()
            print("\nDatabase connection closed.")


# Task 3: An Insert Transaction Based on Data
def create_perez_transaction():
    conn = None
    try:
        # 1. Connect and immediately turn on Foreign Key safety checks
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()

        # 2. Collect IDs from the database using SELECT statements
        cursor.execute("SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons'")
        cust_row = cursor.fetchone()
        
        cursor.execute("SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name = 'Harris'")
        emp_row = cursor.fetchone()

        # Find the 5 least expensive product IDs
        cursor.execute("SELECT product_id FROM products ORDER BY price ASC LIMIT 5")
        product_rows = cursor.fetchall()

        if not cust_row or not emp_row or not product_rows:
            print("\nError: Required customer, employee, or product records missing from lesson.db.")
            return

        customer_id = cust_row[0]
        employee_id = emp_row[0]
        product_ids = [row[0] for row in product_rows]

        # 3. Open explicit transaction block
        conn.execute("BEGIN TRANSACTION;")

        # Insert the main order and catch the auto-generated ID using RETURNING
        cursor.execute('''
            INSERT INTO orders (customer_id, employee_id, date) 
            VALUES (?, ?, DATE('now')) 
            RETURNING order_id
        ''', (customer_id, employee_id))
        
        new_order_id = cursor.fetchone()[0]

        # Insert all 5 line items for this single order_id
        for prod_id in product_ids:
            cursor.execute('''
                INSERT INTO line_items (order_id, product_id, quantity) 
                VALUES (?, ?, 10)
            ''', (new_order_id, prod_id))

        # 4. Save everything together safely
        conn.commit()
        print(f"\n=== Task 3: Transaction Successful! Created Order ID {new_order_id} ===")

        # 5. SELECT JOIN to print the finalized receipt
        cursor.execute('''
            SELECT line_items.line_item_id, line_items.quantity, products.product_name
            FROM line_items
            JOIN products ON line_items.product_id = products.product_id
            WHERE line_items.order_id = ?
        ''', (new_order_id,))
        
        receipt_items = cursor.fetchall()
        print(f"{'Line Item ID':<12} | {'Qty':<4} | {'Product Name':<25}")
        print("-" * 47)
        for row in receipt_items:
            print(f"{row[0]:<12} | {row[1]:<4} | {row[2]:<25}")

    except sqlite3.Error as e:
        print(f"\nDatabase error during transaction: {e}")
        if conn:
            conn.execute("ROLLBACK;")
            print("Transaction rolled back safely.")
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")
            

# Task 4: Aggregation with HAVING
def fetch_top_employees():
    conn = None
    try:
        # 1. Open the database connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 2. Define the SQL statement with HAVING clause
        query = '''
            SELECT 
                employees.employee_id, 
                employees.first_name, 
                employees.last_name, 
                COUNT(orders.order_id) AS order_count
            FROM employees
            JOIN orders ON employees.employee_id = orders.employee_id
            GROUP BY employees.employee_id
            HAVING order_count > 5;
        '''
        
        # 3. Issue the SQL statement
        cursor.execute(query)
        results = cursor.fetchall()
        
        # 4. Print results cleanly with aligned formatting
        print("\n=== Task 4: Employees With More Than 5 Orders ===")
        print(f"{'ID':<4} | {'First Name':<12} | {'Last Name':<12} | {'Orders':<6}")
        print("-" * 45)
        for row in results:
            print(f"{row[0]:<4} | {row[1]:<12} | {row[2]:<12} | {row[3]:<6}")
            
    except sqlite3.Error as e:
        print(f"A database error occurred in Task 4: {e}")
    finally:
        # 5. Close the database connection
        if conn:
            conn.close()
            print("\nDatabase connection closed.")
if __name__ == '__main__':
    fetch_top_orders()
    fetch_customer_averages()
    create_perez_transaction()
    fetch_top_employees()
