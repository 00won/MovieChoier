import openai

#테스트
#from flask import Flask, render_template, request, jsonify

openai.api_key = 'OpenAI api 추가'

class chatAI():
    def __init__(self):
      self.initialize()

    def initialize(self, ):
        self.messages = []

    def reply(self, message):
        prompt_additions = ''

        self.messages.append({'role': 'user', 'content': message})
        self.messages.append({'role': 'system', 'content': prompt_additions})

        chatAnswer = openai.ChatCompletion.create( 
            model="gpt-3.5-turbo",
            messages=self.messages
            )
        
        result = chatAnswer.choices[0].message.content
        self.messages.append({"role": "assistant", "content": result})

        return result