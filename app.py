
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)


def calculate(a, b, operation):
    for value in (a, b):
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError("Inputs must be positive integers")

    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b
    }

    if operation not in operations:
        raise ValueError("Invalid operation")

    return operations[operation]


@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Python Calculator</title>
        <style>
            body {
                font-family: Arial;
                background: #eef2f7;
                display: flex;
                justify-content: center;
                padding-top: 70px;
            }

            .calculator {
                background: white;
                padding: 30px;
                border-radius: 12px;
                width: 320px;
                box-shadow: 0 4px 15px #0002;
            }

            input, select, button {
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                box-sizing: border-box;
                font-size: 16px;
            }

            button {
                background: #2563eb;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
            }

            #result {
                font-size: 20px;
                font-weight: bold;
                margin-top: 20px;
            }
        </style>
    </head>

    <body>
        <div class="calculator">
            <h2>Python Calculator</h2>

            <form id="calculatorForm">

                <input type="number" id="a"
                    placeholder="First number"
                    min="1" step="1" required>

                <select id="operation">
                    <option value="add">Addition (+)</option>
                    <option value="subtract">Subtraction (-)</option>
                    <option value="multiply">Multiplication (×)</option>
                </select>

                <input type="number" id="b"
                    placeholder="Second number"
                    min="1" step="1" required>

                <button type="submit">Calculate</button>

            </form>

            <div id="result"></div>
        </div>

        <script>
            document.getElementById("calculatorForm")
            .addEventListener("submit", async function(event) {

                event.preventDefault();

                const response = await fetch("/calculate", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        a: Number(document.getElementById("a").value),
                        b: Number(document.getElementById("b").value),
                        operation: document.getElementById("operation").value
                    })
                });

                const data = await response.json();

                document.getElementById("result").textContent =
                    response.ok
                    ? "Result: " + data.result
                    : "Error: " + data.error;
            });
        </script>
    </body>
    </html>
    """)


@app.route("/health")
def health():
    return jsonify(status="healthy")


@app.route("/calculate", methods=["POST"])
def calculate_route():
    data = request.get_json(silent=True) or {}

    try:
        result = calculate(
            data.get("a"),
            data.get("b"),
            data.get("operation")
        )

        return jsonify(result=result)

    except ValueError as error:
        return jsonify(error=str(error)), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
