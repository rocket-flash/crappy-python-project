from flask import Flask, request, render_template_string, redirect

import sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username='%s' AND password='%s'" % (
        username,
        password,
    )
    cursor.execute(query)
    user = cursor.fetchone()

    if user:
        return "Login successful"
    else:
        return "Invalid credentials"


@app.route("/open_redirect")
def open_redirect():
    target = request.args.get("target")
    return redirect(target)


@app.route("/xss")
def xss():
    name = request.args.get("name")
    return render_template_string("<h1>Welcome, {{ name }}!</h1>", name=name)


@app.route("/ssti")
def ssti():
    template = request.args.get("template")
    return render_template_string(template)


@app.route("/ssti2")
def ssti2():
    template = request.args.get("template")
    return render_template_string("template2 = %s" + template)


@app.route("/execute", methods=["GET"])
def execute():
    command = request.args.get("command")
    result = os.popen(command).read()

    os.system("ls" + command)

    return result


@app.route("/view_file2", methods=["GET"])
def view_file2():
    file_name = request.args.get("file")
    with open("/path/" + file_name, "r") as file:
        content = file.read()

    return content


@app.route("/view_file", methods=["GET"])
def view_file():
    file_name = request.args.get("file")
    with open(file_name, "r") as file:
        content = file.read()

    return content


if __name__ == "__main__":
    app.run(debug=True)
