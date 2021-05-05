import json, requests

api_id = ""

def test_api(url, payload):
    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()  # if status !=200 raise exception
        return {
            'api_url': url,
            'success': True,
            'content': json.loads(r.content)
        }
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

api_gw_url = f"https://{api_id}.execute-api.eu-west-1.amazonaws.com"
test_payload = {
            "f0": -0.158164,
            "f1": 0.280982,
            "f2": -0.227545,
            "f3": -0.352298,
            "f4": -0.596421,
            "f5": 0.019102,
            "f6": -0.135293,
            "f7": 0.0,
            "f8": 0.0,
            "f9": 1.0,
            "f10":0.001248,
            "f11":-0.235234,
            "f12":0.334334,
            "f14":0.512786
        }

results = test_api(api_gw_url, test_payload)
print(results)