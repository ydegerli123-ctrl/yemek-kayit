from flask import Flask, render_template, request, Response
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
import sqlite3

def initialize_database():
    conn = sqlite3.connect('veritabani.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            program TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Bunu app.py'nin en başında bir defa çalıştır:
initialize_database()


@app.route('/', methods=['GET', 'POST'])
def index():
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    mesaj = None

    if request.method == 'POST':
        student_id = request.form['student_id']
        program = request.form['program']
        date = request.form['date']

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        # Aynı öğrenci numarası aynı gün tekrar kayıt yapamasın
        cursor.execute("SELECT COUNT(*) FROM meals WHERE student_id = ? AND date = ?", (student_id, date))
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute("INSERT INTO meals (student_id, program, date) VALUES (?, ?, ?)", (student_id, program, date))
            conn.commit()
            mesaj = "✅ Kayıt başarıyla alındı."
        else:
            mesaj = "⚠️ Bu öğrenci numarası için zaten kayıt yapılmış."

        conn.close()
        return render_template('index.html', date=tomorrow, submitted=True, mesaj=mesaj)

    return render_template('index.html', date=tomorrow, mesaj=mesaj)

@app.route('/kayitlar')
def kayitlar():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, program, date FROM meals")
    rows = cursor.fetchall()
    conn.close()
    return render_template('kayitlar.html', rows=rows)

@app.route('/csv')
def export_csv():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, program, date FROM meals")
    rows = cursor.fetchall()
    conn.close()

    # UTF-8 BOM ile düzgün Türkçe karakter desteği
    output = '\ufeffÖğrenci No,Program,Tarih\n'
    for row in rows:
        output += f"{row[0]},{row[1]},{row[2]}\n"

    return Response(
        output,
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment;filename=yemek_kayitlari.csv"}
    )

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

    app.run(debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
