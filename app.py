from flask import Flask, render_template, request, redirect
import random
import re
import string

app = Flask(__name__)
code_to_url = {}
url_to_code = {}


def make_code(length=6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def normalize_url(url):
    if not url:
        return ""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def create_short_url(long_url, host_url, custom_code=None):
    long_url = normalize_url(long_url)
    existing_code = url_to_code.get(long_url)
    if existing_code:
        return host_url + existing_code

    if custom_code:
        custom_code = custom_code.strip()
        if not re.fullmatch(r"[A-Za-z0-9]+", custom_code):
            raise ValueError("Custom short code can only contain letters and numbers.")
        if len(custom_code) < 3:
            raise ValueError("Custom short code must be at least 3 characters long.")
        candidate = custom_code
        if candidate in code_to_url:
            raise ValueError("This short code is already in use. Please choose another one.")
    else:
        candidate = make_code()
        while candidate in code_to_url:
            candidate = make_code()

    code_to_url[candidate] = long_url
    url_to_code[long_url] = candidate
    return host_url + candidate


@app.route("/", methods=["GET", "POST"])
def home():
    short_url = None
    error = None

    if request.method == "POST":
        long_url = request.form.get("url", "").strip()
        custom_code = request.form.get("custom_code", "").strip()

        if not long_url:
            error = "Please enter a URL to shorten."
        else:
            try:
                short_url = create_short_url(long_url, request.host_url, custom_code)
            except ValueError as exc:
                error = str(exc)

    return render_template("index.html", short_url=short_url, error=error)


@app.route("/<code>")
def go(code):
    long_url = code_to_url.get(code)
    if long_url:
        return redirect(long_url)

    return "URL not found", 404


if __name__ == "__main__":
    app.run(debug=True)