import json

def get_fields(data):
    try:
        # Comprobar si 'user' está presente
        user = data.get('user')
        if user is None:
            raise ValueError("Error: 'user' key is missing")

        # Comprobar si 'temperature' o 'presence' está presente
        if 'temperature' in data:
            sensor_type = 'temperature'
            sensor_value = data['temperature']
        elif 'presence' in data:
            sensor_type = 'presence'
            sensor_value = data['presence']
        else:
            raise ValueError("Error: Neither 'temperature' nor 'presence' key is present")

        # Comprobar si 'filtered' está presente
        isFiltered = data.get('filtered')
        if isFiltered is None:
            raise ValueError("Error: 'filtered' key is missing")

        # Comprobar si 'timestamp' está presente
        timestamp = data.get('timestamp')
        if timestamp is None:
            raise ValueError("Error: 'timestamp' key is missing")

        # En caso de que no haya errores, devolver los parámetros
        return user, sensor_type, sensor_value, isFiltered, timestamp

    except ValueError as ve:
        print(ve)