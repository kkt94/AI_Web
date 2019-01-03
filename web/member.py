from flask import Blueprint, render_template, request


member = Blueprint('member', __name__, template_folder='templates')

@member.route('/member')
def member_list():
    return render_template("member_list.html")
