from flask import Flask, jsonify, request

app = Flask(__name__)

from flask import Flask, request,json
# ...

@app.route('/json_example', methods=['POST'])
def handle_json():
  content_type = request.headers.get('Content-Type')
  #if (content_type == 'application/json'):
  data = json.loads(request.data)
  print (request.data)
  print (data['name'])
  return  (data)
    #response = client.post('/data_extraction'), data=json.dumps(payload), headers=(accept_json)
    #return{'foo': 'bar'}

    #return {'aas':11,'as':122}
  #else:
   # return "Content type is not supported."

if __name__ == '__main__':
    app.run(debug=True, port=4000)
