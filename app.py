from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect('movies.db')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    search = request.args.get('search', '')
    genre = request.args.get('genre', '')

    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM movies WHERE 1=1"
    params = []

    if search:
        query += " AND Title LIKE ?"
        params.append(f"%{search}%")

    if genre:
        query += " AND Genres LIKE ?"
        params.append(f"%{genre}%")

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    movies = []
    for row in rows:
        movies.append({
            "Title": row[0],
            "Year": row[1],
            "IMDb": row[2],
            "Duration": row[3],
            "Genres": row[4],
            "Synopsis": row[5],
            "Cast": row[6],
            "Director": row[7],
            "Providers": row[8],
            "Link": row[9]
        })

    return jsonify(movies)

if __name__ == '__main__':
    app.run(debug=True)