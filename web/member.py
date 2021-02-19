from flask import Blueprint, render_template

member = Blueprint('member', __name__, template_folder='templates')

def get_member(fname, isalumni=0):
    f = open(fname, "r", encoding="utf-8")
    student = []
    while True:
        line = f.readline()
        if not line: break
        line = line.rstrip()
        info = line.split("()")
        if(isalumni == 1):
            student.append({"name": info[0], "now": info[1]})
        else:
            student.append({"name":info[0], "email":info[1], "homepage":info[2], "research":info[3], "image":info[4]})
    f.close()
    return student

@member.route('/member')
def member_list():
    podoc_fname = "web/static/data/member/postdoc.txt"
    podoc = get_member(podoc_fname)
    phd_fname = "web/static/data/member/phd.txt"
    phd_student = get_member(phd_fname)
    integ_fname = "web/static/data/member/integrated.txt"
    integ_student = get_member(integ_fname)    
    ms_fname = "web/static/data/member/ms.txt"
    ms_student = get_member(ms_fname)
    under_fname = "web/static/data/member/under.txt"
    under_student = get_member(under_fname)
    alumni_fname = "web/static/data/member/alumni.txt"
    alumni_student = get_member(alumni_fname, 1)

    return render_template("member_list.html", postdoc=podoc, phd=phd_student, integ=integ_student, ms=ms_student, under=under_student, alumni=alumni_student)
