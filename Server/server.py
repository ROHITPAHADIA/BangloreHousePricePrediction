from flask import Flask, request, jsonify, send_from_directory
import util
import os

# Load model artifacts
util.load_saved_artifacts()

app = Flask(__name__)

# ---------- ROUTES ----------

# ✅ Serve the homepage (client HTML)
@app.route('/')
def serve_home():
    return send_from_directory('../client', 'app.html')

# ✅ Serve static files (JS, CSS, images)
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory('../client', path)

# ✅ API route to get location names
@app.route('/get_location_names')
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# ✅ API route to predict price
@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = float(request.form['bhk'])
    bath = float(request.form['bath'])

    response = jsonify({
        'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# ---------- MAIN ----------
if __name__ == "__main__":
    print("Starting python flask server for home price prediction...")
    # host=0.0.0.0 allows access from other devices on same network if needed
    app.run(debug=True, host='127.0.0.1', port=5000)
