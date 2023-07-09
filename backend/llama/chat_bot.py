import requests
import json
import subprocess

DETACHED_PROCESS = 0x00000008


class ChatBotSettings:
    def __init__(self, req_url: str, authorization: str, organization: str, model: str, max_tokens: int, temperature: float, stream: bool = True, personality: str = 'you are chat bot'):
        self.req_url = req_url
        self.authorization = authorization
        self.organization = organization
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.stream = stream
        self.personality = personality


class ChatBot:
    def __init__(self, settings):
        self.settings: ChatBotSettings = settings
        self.history: [{}] = []
        self.req_headers = {
            'Accept': 'text/event-stream',
            'Authorization': self.settings.authorization,
            'Content-Type': 'application/json',
            'OpenAI-Organization': self.settings.organization,
        }

    def is_server_running(self):
        try:
            requests.get(self.settings.req_url)
            return True
        except requests.exceptions.ConnectionError:
            return False

    def start_server(self):

        if self.is_server_running():
            return
        command = f"python -m llama_cpp.server --model {self.settings.model}"
        subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         creationflags=DETACHED_PROCESS)

        while not self.is_server_running():
            pass

    def close_server(self):
        if not self.is_server_running():
            return
        print("Closing server...")
        # get pid of server process port 8000
        command = "netstat -ano | findstr 127.0.0.1:8000"
        pid = subprocess.check_output(command, shell=True).decode('utf-8').split('\r\n')
        pid = [i for i in pid if i != ''][0].split(' ')[-1]
        print(f"Server pid: {pid}")
        command = f"taskkill /PID {pid} /F"
        subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def perform_request_with_streaming(self, message):
        self.history.append({"role": "user", "content": message})

        req_body = {
            "model": self.settings.model,
            "messages": self.history,
            "max_tokens": self.settings.max_tokens,
            "temperature": self.settings.temperature,
            "stream": True,
        }

        answer = ''
        request = requests.post(self.settings.req_url, stream=True, headers=self.req_headers,
                                json=req_body)
        for line in request.iter_lines():
            if not line:
                continue
            data = json.loads(line.decode('utf-8').lstrip('data: '))['choices'][0]

            if data.get('finish_reason') is not None:
                break

            if data['delta'].get('content'):
                answer += data['delta']['content']
                yield data['delta']['content']

        answer = answer.strip()
        self.history.append({"role": "assistant", "content": answer})

    def perform_request(self, message):
        self.history.append({"role": "user", "content": message})

        req_body = {
            "model": self.settings.model,
            "messages": self.history,
            "max_tokens": self.settings.max_tokens,
            "temperature": self.settings.temperature,
            "stream": False,
        }

        request = requests.post(self.settings.req_url, stream=False, headers=self.req_headers,
                                json=req_body)
        if request.status_code != 200:
            raise Exception(f'Error: {request.status_code}')

        answer = request.json()['choices'][0]['message']['content']
        self.history.append({"role": "assistant", "content": answer})
        return answer.strip()

    def get_history_string(self):
        history_string = ''
        for message in self.history:
            if message['role'] == 'user':
                history_string += 'User: ' + message['content'] + '\n'
            else:
                history_string += 'Assistant: ' + message['content'] + '\n'
        return history_string

    def perform_request_with_openAI(self, message):
        import openai
        openai.api_key = "sk-xxx"
        openai.api_base = "http://localhost:8000/v1"

        self.history.append({"role": "user", "content": message})

        response = openai.Completion.create(
            model=self.settings.model,
            prompt="### System: " + self.settings.personality +
                   "\n\n### History:\n" + self.get_history_string() +
                   "\n\n### Instructions:\n" + message + "\n\n### Response:\n",
            max_tokens=100,
            stop=["###"],
        )
        return response.choices[0].text

    def perform_request_with_openAI_stream(self, message):
        import openai
        openai.api_key = "sk-xxx"
        openai.api_base = "http://localhost:8000/v1"

        self.history.append({"role": "user", "content": message})

        response = openai.Completion.create(
            model=self.settings.model,
            prompt="### System: " + self.settings.personality +
                   "\n\n### History:\n" + self.get_history_string() +
                   "\n\n### Instructions:\n" + message + "\n\n### Response:\n",
            max_tokens=100,
            stop=["\n"],
            stream=True
        )

        for result in response:
            if result['choices'][0]['finish_reason'] is not None:
                break
            yield result['choices'][0]['text']

    def chat(self, message, provider: ['openai', 'local'] = 'openai'):
        if provider == 'openai':
            if self.settings.stream:
                return self.perform_request_with_openAI_stream(message)
            else:
                return self.perform_request_with_openAI(message)
        elif provider == 'local':
            if self.settings.stream:
                return self.perform_request_with_streaming(message)
            else:
                return self.perform_request(message)

    def reset(self):
        self.history = []


settings = ChatBotSettings(
    req_url='http://localhost:8000/v1/chat/completions',
    authorization='Bearer token',
    organization='LLC BetaBlaze&AlanShan',
    model=r'E:\git\astral-LLM\backend\llama\models\ru-openllama-7b-v5-q5_K.bin',
    max_tokens=1000,
    temperature=0.6,
)

def demo():
    bot = ChatBot(settings)

    while True:
        message = input('>>> ')
        if message == 'exit':
            break
        for response in bot.chat(message, provider='openai'):
            print(response, end='')
        print()

    bot.close_server()


if __name__ == '__main__':
    bot = ChatBot(settings)

    print(bot.make_index(r'E:\git\astral-LLM\backend\README.md'))