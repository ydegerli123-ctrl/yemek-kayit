from flask import Flask, render_template, request, redirect, url_for, Response
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Ana sayfa: form görüntüleme
@app.route('/')
def index():
    return render_template('index.html')

# Form gönderimi: veritabanına kayıt
@app.route('/submit', methods=['POST'])
def submit():
    student_id = request.form['student_id']
    program = request.form['program']
    date = datetime.now().strftime('%Y-%m-%d')

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO meals (student_id, program, date) VALUES (?, ?, ?)",
                   (student_id, program, date))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Kayıtları listele
@app.route('/kayıtlar')
def show_records():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, program, date FROM meals ORDER BY date DESC")
    records = cursor.fetchall()
    conn.close()
    return render_template('kayıtlar.html', records=records)

# CSV olarak dışa aktar
@app.route('/export')
def export_csv():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, program, date FROM meals")
    rows = cursor.fetchall()
    conn.close()

    output = '\ufeffÖğrenci No,Program,Tarih\n'
    for row in rows:
        output += f"{row[0]},{row[1]},{row[2]}\n"

    return Response(
        output,
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment;filename=yemek_kayitlari.csv"}
    )

# Veritabanı tablosu yoksa oluştur
if __name__ == '__main__':
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

    # Sunucuyu başlat
    app.run(host='0.0.0.0', port=5000, debug=True)
