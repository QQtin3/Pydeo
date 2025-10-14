from enum import Enum
from typing import Any


class VideoEffectEnum(Enum):
    
    SPEED = 1
    BLACK_AND_WHITE = 2
    CONTRAST = 3
    SATURATION = 4
    ROTATION = 5
    
class AudioEffectEnum(Enum):
    pass
    
class VideoEffect:
    effect: VideoEffectEnum
    params: dict[str, Any]
    
    def __init__(self, effect: VideoEffectEnum, params: dict[str, Any]) -> None:
        self.effect = effect
        self.params = params
        
class AudioEffect:
    effect: AudioEffectEnum
    params: dict[str, Any]
    
    def __init__(self, effect: AudioEffectEnum, params: dict[str, Any]) -> None:
        self.effect = effect
        self.params = params

