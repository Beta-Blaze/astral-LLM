import requests
import json


def performRequestWithStreaming():
    reqUrl = 'http://localhost:8000/v1/chat/completions'
    reqHeaders = {
        'Accept': 'text/event-stream',
        'Authorization': 'Bearer token',
        'Content-Type': 'application/json',
        'OpenAI-Organization': 'LLC BetaBlaze&AlanShan',

    }

    messages = [{"role": "user", "content": 'Кто такой Пушкин?'}]

    reqBody = {
        "model": "our-gpt",
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0,
        "stream": True,
    }
    request = requests.post(reqUrl, stream=True, headers=reqHeaders, json=reqBody)
    for line in request.iter_lines():
        if line:
            # parse text/event-stream
            data = line.decode('utf-8').split(':', 1)
            if len(data) > 1:
                if data[1] == ' [DONE]':
                    break
                # print(data)
                event = data[0].strip()
                if event == 'data':
                    parse = json.loads(data[1])['choices'][0]['delta']
                    if parse.get('content'):
                        print(parse['content'], end='')
    print()


if __name__ == '__main__':
    performRequestWithStreaming()
