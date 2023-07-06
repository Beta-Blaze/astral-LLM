from llama_cpp import Llama


class Chatbot:
    def __init__(self):
        self.llm = None
        self.mode = "response"
        self.color_mode = False

    def set_mode(self, mode):
        self.mode = mode

    def set_color_mode(self, color_mode):
        self.color_mode = color_mode

    def init_model(self, model_path):
        try:
            self.llm = Llama(model_path=model_path)
            return "Model initialized successfully"
        except Exception as e:
            return f"Error initializing model: {e}"

    def chat(self, input_str, max_tokens=64):
        if not self.llm:
            return "Model not initialized"
        if self.mode == "response":
            input_str = f"Q: {input_str} A: "
        output = self.llm(input_str, max_tokens=max_tokens, stop=["Q:", "\n"], echo=True)
        if self.color_mode:
            output = f"\033[32m{output}\033[0m"
        if self.mode == "chat":
            return output
        elif self.mode == "response":
            return output
        else:
            return "Invalid mode"

    def get_commands(self):
        return ["set_mode", "set_color_mode", "init_model", "chat", "get_commands"]


chatbot = Chatbot()
chatbot.init_model("./models/ru-openllama-7b-v5-q5_K.bin")
print(chatbot.chat("Земля плоская или круглая?"))
