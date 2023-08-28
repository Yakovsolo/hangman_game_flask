import create_admin
from hangman import app, db
from hangman.models.account import Account

if __name__ == "__main__":
    app.run()
    with app.app_context():
        db.create_all()
        if not Account.query.filter_by(email="yakovsolo@gmail.com").first():
            create_admin.run_migration()
