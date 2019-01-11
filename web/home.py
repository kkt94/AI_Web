from flask import Blueprint, render_template, request

home = Blueprint('home', __name__, template_folder='templates')

@home.route("/")
@home.route("/main")
def main():
    return render_template("main.html")

@home.route("/intro")
def intro():
    return render_template("intro.html")

@home.route("/research")
def research():
    f = open("web/static/data/research/research.txt", "r", encoding="utf-8")
    researches = []
    while True:
        line = f.readline()
        if not line: break
        line = line.rstrip()
        info = line.split("()")
        researches.append({"title": info[0], "content":info[1]})
    f.close()
    return render_template("research.html", researches=researches)

def get_link(fname):
    fname = "web/static/data/link/" + fname + ".txt"
    f = open(fname, "r", encoding="utf-8")
    links = []
    while True:
        line = f.readline()
        if not line: break
        line = line.rstrip()
        info = line.split("()")
        links.append({"title":info[0], "link":info[1]})
    f.close()
    return links

@home.route("/link")
def link():
    links = []
    types = ["Artificial Intelligence", "Brain and Cognitive Science", "Machine Learning", "Evolutionary Computation", "Molecular Computation", "BioInformatics"]

    for t in types:
        l = get_link(t)
        links.append({"type": t, "links": l})

    return render_template("link.html", links=links)