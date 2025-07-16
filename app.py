from flask import Flask, request

app = Flask(__name__)

@app.route('/notify', methods=['GET'])
def notify():
    email = request.args.get('EmailAddress')
    campaign = request.args.get('CampaignID')
    useragent = request.args.get('UserAgent')
    timestamp = request.args.get('TimeStamp')
    print(email, campaign, useragent, timestamp)
    # TODO: Save to DB, Google Sheets, etc.
    return 'OK'

@app.route('/')
def health():
    return 'Render is up!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
