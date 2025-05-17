from flask import Flask

# Create an instance of the Flask class
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    return "Hello, World!"

# Define a route with a dynamic URL parameter
@app.route('/greet/<name>')
def greet(name):
    return f"Hello, {name}!"

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
