from flask import jsonify, request, Blueprint, make_response
from app.services.AIService import AIService
from app.services.DBService import DBService
from app.models.Document import Document
import matplotlib.pyplot as plt
import io

api = Blueprint('api', __name__)

@api.route('/get-db-schema', methods=['GET'])
def get_db_schema_route():
    schema = DBService.get_schema()
    return jsonify(schema)

@api.route('/get-sql-response', methods=['POST'])
def get_sql_response():
    data = request.get_json()
    query = data.get("query")

    try:
        results = DBService.execute_query(query)
        return jsonify(results)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@api.route('/generate-ai-response', methods=['POST'])
def generate_ai_response():
    data = request.get_json()
    prompt = data.get("prompt")

    try:
        response_text = AIService.generate_and_execute_python(prompt)
        return jsonify({"response": response_text})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@api.route('/generate-document', methods=['GET'])
def generate_document():
    doc = Document()
    
    doc.add_title("Product Data Report")
    doc.add_subtitle("Generated Sales Report")
    
    doc.add_text("This document contains the sales data for various products.")
    
    product_data = [
        {"name": "Car Model X", "description": "Electric car with high range and performance."},
        {"name": "Car Model Y", "description": "Compact electric car perfect for city driving."}
    ]
    
    table_data = [["Name", "Description"]] + [[p['name'], p['description']] for p in product_data]
    doc.add_table(table_data)
    
    sales_data = [23, 45, 56, 78, 34, 22, 65, 89, 54, 34]
    plt.figure(figsize=(8, 6))
    plt.hist(sales_data, bins=5, color='blue', edgecolor='black')
    plt.title("Sales Data Histogram")
    plt.xlabel("Sales")
    plt.ylabel("Frequency")

    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    plt.close()
    img_io.seek(0)

    doc.add_image(img_io)

    pdf_output = doc.generate()
    
    response = make_response(pdf_output)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename="product_data_report.pdf"'
    
    return response
