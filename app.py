from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Ana sayfa
@app.route('/')
def index():
    return render_template('index.html')

# Form gönderimi
@app.route('/submit', methods=['POST'])
def submit():
    student_id = request.form['student_id']
    program = request.form['program']
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO meals (student_id, program, date) VALUES (?, ?, ?)',
                   (student_id, program, date))
    conn.commit()
    conn.close()

    return 'Yemek kaydı başarıyla alındı!'

# Uygulama ve veritabanı başlatma
if __name__ == '__main__':
    # Veritabanı bağlantısı ve tablo oluşturma
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

    # Uygulamayı başlat
    app.run(host='0.0.0.0', port=5000, debug=True)
