from app.src.models.transaction import Transaction
from app.src.models.transaction import TransactionQueryParams
from app.src.providers.mysql import MySQL
from app.src.models.user import User
from app.src.models.campaign import Campaign

class TransactionRepository:
    def __init__(self, db: MySQL):
        self.db = db

    def getList(self, params: TransactionQueryParams | None = None) -> list[Transaction]:
        query = """
                SELECT t.*,
                       u.name        AS user_name,
                       u.avatar_url  AS user_avatar_url,
                       c.title       AS campaign_title,
                       c.description AS campaign_description
                FROM transactions t
                         LEFT JOIN users u ON u.id = t.user_id
                         LEFT JOIN campaigns c ON c.id = t.campaign_id
                """
        conditions = []
        values = []

        if params:
            if params.user_id:
                placeholders = ", ".join(["%s"] * len(params.user_id))
                conditions.append(f"t.user_id IN ({placeholders})")
                values.extend(params.user_id)

            if params.campaign_id:
                placeholders = ", ".join(["%s"] * len(params.campaign_id))
                conditions.append(f"t.campaign_id IN ({placeholders})")
                values.extend(params.campaign_id)

            if params.status:
                placeholders = ", ".join(["%s"] * len(params.status))
                conditions.append(f"t.status IN ({placeholders})")
                values.extend(params.status)

            if params.min_amount:
                conditions.append("t.amount >= %s")
                values.append(params.min_amount)

            if params.max_amount:
                conditions.append("t.amount <= %s")
                values.append(params.max_amount)

            if params.from_timestamp:
                conditions.append("t.timestamp >= %s")
                values.append(params.from_timestamp)

            if params.to_timestamp:
                conditions.append("t.timestamp <= %s")
                values.append(params.to_timestamp)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY t.timestamp DESC"

        rows = self.db.executeQuery(query, tuple(values))

        result = []
        for r in rows:
            tx_fields = {k: r[k] for k in Transaction.__annotations__ if k in r}
            tx = Transaction(**tx_fields)

            tx.user = User(
                id=r["user_id"],
                name=r["user_name"],
                avatar_url=r["user_avatar_url"]
            )

            tx.campaign = Campaign(
                id=r["campaign_id"],
                title=r["campaign_title"],
                description=r["campaign_description"],
                org_id=None
            )

            result.append(tx)

        return result

    def getById(self, id: str):
        query = """
                SELECT t.*, \
                       u.id          AS user_id, \
                       u.name        AS user_name, \
                       u.avatar_url  AS user_avatar_url, \
                       c.id          AS campaign_id, \
                       c.title       AS campaign_title, \
                       c.description AS campaign_description
                FROM transactions t
                         LEFT JOIN users u ON u.id = t.user_id
                         LEFT JOIN campaigns c ON c.id = t.campaign_id
                WHERE t.id = %s LIMIT 1 \
                """

        result = self.db.executeQuery(query, (id,))
        if not result:
            return None

        r = result[0]

        tx_fields = {k: r[k] for k in Transaction.__annotations__ if k in r}
        tx = Transaction(**tx_fields)

        tx.user = User(
            id=r["user_id"],
            name=r["user_name"],
            avatar_url=r["user_avatar_url"]
        )

        tx.campaign = Campaign(
            id=r["campaign_id"],
            title=r["campaign_title"],
            description=r["campaign_description"],
            org_id=None
        )

        return tx

    def create(self, payload: dict):
        columns = ", ".join(payload.keys())
        placeholders = ", ".join(["%s"] * len(payload))
        values = list(payload.values())

        query = f"""
            INSERT INTO transactions ({columns})
            VALUES ({placeholders})
        """

        cursor = self.db.connection.cursor()
        cursor.execute(query, tuple(values))
        self.db.connection.commit()

        last_id = cursor.lastrowid
        cursor.close()

        return last_id

    def update(self, id: str, payload: dict):
        set_clause = ", ".join([f"{col} = %s" for col in payload.keys()])
        values = list(payload.values())
        values.append(id)

        query = f"""
            UPDATE transactions
            SET {set_clause}
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
