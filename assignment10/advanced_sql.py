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


if __name__ == '__main__':
    #fetch_top_orders()
    fetch_customer_averages()
