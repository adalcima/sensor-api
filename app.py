from api import create_app, db

app = create_app()
with app.app_context():
    # create all tables
    db.create_all()


if __name__ == '__main__':
    app.run()
