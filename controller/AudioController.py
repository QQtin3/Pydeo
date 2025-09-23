from moviepy import VideoClip

from controller.utils.VarConstraintChecker import constraintPourcentageNumber


def changeAudioVolume(video: VideoClip, volume: float) -> VideoClip:
	constraintPourcentageNumber(volume)
	return video.with_volume_scaled(volume)
