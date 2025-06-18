from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2

app = Flask(__name__)
CORS(app)

def lire_pdf(chemin_fichier):
    with open(chemin_fichier, 'rb') as fichier:
        lecteur = PyPDF2.PdfReader(fichier)
        texte = ""
        for page in lecteur.pages:
            texte += page.extract_text()
    return texte

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    contenu = lire_pdf('exemple.pdf')
    return jsonify({"response": f"Extrait : {contenu[:200]}..."})

if __name__ == '__main__':
    app.run(debug=True)
