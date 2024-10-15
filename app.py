from flask import Flask, request, jsonify
import cohere
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['API']['cohere_api_key']
co = cohere.ClientV2(api_key)

@app.route('/generate-description', methods=['POST'])
def generate_description():
    response = co.chat(
        model="command-r-plus-08-2024",
        messages=[{
            "role": "user",
            "content": "Écris une description de produit pour une voiture électrique en 50 à 75 mots"
        }]
    )
    
    description_text = response.message.content[0].text
    
    return jsonify({"description": description_text})

if __name__ == '__main__':
    app.run(debug=True)
