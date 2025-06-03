from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recomendar', methods=['POST'])
def recomendar():
    data = request.get_json()
    if not data or 'habilidades' not in data:
        return jsonify({'erro': 'Campo "habilidades" é obrigatório'}), 400

    habilidades = data['habilidades']
    # Simulação de recomendação com base nas habilidades
    vagas = [
        {"empresa": "Empresa A", "pontuacao": 0.9},
        {"empresa": "Empresa B", "pontuacao": 0.85}
    ]
    return jsonify(vagas)

if __name__ == '__main__':
    app.run(debug=True)
