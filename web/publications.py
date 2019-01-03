from flask import Blueprint, render_template, request, redirect

publications = Blueprint('publications', __name__, template_folder='templates')

def get_publications(fname):
    fname = "web/static/data/publications/" + fname + ".txt"
    f = open(fname, "r", encoding="utf-8")
    papers = []
    while True:
        line = f.readline()
        if not line: break
        line = line.rstrip()
        info = line.split("()")
        papers.append({"title":info[0], "content":info[1]})
    f.close()
    return papers

@publications.route("/publications")
def publications_list():
    t = request.args.get('type')
    if(t == "DJ"):
        fname = "Domestic Journal"
    elif(t == "DC"):
        fname = "Domestic Conference"
    elif(t == "IJ"):
        fname = "International Journal"
    elif(t == "IC"):
        fname = "International Conference"
    else:
        fname = "Domestic Journal"
    papers = get_publications(fname)
    return render_template("publications_list.html", publications=papers, type=fname)