from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import time
import os
import requests

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
GEOCODING_API_KEY = os.getenv("GEOCODING_API_KEY")
IP_STACK_API_KEY = os.getenv("IP_STACK_API_KEY")

app = Flask(__name__)

def get_cep(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    response = requests.get(url)
    print(response)
    
    if response.status_code != 200:
        return {"erro": "Falha ao consultar o CEP!"}
    
    data = response.json()

    if 'erro' in data:
        return {"erro": "CEP não encontrado!"}
    
    return data

@app.route('/weather', methods=['GET'])
def get_location():
    # Pegando o CEP dos parâmetros da URL
    cep = request.args.get('cep')

    if not cep:
        return jsonify({"erro": "CEP não informado!"}), 400
    
    if len(cep) != 8 or not cep.isdigit():
        return jsonify({"erro": "CEP inválido!"}), 400
    
    try:
        # Obtendo os dados do CEP
        address = get_cep(cep)
        query_cep = address["cep"].replace("-", "")
        city = address["localidade"]

        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=pt_br&appid={OPEN_WEATHER_API_KEY}"
        weather_res = requests.get(weather_url)

        print(weather_url)
        
        if weather_res.status_code != 200:
            return jsonify({"erro": "Erro ao consultar a API de tempo!"}), 500

        data = weather_res.json()

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"erro": f"Erro ao consultar a API: {str(e)}"}), 500

@app.route("/teste")
def render_test():
    return render_template("paginatempo.html")


@app.route('/')
def render_app():
    user_ip = request.remote_addr
    endpoint = f"http://api.ipstack.com/{user_ip}?access_key={IP_STACK_API_KEY}"
    
    try:
        res = requests.get(endpoint)

        if res.status_code != 200:
            return jsonify({"erro": "Erro ao consultar localização do IP!"}), 500

        data = res.json()  # Converte a resposta para JSON
        return jsonify(data), 200
    
    except requests.exceptions.RequestException as e:
        return jsonify({"erro": f"Erro ao fazer a requisição: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)