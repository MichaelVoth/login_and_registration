from flask_app.config.mysqlconnection import connectToMySQL

class Planet:
    DB = "login_and_register_schema"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.users = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_planets(cls):
        query = '''SELECT * FROM planets;'''
        results = connectToMySQL(cls.DB).query_db(query)

        return results
        