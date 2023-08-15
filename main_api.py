from flask import Flask, request, jsonify
from luminosidade import controla_luminosidade

app = Flask(__name__)
#********************************************************************************#
@app.route('/luminosidade', methods=['POST'])
def compute_luminosity():
    data = request.get_json()

    luminosidade = data['luminosidade']
    presenca = data['presenca']
    temperatura = data['temperatura']
    preferencia = data['preferencia']

    intensidade, nivel = controla_luminosidade(luminosidade, presenca, temperatura, preferencia)   
    
    result = {
        'nivel': nivel,
        'intensity_output': str(intensidade)
    }

    return jsonify(result)

#********************************************************************************#
def controle_api():
    app.run(debug=True)

#********************************************************************************#
if __name__ == "__main__":
    controle_api()