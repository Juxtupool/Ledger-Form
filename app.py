from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            number INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home route
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries')
    entries = conn.execute('SELECT * FROM entries ORDER BY id DESC').fetchall()  #cursor.fetchall() (for acending order)
    conn.close()
    return render_template('index.html', entries=entries)

# Add entry route
@app.route('/add', methods=['POST'])
def add_entry():
    text = request.form['text']
    number = request.form['number']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO entries (text, number) VALUES (?, ?)', (text, number))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Edit entry route
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    if request.method == 'POST':
        text = request.form['text']
        number = request.form['number']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE entries SET text = ?, number = ? WHERE id = ?', (text, number, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM entries WHERE id = ?', (id,))
        entry = cursor.fetchone()
        conn.close()
        return render_template('edit.html', entry=entry)

# Delete entry route
@app.route('/delete/<int:id>', methods=['POST'])
def delete_entry(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM entries WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
