from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

def predict_model(val1, val2):
    return int(val1) + int(val2)

html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Predict with AI Model</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
  <div class="container mt-5">
    <div class="card shadow p-4">
      <h2 class="text-center mb-4">AI Model Prediction</h2>
      <form method="POST" action="/predict">
        <div class="mb-3">
          <label class="form-label">Input Value 1</label>
          <input type="text" class="form-control" name="val1" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Input Value 2</label>
          <input type="text" class="form-control" name="val2" required>
        </div>
        <button type="submit" class="btn btn-primary w-100">Predict</button>
      </form>
      {% if prediction is not none %}
      <div class="alert alert-success text-center mt-4">
        <strong>Prediction:</strong> {{ prediction }}
      </div>
      {% endif %}
    </div>
  </div>
</body>
</html>
'''

@app.route("/", methods=["GET"])
def index():
    return render_template_string(html_template, prediction=None)

@app.route("/predict", methods=["POST"])
def predict():
    # If client sent JSON, return JSON
    if request.is_json:
        try:
            data = request.get_json()
            val1, val2 = data["input"][0], data["input"][1]
            result = predict_model(val1, val2)
            return jsonify({"prediction": result})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # Otherwise assume form submission, render HTML
    try:
        val1 = request.form["val1"]
        val2 = request.form["val2"]
        result = predict_model(val1, val2)
        return render_template_string(html_template, prediction=result)
    except Exception as e:
        return render_template_string(html_template, prediction=f"Error: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
