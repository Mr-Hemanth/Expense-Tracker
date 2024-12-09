from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'expenses.db'
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()
@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    return render_template('index.html', expenses=expenses)


@app.route('/add', methods=['GET', 'POST'])

def add_expense():
    if request.method == 'POST':
        title = request.form['title']
        amount = request.form['amount']
        date = request.form['date']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (title, amount, date) VALUES (?, ?, ?)",
                       (title, amount, date))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_expense.html')
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
