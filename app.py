 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/app.py b/app.py
index fa3a4a9bf553a296d8c7e56c53f65cac98dc8318..9a452e292f387cf632c10ac13d1f6f4dcb98400b 100644
--- a/app.py
+++ b/app.py
@@ -19,51 +19,51 @@ def index():
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
-    return render_template('kayitlar.html', rows=rows)
+    return render_template('kayitlar.html', records=rows)
 
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
     conn = sqlite3.connect('data.db')
     cursor = conn.cursor()
     cursor.execute('''
         CREATE TABLE IF NOT EXISTS meals (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
 
EOF
)