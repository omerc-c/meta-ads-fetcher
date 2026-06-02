from flask import Flask, jsonify, request
import urllib.request
import urllib.parse
import json

app = Flask(__name__)

@app.route('/ads', methods=['GET'])
def get_ads():
    token = request.args.get('token')
    brand = request.args.get('brand')
    country = request.args.get('country', 'US')

    if not token or not brand:
        return jsonify({"error": "Missing token or brand"}), 400

    params = urllib.parse.urlencode({
        "search_terms": brand,
        "ad_reached_countries": f'["{country}"]',
        "fields": "id,page_name,ad_creative_body,ad_snapshot_url,ad_creative_link_title,ad_creative_link_description",
        "limit": "1",
        "access_token": token
    })
    url = f"https://graph.facebook.com/v19.0/ads_archive?{params}"

    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
            return jsonify(data)
    except urllib.error.HTTPError as e:
        return jsonify({"error": e.read().decode()}), e.code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
