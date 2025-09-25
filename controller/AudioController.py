from moviepy import VideoClip
from moviepy.Clip import Clip

from .utils.VarConstraintChecker import constraintPourcentageNumber


def changeAudioVolume(video: VideoClip, volume: float) -> Clip:
	constraintPourcentageNumber(volume)
	return video.with_volume_scaled(volume)
