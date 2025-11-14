import argparse
import sqlite3
import sys
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parent / 'ecom.db'

def execute_query(conn, sql):
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        if cursor.description:
            rows = cursor.fetchall()
            headers = [col[0] for col in cursor.description]
            return headers, rows
        else:
            conn.commit()
            return None, f"Query executed successfully; {cursor.rowcount} row(s) affected."
    finally:
        cursor.close()

def format_results(headers, rows):
    if not rows:
        return "No rows returned."
    widths = [len(h) for h in headers]
    for row in rows:
        widths = [max(widths[i], len(str(value))) for i, value in enumerate(row)]
    header_line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    separator = "-+-".join('-' * widths[i] for i in range(len(headers)))
    data_lines = [" | ".join(str(value).ljust(widths[i]) for i, value in enumerate(row)) for row in rows]
    return "\n".join([header_line, separator] + data_lines)

def read_sql_from_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def interactive_loop(conn):
    print("Enter SQL statements to run against the database. Type 'exit' to quit.")
    while True:
        try:
            sql = input('sql> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nExiting.')
            break
        if not sql:
            continue
        if sql.lower() in {'exit', 'quit'}:
            break
        try:
            headers, result = execute_query(conn, sql)
            if headers:
                print(format_results(headers, result))
            else:
                print(result)
        except sqlite3.Error as e:
            print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Run SQL queries against ecom.db')
    parser.add_argument('--db', default=str(DEFAULT_DB), help='Path to SQLite database (default: ecom.db next to this script)')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--query', help='SQL query string to execute')
    group.add_argument('--file', help='Path to a .sql file containing the query to execute')
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        sys.exit(f"Database not found: {db_path}")

    conn = sqlite3.connect(db_path)
    try:
        if args.query:
            headers, result = execute_query(conn, args.query)
            if headers:
                print(format_results(headers, result))
            else:
                print(result)
        elif args.file:
            sql = read_sql_from_file(args.file)
            headers, result = execute_query(conn, sql)
            if headers:
                print(format_results(headers, result))
            else:
                print(result)
        else:
            interactive_loop(conn)
    finally:
        conn.close()

if __name__ == '__main__':
    main()
