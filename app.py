from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS todos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 email TEXT NOT NULL,
                 address TEXT NOT NULL,
                 pin TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    search_query = request.args.get('search', '')  # Get search parameter from URL
    
    if search_query:
        # Use LIKE for partial matching and % for wildcards
        c.execute("SELECT * FROM todos WHERE name LIKE ?", ('%' + search_query + '%',))
    else:
        c.execute("SELECT * FROM todos")
    
    todos = c.fetchall()
    conn.close()
    return render_template('index.html', todos=todos, search_query=search_query)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        pin = request.form['pin']
        
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("INSERT INTO todos (name, email, address, pin) VALUES (?, ?, ?, ?)",
                  (name, email, address, pin))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        pin = request.form['pin']
        
        c.execute("UPDATE todos SET name=?, email=?, address=?, pin=? WHERE id=?",
                  (name, email, address, pin, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    c.execute("SELECT * FROM todos WHERE id=?", (id,))
    todo = c.fetchone()
    conn.close()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)