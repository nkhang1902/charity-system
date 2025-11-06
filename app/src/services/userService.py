from app.src.repositories.userRepository import UserRepository
from app.src.models.user import User

class UserService:
    def __init__(self, userRepository: UserRepository):
        self.userRepo = userRepository

    def getById(self, id: int) -> User | None:
        return self.userRepo.getById(id)