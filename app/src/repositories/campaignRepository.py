from app.src.models.campaign import Campaign
from app.src.models.campaign import CampaignQueryParams
from app.src.providers.mysql import MySQL
from app.src.models.organization import Organization

class CampaignRepository:
    def __init__(self, db: MySQL):
        self.db = db

    def getList(self, params: CampaignQueryParams | None = None) -> list[dict]:
        query = """
                SELECT c.*,
                       o.id            AS org_id,
                       o.name          AS org_name,
                       o.description   AS org_description,
                       o.logo_url      AS org_logo_url,
                       o.website_url   AS org_website_url,
                       o.contact_email AS org_contact_email,
                       o.category      AS org_category,
                       o.rating        AS org_rating,
                       o.vote_count    AS org_vote_count
                FROM campaigns c
                         LEFT JOIN organizations o ON o.id = c.org_id
                WHERE c.deleted_at IS NULL
                """
        conditions = []
        values = []

        if params:
            if params.q:
                conditions.append("c.description LIKE %s")
                values.append(f"%{params.q}%")

            if params.id:
                placeholders = ", ".join(["%s"] * len(params.id))
                conditions.append(f"c.id IN ({placeholders})")
                values.extend(params.id)

            if params.org_id:
                placeholders = ", ".join(["%s"] * len(params.org_id))
                conditions.append(f"c.org_id IN ({placeholders})")
                values.extend(params.org_id)

            if params.status:
                placeholders = ", ".join(["%s"] * len(params.status))
                conditions.append(f"c.status IN ({placeholders})")
                values.extend(params.status)

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += " ORDER BY c.created_at DESC"

        rows = self.db.executeQuery(query, tuple(values))
        result = []

        for r in rows:
            camp_fields = {k: r[k] for k in Campaign.__annotations__ if k in r}
            camp = Campaign(**camp_fields)

            camp.organization = Organization(
                id=r["org_id"],
                name=r["org_name"],
                description=r["org_description"],
                logo_url=r["org_logo_url"],
                website_url=r["org_website_url"],
                contact_email=r["org_contact_email"],
                category=r["org_category"],
                rating=r["org_rating"],
                vote_count=r["org_vote_count"]
            )

            result.append(camp)

        return result

    def getById(self, id: str) -> dict | None:
        query = """
                SELECT c.*,
                       o.id            AS org_id,
                       o.name          AS org_name,
                       o.description   AS org_description,
                       o.logo_url      AS org_logo_url,
                       o.website_url   AS org_website_url,
                       o.contact_email AS org_contact_email,
                       o.category      AS org_category,
                       o.rating        AS org_rating,
                       o.vote_count    AS org_vote_count
                FROM campaigns c
                         LEFT JOIN organizations o ON o.id = c.org_id
                WHERE c.id = %s \
                  AND c.deleted_at IS NULL LIMIT 1
                """

        result = self.db.executeQuery(query, (id,))
        if not result:
            return None

        r = result[0]

        camp_fields = {k: r[k] for k in Campaign.__annotations__ if k in r}
        camp = Campaign(**camp_fields)

        camp.organization = Organization(
            id=r["org_id"],
            name=r["org_name"],
            description=r["org_description"],
            logo_url=r["org_logo_url"],
            website_url=r["org_website_url"],
            contact_email=r["org_contact_email"],
            category=r["org_category"],
            rating=r["org_rating"],
            vote_count=r["org_vote_count"]
        )

        return camp

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
            WHERE id = %s AND deleted_at IS NULL
        """

        result = self.db.executeQuery(query, tuple(values))
        return result


    def delete(self,id: str):
        query = """
            UPDATE campaigns
            SET deleted_at = NOW()
            WHERE id = %s AND deleted_at IS NULL
        """
        result = self.db.executeQuery(query, (id,))
        return result
