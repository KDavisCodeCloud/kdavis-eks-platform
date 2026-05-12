from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "KDavis DevOps Platform - EKS Deployment | Automated via GitHub Actions", 200

@app.route("/health")
def health():
    return "healthy", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
