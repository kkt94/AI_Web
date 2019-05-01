from flask import Blueprint, render_template, request, jsonify
from optparse import OptionParser
import socket, random, sys

home = Blueprint('home', __name__, template_folder='templates')

# ChatScript
cs_host = "166.104.143.103"
cs_port = 1024
cs_addr = (cs_host, cs_port)

cs_bot = 'ailabfive'
cs_master = 'user'

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

@home.route("/contact")
def contact():
    return render_template("contact.html")

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

@home.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@home.route("/response", methods=['POST'])
def response():
    result = request.get_json()
    username = request.remote_addr + request.headers.get('User-Agent')
    message = username + chr(0) + cs_bot + chr(0) + result + chr(0)

    if len(result):
        split_result = result.split(' ')[0]
        if split_result == ":reset" or split_result == ":pos" or split_result == ":why" or split_result == ":build":
            message = cs_master + chr(0) + cs_bot + chr(0) + result + chr(0)
        message = message.encode("utf-8") # original
        # message = base64.b64encode(message)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.bind(("166.104.143.103", random.randrange(1025)+1024))
        client_socket.connect(cs_addr)
        client_socket.send(message)
        data_out = ''
        while True:
            buf = client_socket.recv(64)
            if len(buf) > 0:
                # data_out += buf.decode("utf-8")
                data_out += buf.decode("utf-8", errors='ignore') # original
                # data_out += buf.decode("utf-16")
            else:
                break
        client_socket.close()

        return jsonify(data_out)
