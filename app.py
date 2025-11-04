from flask import Flask, render_template, request
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

# Veritabanı bağlantısı ve tablo oluşturma
def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            program TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Ana sayfa (form ve kayıt mesajı birlikte burada)
@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    if request.method == 'POST':
        student_id = request.form['student_id']
        program = request.form['program']
        date = (datetime.now().date() + timedelta(days=1)).strftime('%Y-%m-%d')

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO meals (student_id, program, date) VALUES (?, ?, ?)", 
                       (student_id, program, date))
        conn.commit()
        conn.close()

        message = f"Yemekhane kaydınız oluşturuldu. Tarih: {date}"

    return render_template('index.html', success_message="Yarın için yemekhane kaydınız oluşturulmuştur.")

# Kayıtları listele (isteğe bağlı)
@app.route('/kayitlar')
def show_records():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meals")
    rows = cursor.fetchall()
    conn.close()
    return render_template('kayitlar.html', records=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
