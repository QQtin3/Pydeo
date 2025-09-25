from moviepy import VideoClip
from moviepy.Clip import Clip

from .utils.VarConstraintChecker import constraintPourcentageNumber


def changeAudioVolume(video: VideoClip, volume: float) -> Clip:
	"""Cut a part of a VideoClip & returns it

		Args:
			video (VideoClip): VideoClip object that will be cutted
			volume (float): New volume to be used
		Returns:
	    	Clip: Clip with changed audio volume
	"""
	constraintPourcentageNumber(volume)
	return video.with_volume_scaled(volume)
