from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import time
import os
import requests
import socket

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
GEOCODING_API_KEY = os.getenv("GEOCODING_API_KEY")
IP_STACK_API_KEY = os.getenv("IP_STACK_API_KEY")
IP_GEOLOCATION_API_KEY = os.getenv("IP_GEOLOCATION_API_KEY")

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
def get_weather(city):
    
    try:
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=pt_br&appid={OPEN_WEATHER_API_KEY}"
        weather_res = requests.get(weather_url)

        print(weather_url)
        
        if weather_res.status_code != 200:
            return {"erro": "Erro ao consultar a API de tempo!"}

        data = weather_res.json()

        return data

    except Exception as e:
        return {"erro": f"Erro ao consultar a API: {str(e)}"}


@app.route('/')
def render_app():
    try:
        endpoint = f"https://api.ipgeolocation.io/v2/ipgeo?apiKey={IP_GEOLOCATION_API_KEY}"
        res = requests.get(endpoint)

        if res.status_code != 200:
            return jsonify({"erro": "Erro ao consultar localização do IP!"}), 500
        
        data = res.json()
        user_city = data["location"]["city"]
        user_weather = get_weather(user_city)

        print(user_weather)

        return render_template("paginatempo.html", user_weather=user_weather)
    
    except requests.exceptions.RequestException as e:
        return jsonify({"erro": f"Erro ao fazer a requisição: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)