from app.src.models.user import User
from app.src.providers.mysql import MySQL

class UserRepository:
    def __init__(self, db: MySQL):
        self.db = db

    def getById(self, id: int) -> User | None:
        query = """
            SELECT *
            FROM users
            WHERE id = %s AND deleted_at IS NULL
            LIMIT 1
        """
        result = self.db.executeQuery(query, (id,))
        return User(**result[0]) if result else None
