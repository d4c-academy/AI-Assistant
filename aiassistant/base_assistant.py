# 
# 基底クラス（BaseAssistant）を定義
# BaseAssistantをそのままimportすることはない想定
# 

import openai
from openai.error import InvalidRequestError, RateLimitError
import time
import os

from aiassistant.exceptions import APIKEYNotFoundError

class BaseAssistant:
    '''
    基底クラス
    '''

    def __init__(
            self,
            api_key: str = None,
            model: str = 'gpt-3.5-turbo',
            temperature: float = 0.5,
    ) -> None:
        '''
        基底クラスの__init__
        chatGPTのAPIキーが指定されていない場合、開始できない仕様
        '''

        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')

        if self.api_key is None:
            raise APIKEYNotFoundError('chatGPTのapiキーが指定されていません。')
        
        self.model = model
        self.temperature = temperature
        self.gpt_system = None
        self.history = []

    def reset_history(self) -> None:
        self.history = []

    def add_history(self, new_message: dict, answer: dict) -> None:
        self.history.append(new_message)
        self.history.append(answer)

    def api_format(self, role: str, content: str) -> dict:
        return {'role': role, 'content': content}

    def ask_ChatGPT(self, message: str, use_history: bool=True, history_length: int=None) -> tuple:
        '''
        messageに送信内容を渡すと
        送信内容、返信内容をapiのフォーマットにして返す

        返ってきた内容をprintしたり、
        historyに追加するのは、継承したクラスで行う

        過去の会話履歴を使用しない場合は、use_history=Falseに設定

        過去の会話履歴の中で直近n回分を使用する場合、history_lengthに整数を指定
        （バグりはしないが、history_lengthは2の倍数である必要がある）
        '''
        openai.api_key = self.api_key

        history_length = history_length or len(self.history)
        is_asking = True

        while(is_asking):

            messages = []

            if self.gpt_system:
                messages.append(self.api_format('system', self.gpt_system))
            
            
            if use_history:
                if len(self.history) > history_length:
                    messages += self.history[-1*history_length:].copy()
                else:
                    messages += self.history.copy()

            new_message = self.api_format('user', message)
            messages.append(new_message)

            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                )
                is_asking = False
            
            except InvalidRequestError as e:
                if 'reduce the length of the messages' in e._message:
                    history_length -= 2
                    time.sleep(1)
                    continue
                else:
                    raise Exception(e._message)
            
            except RateLimitError as e:
                raise Exception('一時的なサーバーエラーです。再度実行してください。\n何度も発生する場合は、APIの使用上限に達している可能性があります。')

        res = response['choices'][0]['message']['content']
        answer = self.api_format('assistant', res)

        return new_message, answer

    def ask(self, message: str) -> None:
        '''
        オーバーライド必須
        '''
        raise NotImplementedError