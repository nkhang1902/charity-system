from src.models.organization import Organization
from src.providers.mysql import MySQL

class OrganizationRepository:
    def __init__(self, db: MySQL):
        self.db = db

    def getList(self) -> list[Organization]:
        query = """
            SELECT *
            FROM organizations
            WHERE deleted_at IS NULL
        """
        result = self.db.executeQuery(query)
        return [Organization(**item) for item in result]

    def getById(self, id: str) -> Organization | None:
        query = """
            SELECT *
            FROM organizations
            WHERE id = %s AND deleted_at IS NULL
            LIMIT 1
        """
        result = self.db.executeQuery(query, (id,))
        return Organization(**result[0]) if result else None

    def create(self, payload: dict):
        if not payload:
            raise ValueError("Payload is empty")

        columns = ", ".join(payload.keys())
        placeholders = ", ".join(["%s"] * len(payload))
        values = list(payload.values())

        query = f"""
            INSERT INTO organizations ({columns})
            VALUES ({placeholders})
        """

        result = self.db.executeQuery(query, tuple(values))
        return result


    def update(self, id: str, payload: dict):
        if not payload:
            raise ValueError("Payload is empty")

        set_clause = ", ".join([f"{col} = %s" for col in payload.keys()])
        values = list(payload.values())
        values.append(id)

        query = f"""
            UPDATE organizations
            SET {set_clause}, updated_at = NOW()
            WHERE id = %s
        """

        result = self.db.executeQuery(query, tuple(values))
        return result


    def delete(self,id: str):
        query = """
            UPDATE organizations
            SET deleted_at = NOW()
            WHERE id = %s AND deleted_at IS NULL
        """
        result = self.db.executeQuery(query, (id))
        return result
