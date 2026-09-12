"""Flask web app for the subnetting calculator."""

from flask import Flask, render_template, request

from subnetcalc.core import subnet_summary

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """Show the CIDR input form, and the subnet summary if one was submitted."""
    summary = None
    error = None

    if request.method == "POST":
        cidr = request.form.get("cidr", "")
        try:
            summary = subnet_summary(cidr)
        except ValueError as e:
            error = str(e)

    return render_template("index.html", summary=summary, error=error)


def main():
    """Run the Flask development server."""
    app.run(debug=True)


if __name__ == "__main__":
    main()