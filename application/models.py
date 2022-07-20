from application.app import db


class Movie(db.Model):
    #Создаем модель Movie, для описания данных в таблице movie
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))

    director = db.relationship("Director") #таблица movie ссылается на таблицу director
    genre = db.relationship("Genre") #таблица movie ссылается на таблицу genre


class Director(db.Model):
    #Создаем модель Director, для описания данных в таблице director
    __tablename__ = 'director'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    #Создаем модель Genre, для описания данных в таблице genre
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
