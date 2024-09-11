import aiohttp
import json
from printer import printer

async def fetch_event_stream(url, data):
    headers = {
        'Authorization': 'Zjj123456',
        'Content-Type': 'text/event-stream; charset=utf-8',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no'
    }
    async with aiohttp.ClientSession() as session:
        print("stream_true",data)
        async with session.post(url, data=data.encode('utf-8'), timeout=None, headers=headers) as response:
            reply = ""
            while True:
                #print("1")
                line = await response.content.readline()
                #print("line example:", line)
                if not line.strip():  # Skip empty lines
                    continue
                line = line.decode('utf-8')  # Decode bytes to string
                if line.strip().find(': [DONE]') != -1:  # Check for end of stream
                    break
                line = line.replace('data: ', '', 1)  # Remove "data: " prefix
                try:
                    line_json = json.loads(line)  # Convert string to JSON
                    choices = line_json.get('choices', [{}])  # Get choices list
                    first_choice = choices[0]  # Get first choice
                    content = first_choice.get('delta', {}).get('content', '')  # Extract content from delta
                    if content == "":
                        break
                    await printer(content)  # Print content without newline
                    reply = first_choice.get('message', {}).get('content', '')  # Save whole content to reply
                except json.JSONDecodeError:
                    print("Error decoding JSON")
            print()
            
            return {
                "role": "assistant",
                "content": reply
            }

# async def fetch_non_stream_response(url, data):
#     headers = {
#         'Authorization': 'Zjj123456',
#         'Content-Type': 'application/json',
#         'Accept': 'application/json',
#         'Accept-Encoding': 'gzip, deflate',
#         'Cache-Control': 'no-cache'
#     }
#     async with aiohttp.ClientSession() as session:
#         print(fetch_non_stream_response,data)
#         async with session.post(url, data=data.encode('utf-8'), timeout=None, headers=headers) as response:
#             reply = await response.json()
#             print("fetch_reply:", reply)
#             choices = reply.get('choices', [{}])
#             first_choice = choices[0]
#             content = first_choice.get('message', {}).get('content', '')
#             return {
#                 "role": "assistant",
#                 "content": content
#             }

import aiohttp
import json      
from volcenginesdkarkruntime import AsyncArk

client = AsyncArk(api_key="0b875849-8365-495f-acfa-3837842c4ba0")

async def fetch_non_stream_response(messages):
    print(messages,type(messages))
    stream = await client.chat.completions.create(
        model="ep-20240726181421-rfxtl",
        messages=messages,
        stream=False
    )
    async for completion in stream:
        print(completion.choices[0].delta.content, end="")
        return {
            "role": "assistant",
            "content": completion.choices[0].delta.content
        }