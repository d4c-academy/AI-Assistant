# 
# notebook上で、分析をする際に使用するアシスタント
# 

import sys
import pandas as pd

from aiassistant.base_assistant import BaseAssistant

class AnalysisAssistant(BaseAssistant):

    def __init__(
            self,
            api_key: str = None,
            model: str = 'gpt-3.5-turbo',
            temperature: float = 0.5
    ) -> None:
        
        super().__init__(api_key, model, temperature)
        self.gpt_system = 'Pythonを使って実装する'

    def get_dataframes(self) -> list:
        '''
        main関数（notebookの想定）のdataframeとそのカラムをすべて取得する
        '''

        main_module = sys.modules['__main__']

        dataframes = []
        for var in dir(main_module):
            if var[0] == '_':
                continue

            if eval(f'isinstance(main_module.{var}, pd.DataFrame)'):
                name = var
                columns = str(list(eval(f'main_module.{var}.columns')))

                dataframes.append({
                    'name': name,
                    'columns': columns
                })
        
        return dataframes
    
    def is_python_code(self, message: str) -> bool:
        return '```python' in message

    def extract_python_code(self, message: str) -> str:
        '''
        chatGPTの返事から
        pythonのコードブロック部分のみを抽出して返す
        '''

        code = ''

        i = 0
        while(i < len(message)):
            if message[i:i+9] == '```python':
                start = i + 9
                i = start
            elif message[i:i+3] == '```':
                end = i
                code += message[start:end] + '\n'

            i += 1

        return code
    
    def ask(self, message: str) -> None:
        '''
        ChatGPTに聞くためのメソッド
        message引数に質問内容を渡す
        なお、Jupyter Notebook上での使用が前提
        '''

        dataframes = self.get_dataframes()
        if dataframes:
            message += '\n読み込んだデータフレーム名とそのカラムは以下です。\n'
            for dataframe in dataframes:
                message += dataframe['name'] + '\n'
                message += dataframe['columns'] + '\n'
        
        new_message, answer = self.ask_ChatGPT(message)

        if self.is_python_code(answer['content']):
            self.add_history(new_message, answer)

            print(self.extract_python_code(answer['content']))
        else:
            print('返事がPythonのコードではありませんでした')

    def ask_error(self, message: str) -> None:
        '''
        エラー文をChatGPTに聞く
        なお、履歴（history）には残さない
        '''
        
        message = '下記エラーの内容と解決方法を教えてください。\n' + message

        new_message, answer = self.ask_ChatGPT(message=message,use_history=False)

        print(answer['content'])
