from flask import Blueprint, render_template, request, redirect
from web.database import db_session
from web.models import Member

member = Blueprint('member', __name__, template_folder='templates')

@member.route('/member')
def member_list():
    phd = Member.query.filter(Member.degree == "phd").all()
    ms = Member.query.filter(Member.degree == "ms").all()
    under = Member.query.filter(Member.degree == "under").all()
    alumni = Member.query.filter(Member.degree == "alumni").all()
    return render_template("member_list.html", phd=phd, ms=ms, under=under, alumni=alumni)

@member.route("/member_insert", methods=['GET', 'POST'])
def member_insert():
    if request.method == "POST":
        name = request.form.get("name")
        print(name)
        degree = request.form.get("degree")
        email = request.form.get("email")
        homepage = request.form.get("homepage")
        research = request.form.get("research")
        image = request.form.get("image")

        new = Member(name, degree, email, homepage, research, image)

        db_session.add(new)
        db_session.commit()

        return redirect("/member")
    else:
        return render_template("member_insert.html")