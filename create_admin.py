from hangman import app, db
from hangman.models.account import Account


def create_admin():
    with app.app_context():
        db.create_all()
        if not Account.query.filter_by(email="yakovsolo@gmail.com").first():
            Account.create_admin(
                name="Admin",
                surname="Admin",
                email="admin@admin.com",
                password="admin",
            )


if __name__ == "__main__":
    create_admin()
