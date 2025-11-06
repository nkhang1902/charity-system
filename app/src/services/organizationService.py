from app.src.repositories.organizationRepository import OrganizationRepository
from app.src.models.organization import Organization
from app.src.models.organization import OrganizationQueryParams

class OrganizationService:
    def __init__(self, organizationRepository: OrganizationRepository):
        self.organizationRepo = organizationRepository

    def getById(self, id: str) -> Organization | None:
        return self.organizationRepo.getById(id)

    def getList(self, params: OrganizationQueryParams | None = None) -> list[Organization]:
        return self.organizationRepo.getList(params)

    def create(self, payload: dict):
        return self.organizationRepo.create(payload)

    def update(self, id: str, payload: dict):
        return self.organizationRepo.update(id, payload)

    def delete(self, id: str):
        return self.organizationRepo.delete(id)