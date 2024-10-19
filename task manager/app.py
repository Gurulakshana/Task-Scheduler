from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345678',  # Change this to your MySQL password
    'database': 'task_schedulers'
}

def connect_db():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            return conn
        else:
            print("Failed to connect to database")
            return None
    except Error as e:
        print(f"Database connection error: {e}")
        return None

# Home route: display tasks
@app.route('/')
def index():
    conn = connect_db()
    if not conn:
        flash("Database connection failed", "danger")
        return render_template('index.html', tasks=[])

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks where status='yet to do' or status='ongoing' order by due_date ASC,status desc;")
    tasks = cursor.fetchall()
    cursor.execute("select * from tasks where status='completed';")
    tasks+=cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('index.html', tasks=tasks)

# Route to add a new task
@app.route('/add_task', methods=['POST'])
def add_task():
    conn = connect_db()
    if not conn:
        flash("Database connection failed", "danger")
        return redirect(url_for('index'))

    task_name = request.form['task_name']
    description = request.form['description']
    due_date = request.form['due_date']
    category = request.form['category']

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (task_name, description, due_date, category, status) VALUES (%s, %s, %s, %s, 'Yet to Do')",
        (task_name, description, due_date, category)
    )
    conn.commit()

    cursor.close()
    conn.close()

    flash('Task added successfully', 'success')
    return redirect(url_for('index'))

# Route to update task status
@app.route('/update_status/<int:id>/<string:status>')
def update_status(id, status):
    conn = connect_db()
    if not conn:
        flash("Database connection failed", "danger")
        return redirect(url_for('index'))

    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = %s WHERE id = %s", (status, id))
    conn.commit()

    cursor.close()
    conn.close()
    flash(f'Task marked as {status}', 'success')
    return redirect(url_for('index'))

# Route to delete a task
@app.route('/delete_task/<int:id>')
def delete_task(id):
    conn = connect_db()
    if not conn:
        flash("Database connection failed", "danger")
        return redirect(url_for('index'))

    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    flash('Task deleted successfully', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    conn = connect_db()
    if not conn:
        flash("Database connection failed", "danger")
        return redirect(url_for('index'))

    cursor = conn.cursor(dictionary=True)
    
    # Fetch task count by status
    cursor.execute("SELECT status, COUNT(*) as count FROM tasks GROUP BY status")
    status_counts = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    # Organize the data for easier access in the template
    counts = {
        'Completed': 0,
        'Ongoing': 0,
        'Yet to Do': 0
    }

    for row in status_counts:
        counts[row['status']] = row['count']

    return render_template('dashboard.html', counts=counts)

if __name__ == '__main__':
    app.run(debug=True)
