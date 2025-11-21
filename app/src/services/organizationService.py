from app.src.repositories.organizationRepository import OrganizationRepository
from app.src.models.organization import Organization
from app.src.models.organization import OrganizationQueryParams
from app.src.constants.userInteraction import TargetType
from app.src.jobs.writeEmbedding import write_embedding


class OrganizationService:
    def __init__(self, organizationRepository: OrganizationRepository):
        self.organizationRepo = organizationRepository

    def getById(self, id: str) -> Organization | None:
        return self.organizationRepo.getById(id)

    def getList(self, params: OrganizationQueryParams | None = None) -> list[Organization]:
        return self.organizationRepo.getList(params)

    def create(self, payload: dict):
        data = self.organizationRepo.create(payload)
        write_embedding({
            "entityType": TargetType.ORGANIZATION,
            "id": str(data.id),
            "isDeleted": False,
            "data":  {"name": data.name, "description": data.description, "category": data.category}
        })
        return data

    def update(self, id: str, payload: dict):
        data = self.organizationRepo.update(id, payload)
        write_embedding({
            "entityType": TargetType.ORGANIZATION,
            "id": str(data.id),
            "isDeleted": False,
            "data":  {"name": data.name, "description": data.description, "category": data.category}
        })
        return data

    def delete(self, id: str):
        data = self.organizationRepo.delete(id)
        write_embedding({
            "entityType": TargetType.ORGANIZATION,
            "id": str(data.id),
            "isDeleted": True,
            "data":  {"name": data.name, "description": data.description, "category": data.category}
        })
        return data