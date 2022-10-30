from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
  

db = SQLAlchemy()
DB_NAME = "testdb"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hello'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:postgres@localhost:5432/{DB_NAME}"
    # engine = db.create_engine(f"postgresql://postgres:postgres@localhost:5432/{DB_NAME}")
    # Session = sessionmaker(bind=engine)
    # session = Session()
    
    db.init_app(app)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from nftwebsite.models import UserInfo

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return UserInfo.query.get(int(id))

    

    return app


    
