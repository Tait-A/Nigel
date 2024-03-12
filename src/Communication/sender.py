import json
import requests

# Replace 'your_object' with your actual Python object
your_object = {
    'name': 'Example Object',
    'type': 'Example Type',
    'details': {
        'description': 'This is a sample object for demonstration purposes.',
        'id': 123
    }
}

def send_object_as_json(url, obj):
    # Serialize the Python object into JSON
    json_data = json.dumps(obj)
    headers = {'Content-Type': 'application/json'}
    
    # Send the JSON data as a POST request
    response = requests.post(url, headers=headers, data=json_data)
    print(f"Response from server: {response.text}")

if __name__ == "__main__":
    # Specify the URL where the server is listening
    url = "192.168.105.135:8000"
    send_object_as_json(url, your_object)
