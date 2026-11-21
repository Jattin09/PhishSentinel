
from flask import Flask, render_template, request
from src.predictor import predict_url
from src.input_validator import validate_url
from src.database_manager import (
    initialize_database,
    save_scan,
    get_recent_scans
)

app = Flask(__name__)

initialize_database()


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    if request.method == "POST":
        url = request.form.get("url", "").strip()

        is_valid, message = validate_url(url)

        if not is_valid:
            error = message
        else:
            try:
                result = predict_url(url)
                save_scan(result)
            except Exception as e:
                error = f"Analysis failed: {e}"

    history = get_recent_scans(10)

    return render_template(
        "index.html",
        result=result,
        error=error,
        history=history
    )


if __name__ == "__main__":
    app.run(debug=True)
