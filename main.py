import json
import requests
import urllib.parse
from requests.auth import HTTPBasicAuth
import quart
import quart_cors
from quart import request

# Note: Setting CORS to allow chat.openapi.com is only required when running a localhost plugin
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")
HOST_URL = "http://localhost:8080"

@app.get("/change_request/<string:number>")
async def get_change_request_details(number):
    res = requests.get(
        f"{HOST_URL}/api/now/table/change_request/{number}", auth = HTTPBasicAuth('admin', 'admin'))
    body = res.json()
    return quart.Response(response=json.dumps(body), status=200)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("ai-plugin.json") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the manifest
        #text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the OpenAPI spec
        #text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/yaml")


def main():
    app.run(debug=True, host="127.0.0.1", port=5001)


if __name__ == "__main__":
    main()
