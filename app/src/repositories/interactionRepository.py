from app.src.models.userInteraction import UserInteraction
from app.src.providers.mysql import MySQL

class InteractionRepository:
    def __init__(self, db: MySQL):
        self.db = db

    def create(self, payload: dict):
        columns = ", ".join(payload.keys())
        placeholders = ", ".join(["%s"] * len(payload))
        values = list(payload.values())

        query = f"""
            INSERT INTO user_interactions ({columns})
            VALUES ({placeholders})
        """

        result = self.db.executeQuery(query, tuple(values))
        return result