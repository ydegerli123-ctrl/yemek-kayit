from flask import Flask, render_template, request, Response
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)


def init_db():
    """Ensure the SQLite database and meals table exist before handling requests."""
    conn = sqlite3.connect('data.db')
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                program TEXT,
                date TEXT
            )
            '''
        )
        conn.commit()
    finally:
        conn.close()


# Veritabanını uygulama ayağa kalkarken hazırla (Render gibi ortamlarda gereklidir)
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    mesaj = None
    submitted = False

    if request.method == 'POST':
        student_id = request.form['student_id']
        program = request.form['program']
        date = tomorrow  # Yarının tarihi otomatik olarak alınır

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        # Aynı öğrenci aynı gün tekrar kayıt olmasın
        cursor.execute("SELECT COUNT(*) FROM meals WHERE student_id = ? AND date = ?", (student_id, date))
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute("INSERT INTO meals (student_id, program, date) VALUES (?, ?, ?)", (student_id, program, date))
            conn.commit()
            mesaj = "✅ Yarın için yemekhane kaydınız oluşturulmuştur."
        else:
            mesaj = "⚠️ Bu öğrenci numarası için zaten kayıt yapılmış."

        conn.close()
        submitted = True

    return render_template('index.html', date=tomorrow, mesaj=mesaj, submitted=submitted)

@app.route('/kayitlar')
def kayitlar():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, program, date FROM meals")
    rows = cursor.fetchall()
    conn.close()
    return render_template('kayitlar.html', records=rows)

@app.route('/csv')
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
        headers={"Content-Disposition": "attachment; filename=yemek_kayitlari.csv"}
    )

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
