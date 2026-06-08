from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>DevOps Demo Application</h1>
    <p>Successfully deployed using:</p>
    <ul>
        <li>GitHub</li>
        <li>Jenkins</li>
        <li>Docker</li>
        <li>AWS EC2</li>
    </ul>
    """

@app.route("/health")
def health():
    return {
        "status": "UP"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)