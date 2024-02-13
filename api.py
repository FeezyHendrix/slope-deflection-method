from flask import Flask, render_template, jsonify, make_response, request
from flask_cors import CORS
from engine import calculate_beam_properties

app = Flask(__name__)
CORS(app)

@app.route("/")
def home_page():
  return render_template('index.html')

@app.route("/calculate", methods=['POST'])
def calculate():
  data = request.get_json()
  print(data)
    

    # Extract parameters from the request
  number_of_supports = data.get('number_of_supports')
  number_of_internal_joints = data.get('number_of_internal_joints')
  span_data = data.get('span_data')
  settlement_positions = data.get('settlement_positions', [])
  settlement_values = data.get('settlement_values', [])
  settlement_on_beam = data.get('settlement_on_beam', "no")
  first_node_fixed = data.get('first_node_fixed', "no")
  last_node_fixed = data.get('last_node_fixed', "no")

  # Call the function
  result = calculate_beam_properties(number_of_supports, number_of_internal_joints, span_data, settlement_positions, settlement_values, settlement_on_beam, first_node_fixed, last_node_fixed)

  # Return the result as a JSON response
  return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=6900)