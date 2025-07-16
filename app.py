from flask import Flask, request

app = Flask(__name__)

@app.route('/notify', methods=['GET', 'POST'])
def notify():
    if request.method == 'POST':
        # Try form first, fallback to json if needed
        email = request.form.get('EmailAddress') or (request.json.get('EmailAddress') if request.json else None)
        campaign = request.form.get('CampaignID') or (request.json.get('CampaignID') if request.json else None)
        useragent = request.form.get('UserAgent') or (request.json.get('UserAgent') if request.json else None)
        timestamp = request.form.get('TimeStamp') or (request.json.get('TimeStamp') if request.json else None)
    else:  # GET method
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
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
