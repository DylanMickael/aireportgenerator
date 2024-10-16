from flask import jsonify, Blueprint, make_response
from app import get_db_connection, get_api_connection
from fpdf import FPDF
import io

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


@api.route('/generate-pdf', methods=['GET'])
def generate_pdf():
    buffer = io.BytesIO()

    pdf = FPDF()

    # Ajouter une page au PDF
    pdf.add_page()

    # Définir la police
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Product Data Report", ln=True, align='C')

    pdf.ln(10)

    # Données de produit simulées
    product_data = [
        {"name": "Car Model X", "description": "Electric car with high range and performance."},
        {"name": "Car Model Y", "description": "Compact electric car perfect for city driving."}
    ]

    pdf.set_font('Arial', '', 12)
    for product in product_data:
        pdf.cell(200, 10, txt=f"Product: {product['name']}", ln=True)
        pdf.cell(200, 10, txt=f"Description: {product['description']}", ln=True)
        pdf.ln(10)

    # Écrire le contenu PDF dans le buffer
    pdf_output = pdf.output(dest='S').encode('latin1')  # Nécessaire pour gérer correctement l'encodage

    # Créer une réponse Flask avec le fichier PDF
    response = make_response(pdf_output)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename="product_data_report.pdf"'

    return response
