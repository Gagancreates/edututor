import requests
import json

def test_generate_api():
    url = "http://localhost:8000/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {"prompt": "Basic algebra equations"}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        
        try:
            response_json = response.json()
            print(f"Response JSON: {json.dumps(response_json, indent=2)}")
        except:
            print(f"Raw Response: {response.text}")
        
        if response.status_code == 200:
            print("Success!")
        else:
            print(f"Failed with status code {response.status_code}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_generate_api() 