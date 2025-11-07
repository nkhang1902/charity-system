from app.src.models.organization import Organization
from app.src.models.organization import OrganizationQueryParams
from app.src.providers.mysql import MySQL

class OrganizationRepository:
    def __init__(self, db: MySQL):
        self.db = db

    def getList(self, params: OrganizationQueryParams | None = None) -> list[Organization]:
        query = """
            SELECT *
            FROM organizations
            WHERE deleted_at IS NULL
        """
        conditions = []
        values = []

        if params:
            if params.q != None and params.q != "":
                conditions.append("(name LIKE %s OR description LIKE %s OR category LIKE %s)")
                q = f"%{params.q}%"
                values.extend([q, q, q])

            if params.id:
                placeholders = ", ".join(["%s"] * len(params.id))
                conditions.append(f"id IN ({placeholders})")
                values.extend(params.id)

            if params.category:
                placeholders = ", ".join(["%s"] * len(params.org_id))
                conditions.append(f"category IN ({placeholders})")
                values.extend(params.org_id)

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += " ORDER BY created_at DESC"

        result = self.db.executeQuery(query, tuple(values))
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
        set_clause = ", ".join([f"{col} = %s" for col in payload.keys()])
        values = list(payload.values())
        values.append(id)

        query = f"""
            UPDATE organizations
            SET {set_clause}, updated_at = NOW()
            WHERE id = %s AND deleted_at IS NULL
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
