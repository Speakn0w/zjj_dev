import requests
import json

def send_message_to_server(url, session_id, user_id, content, function_type):
    data = {
        'session_id': session_id,
        'user_id': user_id,
        'content': content,
        'function_type': function_type
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

def main():
    url = "http://localhost:5008/the-url"  # Adjust as needed for the actual server location
    session_id = "123456"  # Use a consistent session ID for maintaining session state
    user_id = "user_01"

    print("Start talking with the server (type 'exit' to quit):")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting dialogue...")
            break

        result = send_message_to_server(url, session_id, user_id, user_input, "dialog")
        if result:
            print("Server:", result.get('content', 'No response from server'))

if __name__ == "__main__":
    main()
