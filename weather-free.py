import requests

def get_weather_temp(location):
    url = f"https://wttr.in/{location}?format=j1"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        current_condition = weather_data['current_condition'][0]
        temp_C = current_condition['temp_C']
        temp_F = current_condition['temp_F']
        return temp_C, temp_F
    else:
        print("Error fetching weather data:", response.status_code)
        return None, None

# Example usage
location = "London"
temp_C, temp_F = get_weather_temp(location)
print(f"Temperature in Celsius: {temp_C}")
print(f"Temperature in Fahrenheit: {temp_F}")