from report import report_bp
from user import user_bp
from home import home_bp
from Model_methode import Model_bp
from verification import verify_bp
from common_imports import *
from database import init_app
from mail import init_mail
app = Flask(__name__)
app.secret_key = os.urandom(24)

init_app(app)
init_mail(app)
app.register_blueprint(report_bp,)
app.register_blueprint(user_bp,)
app.register_blueprint(home_bp)
app.register_blueprint(verify_bp)
#app.register_blueprint(Model_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
