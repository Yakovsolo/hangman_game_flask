from hangman import db, app

# Создаем таблицы в базе данных
with app.app_context():
    db.create_all()
