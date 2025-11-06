from app.src.models.campaign import Campaign
from app.src.models.campaign import CampaignQueryParams
from app.src.models.exception import ApiException
from app.src.constants.errorCode import API_ERROR_CODE
from app.src.providers.mysql import MySQL

class CampaignRepository:
    def __init__(self, db: MySQL):
        self.db = db

    def getList(self, params: CampaignQueryParams | None = None) -> list[Campaign]:
        query = """
            SELECT *
            FROM campaigns
            WHERE deleted_at IS NULL
        """
        conditions = []
        values = []

        if params:
            if params.q != "":
                conditions.append("(name LIKE %s OR description LIKE %s)")
                q = f"%{params.q}%"
                values.extend([q, q, q])

            if params.id:
                placeholders = ", ".join(["%s"] * len(params.id))
                conditions.append(f"id IN ({placeholders})")
                values.extend(params.id)

            if params.org_id:
                placeholders = ", ".join(["%s"] * len(params.org_id))
                conditions.append(f"org_id IN ({placeholders})")
                values.extend(params.org_id)

            if params.status:
                placeholders = ", ".join(["%s"] * len(params.status))
                conditions.append(f"status IN ({placeholders})")
                values.extend(params.status)

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += " ORDER BY created_at DESC"

        result = self.db.executeQuery(query, tuple(values))
        return [Campaign(**item) for item in result]

    def getById(self, id: str) -> Campaign | None:
        query = """
            SELECT *
            FROM campaigns
            WHERE id = %s AND deleted_at IS NULL
            LIMIT 1
        """
        result = self.db.executeQuery(query, (id,))
        return Campaign(**result[0]) if result else None

    def create(self, payload: dict):
        columns = ", ".join(payload.keys())
        placeholders = ", ".join(["%s"] * len(payload))
        values = list(payload.values())

        query = f"""
            INSERT INTO campaigns ({columns})
            VALUES ({placeholders})
        """

        result = self.db.executeQuery(query, tuple(values))
        return result


    def update(self, id: str, payload: dict):
        set_clause = ", ".join([f"{col} = %s" for col in payload.keys()])
        values = list(payload.values())
        values.append(id)

        query = f"""
            UPDATE campaigns
            SET {set_clause}, updated_at = NOW()
            WHERE id = %s
        """

        result = self.db.executeQuery(query, tuple(values))
        return result


    def delete(self,id: str):
        query = """
            UPDATE campaigns
            SET deleted_at = NOW()
            WHERE id = %s AND deleted_at IS NULL
        """
        result = self.db.executeQuery(query, (id))
        return result
