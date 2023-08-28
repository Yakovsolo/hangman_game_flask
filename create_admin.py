from hangman import db, app
from hangman.models.account import Account


def run_migration():
    with app.app_context():
        db.create_all()
        if not Account.query.filter_by(email="yakovsolo@gmail.com").first():
            Account.create_admin(
                name="Admin",
                surname="Admin",
                email="yakovsolo@gmail.com",
                password="111",
            )


if __name__ == "__main__":
    run_migration()
