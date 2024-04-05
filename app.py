from flask import Flask, render_template, request, jsonify
import model


app = Flask(__name__)

def chat_reply(message):
      return model.chatAI().reply(message)

# 플라스크 실행시 기본 경로
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.get_json('message')
    print(text)
    msg = text['message']
    print(msg)
    reply = chat_reply(msg)
    print(reply)
    massage = {'answer': reply}
    return jsonify(massage)


if __name__ == '__main__':
    app.run(debug=True)