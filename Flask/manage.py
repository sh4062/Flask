from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from main import app
from exts import db
from models import User
#使用manage管理app
manager = Manager(app)
#使用migarte绑定app和db
migrate = Migrate(app,db)
#添加迁移脚本的命令到manage
manager.add_command('db',MigrateCommand)

if __name__ == "__main__":
    manager.run()