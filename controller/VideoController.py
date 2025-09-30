from moviepy import VideoClip, TextClip, CompositeVideoClip
from moviepy.video.fx.MultiplySpeed import MultiplySpeed
from controller.utils.VarConstraintChecker import constraintPositiveNumber, constraintNotEmptyText, \
	constraintPourcentageNumber

from .utils.VarConstraintChecker import constraintPositiveNumber, constraintNotEmptyText

def cutVideo(video: VideoClip, cuttingFrame: int, framerate: int) -> tuple[VideoClip, VideoClip]:
	"""Cut a part of a VideoClip & returns it

    Args:
        video (VideoClip): VideoClip object that will be cutted
        cuttingFrame (int): Frame that will be used to cut the video
        framerate (int): Video framerate
    Returns:
        tuple[VideoClip, VideoClip]: 2 VideoClips, one before & one after the cut
        
    Raises:
        :exception If the cutting frame is lower or equal the video duration
    """
	videoDuration = video.duration * framerate
	if videoDuration <= cuttingFrame:
		raise Exception('Cutting time cannot be higher than video duration.')
	
	beforeCut = video.subclipped(0, cuttingFrame / framerate)
	afterCut = video.subclipped(videoDuration - (cuttingFrame / framerate), videoDuration)
	return beforeCut, afterCut


def addingText(video: VideoClip, frames: int, framerate: int, text: str, position: str = 'center', fontsize: int = 16,
               color: str = 'black') -> VideoClip:
	"""Cut a part of a VideoClip & returns it
	
	Args:
		video (VideoClip): VideoClip object that will be cutted
		frames (int): Duration the text will be shown (in frames)
		framerate (int): Video framerate
		text (str): Text to be shown
		position (str): Text positioning
		fontsize (int): Text size
		color (str): Text color
	Returns:
    	VideoClip: Clip with the text added to it
    """
	constraintPositiveNumber(frames)
	constraintPositiveNumber(framerate)
	constraintPositiveNumber(fontsize)
	constraintNotEmptyText(text)
	constraintNotEmptyText(position)
	constraintNotEmptyText(color)
	
	txtClip = TextClip(text=text, font_size=fontsize, color=color)
	txtClip = txtClip.with_position(position).with_duration(frames / framerate)
	
	# Overlay the text clip on the first video clip
	return CompositeVideoClip([video, txtClip])


def changeVideoSpeed(video: VideoClip, newspeed: float) -> VideoClip:
	"""Change video speed & returns it

		Args:
			video (VideoClip): VideoClip object that will be cutted
			newspeed (float): New clip speed (between 0 & 1)
		Returns:
	    	VideoClip: New clip with changed speed
	    """
	constraintPourcentageNumber(newspeed)
	return VideoClip(MultiplySpeed(newspeed).apply(video))
