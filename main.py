from conversation import Conversation
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/dialogflow_fulfillment', methods=['POST'])
def conversation_hook():
    req = request.get_json(silent=True, force=True)
    conversation = Conversation()
    res = conversation.process_request(req)
    print(res)
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)
