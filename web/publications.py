from flask import Blueprint, render_template, request

publications = Blueprint('publications', __name__, template_folder='templates')

@publications.route("/publications")
def publications_list():
    return render_template("publications_list.html")