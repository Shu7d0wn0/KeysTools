from flask import Flask, request, jsonify
import sqlite3
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)

def create_connection():
    conn = sqlite3.connect('access_keys.db')
    return conn

@app.route('/generate_key', methods=['POST'])
def generate_key():
    try:
        duration = request.json.get('duration')  # durée en jours (par exemple 1, 7, 14, 30, etc.)
        new_key = str(uuid.uuid4())
        expiration_date = None

        if duration and duration.lower() != 'lifetime':
            expiration_date = datetime.now() + timedelta(days=int(duration))
        elif duration and duration.lower() == 'lifetime':
            expiration_date = None

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO keys (key, expiration_date) VALUES (?, ?)", 
                       (new_key, expiration_date.strftime('%Y-%m-%d %H:%M:%S') if expiration_date else None))
        conn.commit()
        conn.close()
        return jsonify({"key": new_key, "expiration_date": expiration_date.strftime('%Y-%m-%d %H:%M:%S') if expiration_date else "No expiration"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/validate_key', methods=['POST'])
def validate_key():
    try:
        key = request.json.get('key')
        computer_id = request.json.get('computer_id')
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM keys WHERE key=?", (key,))
        key_data = cursor.fetchone()
        conn.close()

        if key_data:
            key_expiration = key_data[3]  # Assurez-vous que cet index correspond à la colonne expiration_date
            if key_expiration and datetime.strptime(key_expiration, '%Y-%m-%d %H:%M:%S') < datetime.now():
                return jsonify({"valid": False, "message": "Key has expired"})

            if key_data[4] is None:  # Si computer_id est None, associez-le à cet ordinateur
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE keys SET computer_id=? WHERE key=?", (computer_id, key))
                conn.commit()
                conn.close()
            elif key_data[4] != computer_id:
                return jsonify({"valid": False, "message": "Key is not associated with this computer"})

            return jsonify({"valid": True})
        else:
            return jsonify({"valid": False})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/list_keys', methods=['GET'])
def list_keys():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT key, expiration_date FROM keys")
        keys = [{"key": row[0], "expiration_date": row[1]} for row in cursor.fetchall()]
        conn.close()
        return jsonify({"keys": keys})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_key', methods=['POST'])
def delete_key():
    try:
        key_to_delete = request.json.get('key')
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM keys WHERE key=?", (key_to_delete,))
        conn.commit()
        key_exists = cursor.rowcount > 0
        conn.close()
        if key_exists:
            return jsonify({"message": f"Key {key_to_delete} deleted"})
        else:
            return jsonify({"message": "Key not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
