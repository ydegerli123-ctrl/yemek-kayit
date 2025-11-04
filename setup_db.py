import sqlite3

# Bağlantı oluştur
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# meals tablosunu oluştur
cursor.execute('''
    CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        program TEXT,
        date TEXT
    )
''')

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()

print("✅ Veritabanı ve meals tablosu başarıyla oluşturuldu.")
