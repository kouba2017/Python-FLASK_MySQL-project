from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
class Show:
    def __init__(self,data) :
        self.id= data['id']
        self.title=data['title']
        self.network=data['network']
        self.description=data['description']
        self.release_date=data['release_date']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id=data['user_id']
        self.creator_id=user.User.get_by_id({'id':self.user_id}).id
    @classmethod
    def get_all(cls):
        query="SELECT*FROM shows"
        results=connectToMySQL('tv_shows').query_db(query)
        shows=[]
        for row in results:
            shows.append(cls(row))
        return shows
#******Create Show******
    @classmethod
    def create_show(cls, data):
        query ="INSERT INTO shows ( title,network, description,release_date,user_id) VALUES  (%(title)s,%(network)s, %(description)s, %(release_date)s, %(user_id)s) ;"
        return connectToMySQL('tv_shows').query_db(query,data)
#******GET Show by id******
    @classmethod
    def get_by_id(cls,data):
        query="SELECT*FROM shows WHERE id=%(id)s;"
        results = connectToMySQL('tv_shows').query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])
#******UPDATE Show******
    @classmethod
    def update(cls,data):
        query="UPDATE shows SET  title = %(title)s, network=%(network)s,description = %(description)s, release_date = %(release_date)s  WHERE id = %(id)s ;  " 
        return connectToMySQL('tv_shows').query_db(query,data)
#******DELETE Show******
    @classmethod
    def delete(cls,data):
        query="DELETE FROM shows WHERE id=%(id)s;"
        return connectToMySQL('tv_shows').query_db(query,data)
#******VALIDATIONS******
    @staticmethod
    def validate(show):
        is_valid = True
        if len(show['title'])<3:
            flash("Title must be at least 3 characters")
            is_valid = False
        if len(show['description'])<3:
            flash("Description must be at least 3 characters")
            is_valid = False
        if len(show['network'])<3:
            is_valid = False
            flash("Network must be at least 3 characters" )
        if show["release_date"] == "":
            is_valid = False
            flash("Release Date must not be blank **")
        return is_valid
