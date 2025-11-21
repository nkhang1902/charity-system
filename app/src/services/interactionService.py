from app.src.repositories.interactionRepository import InteractionRepository
from app.src.models.userInteraction import UserInteraction

class InteractionService:
    def __init__(self, interactionRepository: InteractionRepository):
        self.interactionRepo = interactionRepository

    def create(self, payload: dict):
        return self.interactionRepo.create(payload)
