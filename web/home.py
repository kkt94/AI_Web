from flask import Blueprint, render_template, request

home = Blueprint('home', __name__, template_folder='templates')
@home.route("/main")
def main():
    return render_template("main.html")

@home.route("/intro")
def intro():
    return render_template("intro.html")