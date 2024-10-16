from flask import jsonify, Blueprint
from app import get_db_connection, get_api_connection

api = Blueprint('api', __name__)

@api.route('/generate-description', methods=['POST'])
def generate_description():
    conn = get_api_connection()
    response = conn.chat(
        model="command-r-plus-08-2024",
        messages=[{
            "role": "user",
            "content": "Écris une description de produit pour une voiture électrique en 50 à 75 mots"
        }]
    )
    
    description_text = response.message.content[0].text
    
    return jsonify({"description": description_text})


@api.route('/get-data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRODUCT")
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(results)