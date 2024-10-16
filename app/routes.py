from flask import jsonify, request, Blueprint, make_response
from app import get_db_connection, get_db_schema, get_api_connection
from fpdf import FPDF
import io
import matplotlib.pyplot as plt

api = Blueprint('api', __name__)

@api.route('/get-db-schema', methods=['GET'])
def get_db_schema_route():
    schema = get_db_schema()
    return jsonify(schema)

@api.route('/get-sql-response', methods=['POST'])
def get_sql_respone():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(results)

@api.route('/generate-ai-response', methods=['POST'])
def generate_ai_respone():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    conn = get_api_connection()
    response = conn.chat(
        model="command-r-plus-08-2024",
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    
    description_text = response.message.content[0].text
    
    return jsonify({"response": description_text})

@api.route('/generate-pdf', methods=['GET'])
def generate_pdf():
    pdf = FPDF()

    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Product Data Report", ln=True, align='C')

    pdf.ln(10)

    product_data = [
        {"name": "Car Model X", "description": "Electric car with high range and performance."},
        {"name": "Car Model Y", "description": "Compact electric car perfect for city driving."}
    ]

    pdf.set_font('Arial', '', 12)
    for product in product_data:
        pdf.cell(200, 10, txt=f"Product: {product['name']}", ln=True)
        pdf.cell(200, 10, txt=f"Description: {product['description']}", ln=True)
        pdf.ln(10)

    pdf_output = pdf.output(dest='S').encode('latin1')

    response = make_response(pdf_output)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename="product_data_report.pdf"'

    return response

@api.route('/generate-chart', methods=['GET'])
def generate_chart():
    sales_data = [23, 45, 56, 78, 34, 22, 65, 89, 54, 34]

    plt.figure(figsize=(8, 6))
    plt.hist(sales_data, bins=5, color='blue', edgecolor='black')
    plt.title("Sales Data Histogram")
    plt.xlabel("Sales")
    plt.ylabel("Frequency")

    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)

    response = make_response(img_io.read())
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Disposition'] = 'inline; filename="sales_histogram.png"'

    return response