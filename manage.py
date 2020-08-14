from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from App import create_app, db

app = create_app('development')
app.app_context().push()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

from App.model.user import User, Role, roles_users
try:
    db.create_all()
    db.session.add(User("test1.qq.com", "test1", "test1"))
    db.session.add(User("test2.qq.com", "test2", "test2"))
    db.session.add(Role("admin", "管理员"))
    db.session.commit()
    db.engine.execute(roles_users.insert(), user_id=1, role_id=1)
    db.session.commit()
except Exception as e:
    print(e)

@manager.command
def run():
    print(app.url_map)
    app.run(host="0.0.0.0", port=5010)


if __name__ == '__main__':
    manager.run()