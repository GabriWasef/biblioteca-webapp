from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configurazione database Aiven
DB_CONFIG = {
    "user": "your_db_user",
    "password": "your_db_password",
    "host": "your_db_host.aivencloud.com",
    "port": 27368,
    "database": "biblioteca",
    "ssl_disabled": False
}

def get_db_connection():
    """Crea connessione al database MySQL con SSL"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Exception as e:
        print(f"❌ Errore connessione DB: {e}")
        raise

# ===== LIBRI ENDPOINTS =====

@app.route('/api/libri', methods=['GET'])
def get_libri():
    """Ottieni tutti i libri"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Libri ORDER BY id_libro DESC")
        libri = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(libri)
    except Exception as e:
        print(f"❌ Errore GET libri: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/libri/<int:id>', methods=['GET'])
def get_libro(id):
    """Ottieni un libro specifico"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Libri WHERE id_libro = %s", (id,))
        libro = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(libro)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/libri', methods=['POST'])
def create_libro():
    """Crea nuovo libro"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """INSERT INTO Libri (titolo, autore, anno_pubblicazione, genere) 
                   VALUES (%s, %s, %s, %s)"""
        cursor.execute(query, (data['titolo'], data['autore'], 
                              data['anno_pubblicazione'], data['genere']))
        conn.commit()
        libro_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"id": libro_id, "message": "Libro creato"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/libri/<int:id>', methods=['PUT'])
def update_libro(id):
    """Aggiorna libro esistente"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """UPDATE Libri SET titolo=%s, autore=%s, 
                   anno_pubblicazione=%s, genere=%s WHERE id_libro=%s"""
        cursor.execute(query, (data['titolo'], data['autore'],
                              data['anno_pubblicazione'], data['genere'], id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Libro aggiornato"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/libri/<int:id>', methods=['DELETE'])
def delete_libro(id):
    """Elimina libro"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Libri WHERE id_libro = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Libro eliminato"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== LETTORI ENDPOINTS =====

@app.route('/api/lettori', methods=['GET'])
def get_lettori():
    """Ottieni tutti i lettori"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Lettori ORDER BY id_lettore DESC")
        lettori = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(lettori)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/lettori/<int:id>', methods=['GET'])
def get_lettore(id):
    """Ottieni un lettore specifico"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Lettori WHERE id_lettore = %s", (id,))
        lettore = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(lettore)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/lettori', methods=['POST'])
def create_lettore():
    """Crea nuovo lettore"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """INSERT INTO Lettori (nome, cognome, email, citta) 
                   VALUES (%s, %s, %s, %s)"""
        cursor.execute(query, (data['nome'], data['cognome'], 
                              data['email'], data['citta']))
        conn.commit()
        lettore_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"id": lettore_id, "message": "Lettore creato"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/lettori/<int:id>', methods=['PUT'])
def update_lettore(id):
    """Aggiorna lettore esistente"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """UPDATE Lettori SET nome=%s, cognome=%s, 
                   email=%s, citta=%s WHERE id_lettore=%s"""
        cursor.execute(query, (data['nome'], data['cognome'],
                              data['email'], data['citta'], id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Lettore aggiornato"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/lettori/<int:id>', methods=['DELETE'])
def delete_lettore(id):
    """Elimina lettore"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Lettori WHERE id_lettore = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Lettore eliminato"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== PRESTITI ENDPOINTS =====

@app.route('/api/prestiti', methods=['GET'])
def get_prestiti():
    """Ottieni tutti i prestiti con dettagli libro e lettore"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT p.*, l.titolo as libro_titolo, 
                   CONCAT(le.nome, ' ', le.cognome) as lettore_nome
            FROM Prestiti p
            LEFT JOIN Libri l ON p.id_libro = l.id_libro
            LEFT JOIN Lettori le ON p.id_lettore = le.id_lettore
            ORDER BY p.id_prestito DESC
        """
        cursor.execute(query)
        prestiti = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(prestiti)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/prestiti/<int:id>', methods=['GET'])
def get_prestito(id):
    """Ottieni un prestito specifico"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Prestiti WHERE id_prestito = %s", (id,))
        prestito = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(prestito)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/prestiti', methods=['POST'])
def create_prestito():
    """Crea nuovo prestito"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """INSERT INTO Prestiti (id_libro, id_lettore, data_prestito, data_restituzione) 
                   VALUES (%s, %s, %s, %s)"""
        cursor.execute(query, (data['id_libro'], data['id_lettore'],
                              data['data_prestito'], data.get('data_restituzione')))
        conn.commit()
        prestito_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"id": prestito_id, "message": "Prestito creato"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/prestiti/<int:id>', methods=['PUT'])
def update_prestito(id):
    """Aggiorna prestito esistente"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """UPDATE Prestiti SET id_libro=%s, id_lettore=%s,
                   data_prestito=%s, data_restituzione=%s WHERE id_prestito=%s"""
        cursor.execute(query, (data['id_libro'], data['id_lettore'],
                              data['data_prestito'], data.get('data_restituzione'), id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Prestito aggiornato"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/prestiti/<int:id>', methods=['DELETE'])
def delete_prestito(id):
    """Elimina prestito"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Prestiti WHERE id_prestito = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Prestito eliminato"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Avvio Flask su http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
