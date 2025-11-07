from app.src.models.transaction import Transaction
from app.src.models.transaction import TransactionQueryParams
from app.src.providers.mysql import MySQL

class TransactionRepository:
    def __init__(self, db: MySQL):
        self.db = db

    def getList(self, params: TransactionQueryParams | None = None) -> list[Transaction]:
        query = """
            SELECT *
            FROM transactions
        """
        conditions = []
        values = []

        if params:
            if params.user_id:
                placeholders = ", ".join(["%s"] * len(params.user_id))
                conditions.append(f"user_id IN ({placeholders})")
                values.extend(params.user_id)

            if params.campaign_id:
                placeholders = ", ".join(["%s"] * len(params.campaign_id))
                conditions.append(f"campaign_id IN ({placeholders})")
                values.extend(params.campaign_id)

            if params.status:
                placeholders = ", ".join(["%s"] * len(params.status))
                conditions.append(f"status IN ({placeholders})")
                values.extend(params.status)

            if params.min_amount:
                conditions.append("amount >= %s")
                values.append(params.min_amount)

            if params.max_amount:
                conditions.append("amount <= %s")
                values.append(params.max_amount)

            if params.from_timestamp:
                conditions.append("timestamp >= %s")
                values.append(params.from_timestamp)

            if params.to_timestamp:
                conditions.append("timestamp <= %s")
                values.append(params.to_timestamp)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY timestamp DESC"

        result = self.db.executeQuery(query, tuple(values))
        return [Transaction(**item) for item in result]

    def getById(self, id: str) -> Transaction | None:
        query = """
            SELECT *
            FROM transactions
            WHERE id = %s
            LIMIT 1
        """
        result = self.db.executeQuery(query, (id,))
        return Transaction(**result[0]) if result else None

    def create(self, payload: dict):
        columns = ", ".join(payload.keys())
        placeholders = ", ".join(["%s"] * len(payload))
        values = list(payload.values())

        query = f"""
            INSERT INTO transactions ({columns})
            VALUES ({placeholders})
        """

        result = self.db.executeQuery(query, tuple(values))
        return result


    def update(self, id: str, payload: dict):
        set_clause = ", ".join([f"{col} = %s" for col in payload.keys()])
        values = list(payload.values())
        values.append(id)

        query = f"""
            UPDATE transactions
            SET {set_clause}, updated_at = NOW()
            WHERE id = %s
        """

        result = self.db.executeQuery(query, tuple(values))
        return result


    def delete(self,id: str):
        query = """
            UPDATE transactions
            SET deleted_at = NOW()
            WHERE id = %s
        """
        result = self.db.executeQuery(query, (id))
        return result
