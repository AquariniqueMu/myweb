from flask import Flask, request, jsonify

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/echo', methods=['POST'])
def echo():
    # Assuming the data is sent as JSON
    data = request.json.get('search_input')  # Adjusted to match the JSON key
    print("Received input: ", data)

    # Return the received content
    return jsonify({'search_result': data})  # Adjusted key to match the frontend expectation

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5501)
