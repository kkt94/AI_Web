from flask import Flask, render_template, session, url_for
from web.home import home
from web.member import member



app = Flask(__name__)
app.register_blueprint(home)
app.register_blueprint(member)

#error handler 404, 500
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html')