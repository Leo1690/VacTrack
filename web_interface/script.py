from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse

app = Flask(__name__)

def check_vacuum():
    """
    Check if vacuum is available or not
    """
 
    my_file = open("data.txt", "r")
    signal = (int)(my_file.read())

    if(signal == -100):
        return "Vacuum cleaner not available"

    elif (signal == 0):
        return "Vacuum cleaner is available"

    my_file.close()

@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    resp = MessagingResponse()
    print(f'{number}, {message_body}')
    resp_msg = check_vacuum()
    resp.message(resp_msg)
    return str(resp)

if __name__ == '__main__':
    app.run()