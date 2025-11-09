from moviepy import VideoClip, TextClip, CompositeVideoClip
from moviepy.Clip import Clip
from moviepy.video.fx.MultiplySpeed import MultiplySpeed
from moviepy.video.fx.BlackAndWhite import BlackAndWhite
from moviepy.video.fx.LumContrast import LumContrast
from moviepy.video.fx.Painting import Painting
from moviepy.video.fx.Rotate import Rotate
from controller.utils.VarConstraintChecker import constraintPositiveNumber, constraintNotEmptyText, \
	constraintPourcentageNumber

from .utils.VarConstraintChecker import constraintPositiveNumber, constraintNotEmptyText

from model.Effects import VideoEffectEnum


def apply_video_effects(video_clip, effects):
	"""Apply all stored VideoEffects sequentially."""
	for eff in effects:
		if eff.effect == VideoEffectEnum.BLACK_AND_WHITE:
			video_clip = videoBlackWhiteEffect(video_clip)
		elif eff.effect == VideoEffectEnum.SPEED:
			speed = eff.params.get("speed", 1.0)
			video_clip = videoSpeedEffect(video_clip, speed)
		elif eff.effect == VideoEffectEnum.CONTRAST:
			lum = eff.params.get("lum", 0)
			contrast = eff.params.get("contrast", 1)
			video_clip = videoContrastEffect(video_clip, lum, contrast)
		elif eff.effect == VideoEffectEnum.SATURATION:
			saturation = eff.params.get("saturation", 1)
			video_clip = videoSaturationEffect(video_clip, saturation)
		elif eff.effect == VideoEffectEnum.ROTATION:
			rotation = eff.params.get("rotation", 0)
			video_clip = videoRotationEffect(video_clip, rotation)
	return video_clip


# --- Helper Function ---
def frames_to_timecode(frames, fps=24) -> str:
	seconds = frames // fps
	frames_rem = frames % fps
	hours = seconds // 3600
	minutes = (seconds % 3600) // 60
	seconds_rem = seconds % 60
	return f"{hours:02}:{minutes:02}:{seconds_rem:02}:{frames_rem:02}"


def seconds_to_frames(seconds: float, fps=24) -> int:
	seconds = float(round(seconds, 2))

	return int(round(seconds * fps))


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


def videoSpeedEffect(video: VideoClip, newspeed: float) -> Clip:
	"""Change video speed & returns it

		Args:
			video (VideoClip): VideoClip object that will be cutted
			newspeed (float): New clip speed (between 0 & 1)
		Returns:
			Clip: New clip with changed speed
		"""
	constraintPourcentageNumber(newspeed)
	return MultiplySpeed(newspeed).apply(video)


def videoBlackWhiteEffect(video: VideoClip) -> Clip:
	"""Apply the black & white effect on a video clip

	Args:
		video (VideoClip): The clip to apply on the effect

	Returns:
		Clip: The video clip with the applied effect
	"""
	return BlackAndWhite().apply(video)


def videoContrastEffect(video: VideoClip, lum: float, contrast: float) -> Clip:
	"""Apply the contrast effect with given parameters to the video clip

	Args:
		video (VideoClip): The clip to apply on the effect
		lum (float): Luminosity of the clip
		contrast (float): Contrast of the clip

	Returns:
		Clip: The video clip with the applied effect
	"""
	return LumContrast(lum, contrast).apply(video)


def videoSaturationEffect(video: VideoClip, saturation: float) -> Clip:
	"""Apply the saturation effect with given parameters to the video clip

	Args:
		video (VideoClip): The clip to apply on the effect
		saturation (float): Saturation of the clip

	Returns:
		Clip: The video clip with the applied effect
	"""
	return Painting(saturation).apply(video)


def videoRotationEffect(video: VideoClip, rotation: float) -> Clip:
	"""Apply the saturation effect with given parameters to the video clip

	Args:
		video (VideoClip): The clip to apply on the effect
		rotation (float): Rotation of the clip (in degrees)

	Returns:
		Clip: The video clip with the applied effect
	"""

	return Rotate(rotation).apply(video)
