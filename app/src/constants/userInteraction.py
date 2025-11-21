from enum import Enum

class TargetType(str, Enum):
    CAMPAIGN = "campaign"
    ORGANIZATION = "organization"

class ActionType(str, Enum):
    CLICK = "click"
    SEARCH = "search"
    VOTE = "vote"
    DONATE = "donate"
    SHARE = "share"

WeightMapping = {
    ActionType.CLICK: 1,
    ActionType.SEARCH: 1,
    ActionType.VOTE: 1,
    ActionType.DONATE: 4,
    ActionType.SHARE: 3,
}