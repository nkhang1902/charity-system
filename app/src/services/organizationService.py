from src.repositories.organizationRepository import OrganizationRepository
from src.models.organization import Organization

class OrganizationService:
    def __init__(self, organizationRepository: OrganizationRepository):
        self.organizationRepo = organizationRepository

    def getById(self, id: str) -> Organization | None:
        return self.organizationRepo.getById(id)

    def getList(self) -> list[Organization]:
        return self.organizationRepo.getList()

    def create(self, payload: dict):
        return self.organizationRepo.create(payload)

    def update(self, id: str, payload: dict):
        return self.organizationRepo.update(id, payload)

    def delete(self, id: str):
        return self.organizationRepo.delete(id)