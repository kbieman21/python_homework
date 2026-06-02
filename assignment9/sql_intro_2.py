# Task 5: Read Data into a DataFrame

import sqlite3
import pandas as pd

# Define path to the lesson database
db_path = '../db/lesson.db'

try:
    # 1. Connect to the database
    conn = sqlite3.connect(db_path)
    
    # 2. Write the SQL JOIN query
    query = '''
        SELECT 
            line_items.line_item_id, 
            line_items.quantity, 
            line_items.product_id, 
            products.product_name, 
            products.price 
        FROM line_items
        JOIN products ON line_items.product_id = products.product_id
    '''
    
    # 3. Read SQL data directly into a Pandas DataFrame
    df = pd.read_sql_query(query, conn)
    
    print("--- Step 1: First 5 lines of the initial DataFrame ---")
    print(df.head(5))
    print("\n" + "="*50 + "\n")

    # 4. Add the 'total' calculated column
    df['total'] = df['quantity'] * df['price']
    
    print("--- Step 2: First 5 lines with the 'total' column added ---")
    print(df.head(5))
    print("\n" + "="*50 + "\n")

    # 5. Group by product_id and apply the count, total, and first aggregations
    summary_df = df.groupby('product_id').agg({
        'line_item_id': 'count',
        'total': 'sum',
        'product_name': 'first'
    })
    
    print("--- Step 3: First 5 lines after groupby and agg ---")
    print(summary_df.head(5))
    print("\n" + "="*50 + "\n")

    # 6. Sort the resulting DataFrame by product_name
    summary_df = summary_df.sort_values(by='product_name')
    
    # 7. Write the summarized data to a CSV file in the current directory
    csv_filename = 'order_summary.csv'
    summary_df.to_csv(csv_filename, index=True)
    print(f"--- Step 4: Successfully wrote sorted data to '{csv_filename}' ---")

except sqlite3.Error as e:
    print(f"A database error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    if 'conn' in locals() and conn:
        conn.close()
        print("Database connection closed.")
