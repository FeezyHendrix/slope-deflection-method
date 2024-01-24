from flask import Flask, render_template, jsonify, make_response, request

app = Flask(__name__)

@app.route("/")
def home_page():
  return render_template('index.html')

@app.route("/calculate", methods=['POST'])
def calculate():
  data = request.get_json()


if __name__ == '__main__':
    app.run(debug=True, port=6900)