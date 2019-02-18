
from flask import Flask
from flask_script import Manager

from app.house_views import house_blue
from app.models import db
from app.user_views import user_blue

app = Flask(__name__)

app.register_blueprint(blueprint=user_blue, url_prefix='/user/')
app.register_blueprint(blueprint=house_blue, url_prefix='/house/')

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@39.108.145.217:3306/ihome'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.secret_key = 'qw321hf142rt4345jlk35rcx139jkd'

manage = Manager(app)

if __name__ == '__main__':
    manage.run()