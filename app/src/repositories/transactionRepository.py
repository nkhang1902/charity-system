from app.src.models.transaction import Transaction
from app.src.models.transaction import TransactionQueryParams
from app.src.providers.mysql import MySQL
from app.src.models.user import User
from app.src.models.campaign import Campaign

class TransactionRepository:
    def __init__(self, db: MySQL):
        self.db = db

    @staticmethod
    def map_campaign(r):
        if r.get("campaign_id") is None:
            return None

        return Campaign(
            id=r.get("campaign_id"),
            title=r.get("campaign_title") or "",
            description=r.get("campaign_description"),
            goal_amount=r.get("campaign_goal_amount"),
            current_amount=r.get("campaign_current_amount"),
            start_date=r.get("campaign_start_date"),
            end_date=r.get("campaign_end_date"),
            status=r.get("campaign_status"),
            media_url=r.get("campaign_media_url"),
            org_id=r.get("campaign_org_id"),
            created_at=r.get("campaign_created_at"),
            updated_at=None,
            deleted_at=None,
            organization=None
        )

    def getList(self, params: TransactionQueryParams | None = None) -> list[Transaction]:
        query = """
                SELECT t.*,
                   u.id          AS user_id,
                   u.name        AS user_name,
                   u.avatar_url  AS user_avatar_url,
                   c.id          AS campaign_id,
                   c.title       AS campaign_title,
                   c.description AS campaign_description,
                   c.goal_amount AS campaign_goal_amount,
                   c.current_amount AS campaign_current_amount,
                   c.start_date AS campaign_start_date,
                   c.end_date AS campaign_end_date,
                   c.media_url AS campaign_media_url,
                   c.status AS campaign_status,
                   c.org_id AS campaign_org_id,
                   c.created_at AS campaign_created_at
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
            tx_fields = {k: r.get(k) for k in Transaction.__annotations__}
            tx = Transaction(**tx_fields)

            tx.user = User(
                id=r["user_id"],
                name=r["user_name"],
                avatar_url=r["user_avatar_url"]
            )

            tx.campaign = self.map_campaign(r)

            result.append(tx)

        return result

    def getById(self, id: str):
        query = """
                SELECT t.*,
                   u.id          AS user_id,
                   u.name        AS user_name,
                   u.avatar_url  AS user_avatar_url,
                   c.id          AS campaign_id,
                   c.title       AS campaign_title,
                   c.description AS campaign_description,
                   c.goal_amount AS campaign_goal_amount,
                   c.current_amount AS campaign_current_amount,
                   c.start_date AS campaign_start_date,
                   c.end_date AS campaign_end_date,
                   c.media_url AS campaign_media_url,
                   c.status AS campaign_status,
                   c.org_id AS campaign_org_id,
                   c.created_at AS campaign_created_at
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

        tx.campaign = self.map_campaign(r)

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
