from app.src.repositories.interactionRepository import InteractionRepository
from app.src.models.userInteraction import UserInteraction
from app.src.services.recommendation import RecommendationService


class InteractionService:
    def __init__(self, interactionRepository: InteractionRepository):
        self.interactionRepo = interactionRepository
        self.recommendation = RecommendationService()

    def create(self, payload: dict):
        return self.interactionRepo.create(payload)
