# 
# シンプルにchatGPTと会話するためのクラス
# 

from gptassistant.base_assistant import BaseAssistant

class ChatAssistant(BaseAssistant):

    def __init__(
            self,
            api_key: str = None,
            model: str = 'gpt-3.5-turbo',
            temperature: float = 0.5,
            gpt_system: str=None
    ) -> None:
        
        super().__init__(api_key, model, temperature)

        # chatGPTの'role':'system'用のパラメータ
        self.gpt_system = gpt_system

    def ask(self, message: str) -> str:
        new_message, answer = self.ask_gpt(message)

        self.add_history(new_message, answer)
        
        return answer['content']