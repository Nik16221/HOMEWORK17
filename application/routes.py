from flask_restx import Api, Namespace, Resource
from flask import current_app as app, request
from application import models, schema
from application.models import db

api: Api = app.config["api"]

#Создаем неймспейс для разделов
movies_ns: Namespace = api.namespace("movies")
directors_ns = api.namespace("directors")
genres_ns = api.namespace("genres")

movies_schema = schema.Movie(many=True)
movie_schema = schema.Movie()
directors_schema = schema.Director(many=True)
director_schema = schema.Director()
genres_schema = schema.Genre(many=True)
genre_schema = schema.Genre()


@genres_ns.route("/")
#Создаем представление для вывода информации по всем жанрам и методы get, post
class GenresView(Resource):
    @genres_ns.response(200, description="Возвращает список всех жанров")
    #добавляем описание кода в swagger
    def get(self): #вывод информации о жанре
        genres = db.session.query(models.Genre).all()

        return genres_schema.dump(genres), 200

    @directors_ns.response(201, description="Жанр добавлен")
    #добавляем описание кода в swagger
    def post(self): #добавление жанра в базу
        genre = genre_schema.load(request.json)
        db.session.add(models.Genre(**genre))
        db.session.commit()

        return "Жанр добавлен", 201


@genres_ns.route("/<genre_id>/")
#Создаем представление для вывода информации о жанре по его ID и метод к get к нему
class GenreView(Resource):
    @genres_ns.response(200, description="Возвращает жанр по его ID")
    @genres_ns.response(404, description="Нет такого жанра!")
    #добавляем описание кода в swagger
    def get(self, genre_id): #вывод информации о конкретном жанре(по ID)
        genre = db.session.query(models.Genre).filter(models.Genre.id == genre_id).first()
        if genre is None:

            return "Нет такого жанра!", 404

        return genre_schema.dump(genre), 200

    @genres_ns.response(400, description="Неверное обновление информации")
    @genres_ns.response(200, description="Жанр изменен")
    #добавляем описание кода в swagger
    def put(self, genre_id): #вносим изменения о жанре в базе
        put_row = db.session.query(models.Genre).filter(models.Genre.id == genre_id).update(request.json)
        if put_row != 1:

            return "Неверное обновление информации", 400

        db.session.commit()

        return "Жанр изменен", 200

    @genres_ns.response(400, description="Неверное удаление информации")
    @genres_ns.response(200, description="Жанр удален")
    #добавляем описание кода в swagger
    def delete(self, genre_id): #удаляем информацию о жанре
        delete_row = db.session.query(models.Genre).filter(models.Genre.id == genre_id).delete()
        if delete_row != 1:

            return "Неверное удаление информации", 400

        db.session.commit()

        return "Информация о жанре удалена!", 200


@directors_ns.route("/")
#Создаем представление для вывода информации о режессерах, методы get, post
class DirectorsView(Resource):
    @directors_ns.response(200, description="Возвращает режессера по его ID")
    #добавляем описание кода в swagger
    def get(self): #выводим информацию о всех режессерах
        directors = db.session.query(models.Director).all()

        return directors_schema.dump(directors), 200

    @directors_ns.response(201, description="Режессер добавлен")
    #добавляем описание кода в swagger
    def post(self): #добавляем режессера
        director = director_schema.load(request.json)
        db.session.add(models.Director(**director))
        db.session.commit()

        return "Режессер добавлен", 201


@directors_ns.route("/<int:director_id>/")
#Создаем представление для вывода информации о режессере по его ID, методы get, put, delete
class DirectorView(Resource):
    @directors_ns.response(200, description="Возвращает режессера по его ID")
    @directors_ns.response(404, description="Нет такого режессера!")
    #добавляем описание кода в swagger
    def get(self, director_id): #выводим информацию о конкретном режессере(по ID)
        director = db.session.query(models.Director).filter(models.Director.id == director_id).first()
        if director is None:

            return "Нет такого режессера!", 404

        return director_schema.dump(director), 200

    @directors_ns.response(200, description="Информация о режессере обновлена")
    @directors_ns.response(400, description="Неверное обновление информации")
    #добавляем описание кода в swagger
    def put(self, director_id): #вносим изменения в данные конкретного режессера
        put_row = db.session.query(models.Director).filter(models.Director.id == director_id).update(request.json)
        if put_row != 1:

            return "Неверное обновление информации", 400

        db.session.commit()

        return "Информация о режессере обновлена!", 200

    @directors_ns.response(200, description="Информация о режессере удалена")
    @directors_ns.response(400, description="Неверное удаление информации")
    #добавляем описание кода в swagger
    def delete(self, director_id): #удаляем режессера из базы
        put_row = db.session.query(models.Director).filter(models.Director.id == director_id).delete()
        if put_row != 1:

            return "Неверное удаление информации", 400

        db.session.commit()

        return "Информация о режессере удалена!", 200


@movies_ns.route("/")
#Создаем представление для вывода информации о всех фильмах
class MoviesView(Resource):
    @movies_ns.response(200, description="Возвращает список фильмов")
    #добавляем описание кода в swagger
    def get(self): #выводим информацию о фильмах, можно использовать 2 фильтра: director_id и genre_id(вместе или отдельно)
        movies_query = db.session.query(models.Movie)

        args = request.args

        director_id = args.get("director_id")
        if director_id is not None:
            movies_query = movies_query.filter(models.Movie.director_id == director_id)
        genre_id = args.get("genre_id")
        if genre_id is not None:
            movies_query = movies_query.filter(models.Movie.genre_id == genre_id)
        movies = movies_query.all()

        return movies_schema.dump(movies), 200

    @movies_ns.response(201, description="Фильм добавлен")
    #добавляем описание кода в swagger
    def post(self): #добавляем фильм в базу
        movie = movie_schema.load(request.json)
        db.session.add(models.Movie(**movie))
        db.session.commit()

        return "Фильм добавлен!", 201


@movies_ns.route("/<int:movie_id>/")
#Создаем представление для вывода информации о фильме по его ID
class MovieView(Resource):
    @movies_ns.response(404, description="Нет такого фильма")
    @movies_ns.response(200, description="Возвращает фильм по ID")
    #добавляем описание кода в swagger
    def get(self, movie_id): #выводим информацию конкретном фильме(по ID)
        movie = db.session.query(models.Movie).filter(models.Movie.id == movie_id).first()
        if movie is None:

            return "Нет такого фильма!", 404

        return movie_schema.dump(movie), 200

    @movies_ns.response(400, description="Неверное обновление информации (обновлено несколько строк)")
    @movies_ns.response(200, description="Информация о фильме обновлена")
    #добавляем описание кода в swagger
    def put(self, movie_id): #вносим изменения в информацию о фильме(по ID)
        put_row = db.session.query(models.Movie).filter(models.Movie.id == movie_id).update(request.json)
        if put_row != 1:

            return "Неверное обновление информации", 400

        db.session.commit()

        return "Информация о фильме обновлена!", 200

    @movies_ns.response(200, description="Фильм удален")
    @movies_ns.response(400, description="Неверное удаление информации (удалено несколько строк)")
    #добавляем описание кода в swagger
    def delete(self, movie_id): #удаляем фильм из базы
        delete_row = db.session.query(models.Movie).filter(models.Movie.id == movie_id).delete()
        if delete_row != 1:

            return "Неверное обновление информации", 400

        db.session.commit()

        return "Фильм удален!", 200
