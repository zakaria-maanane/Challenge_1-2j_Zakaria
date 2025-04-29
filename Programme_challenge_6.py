import requests
from urllib.parse import quote # sert Pour encoder les noms de villes avec des espaces ou caractères spéciaux

def get_weather(city, api_key):
    # Encodage de la ville pour éviter des erreurs avec des espaces ou caractères spéciaux
    city_encoded = quote(city)
    
    # URL de l'API WeatherAPI
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_encoded}&lang=fr"
    
    # Faire une requête à l'API
    response = requests.get(url)
    
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        data = response.json()
        
        # Extraire les informations nécessaires
        temperature = data['current']['temp_c']
        description = data['current']['condition']['text']
        humidity = data['current']['humidity']
        wind_speed = data['current']['wind_kph']
        
        # Afficher les informations sur la météo
        print(f"Météo à {city}:")
        print(f"Température: {temperature}°C")
        print(f"Description: {description}")
        print(f"Humidité: {humidity}%")
        print(f"Vitesse du vent: {wind_speed} km/h")
    else:
        print(f"Erreur {response.status_code}: Impossible de récupérer les données pour {city}.")

# Remplace "ton_api_key" par ta clé API WeatherAPI
api_key = "0488d6cea99c47b69d1123242252604"
city = input("Entrez le nom de la ville: ") 

get_weather(city, api_key)
