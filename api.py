from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from prompt_builder import build_icse_visual_prompt
from image_generator import generate_icse_infographic
from study_text_generator import generate_study_json
import json, os, uuid
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import secrets 

app = Flask(__name__)
app.static_folder = '.'  # Serve static from /app (your index.html)
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)


app.config["JWT_SECRET_KEY"] = secrets.token_hex(32)
jwt = JWTManager(app)

# temporary in-memory store
users = {
    "arafat@icse.ai": generate_password_hash("tc3913"),
    "aayat@icse.ai": generate_password_hash("tc5149")
}


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # ❌ User must already exist
    if email not in users:
        return jsonify(error="Invalid credentials"), 401

    # ❌ Password must match
    if not check_password_hash(users[email], password):
        return jsonify(error="Invalid credentials"), 401

    # ✅ Valid login
    token = create_access_token(identity=email)
    return jsonify(token=token)


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    question = data.get("question")
    grade = int(data.get("grade"))

    if not question or grade not in range(5, 11):
        return jsonify({"error": "Invalid input"}), 400

    os.makedirs("output", exist_ok=True)

    # unique id for mobile/web users
    session_id = str(uuid.uuid4())[:8]

    image_path = f"output/icse_{session_id}.png"
    json_path = f"output/study_{session_id}.json"

    # STEP 1: Study content
    study_data = generate_study_json(question, grade)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(study_data, f, indent=2)

    # STEP 2: Infographic
    image_prompt = build_icse_visual_prompt(question, grade)
    generate_icse_infographic(image_prompt, image_path)

    return jsonify({
        "study_data": study_data,
        "image_url": f"/{image_path}"
    })


@app.route("/output/<path:filename>")
def serve_files(filename):
    # ✅ Correct way to serve files
    return send_from_directory("output", filename)


if __name__ == "__main__":
    #app.run(port=5000, debug=True)
    app.run(host="0.0.0.0", port=5000)
