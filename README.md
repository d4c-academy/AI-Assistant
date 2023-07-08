# AI-Assistant
## aiassistantって？
aiassistantは、Jupyter Notebookや、Google Colaboratoryで動く、コード生成支援ツールです。<br>
askメソッドに生成したいコードの内容を渡すことで、ChatGPTがコードをPythonのコードを生成してくれます。みなさんのデータ分析を支援するツールです。

## インストール前の準備
このツールを使用するには、OpenAIのAPIキーが必要になります。下記URLからキーの発行を行い、使用してください。
https://openai.com/blog/openai-api

## インストール方法
ローカルの場合
```
pip install git+https://github.com/d4c-academy/AI-Assistant.git
```
Notebook上での場合
```
!pip install git+https://github.com/d4c-academy/AI-Assistant.git
```

## 使用方法
```
from aiassistant.analysis_assistant import AnalysisAssistant

assistant = AnalysisAssistant('YOUR OPENAI API KEY')

assistant.ask('hoge hoge')
```
OpenAIのAPIキーを、引数に渡すか、環境変数「OPENAI_API_KEY」に登録すると実行できます。どちらにもない場合は、使用できません。