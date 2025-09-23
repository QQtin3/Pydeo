from moviepy import VideoClip, TextClip, CompositeVideoClip

from controller.utils.VarConstraintChecker import constraintPositiveNumber, constraintNotEmptyText


def cutVideo(video: VideoClip, cuttingTime: int, position='B'):
    """Allow to cut a video with a specified cuttingTime"""
    videoDuration = video.duration
    if videoDuration <= cuttingTime:
        raise Exception('Cutting time cannot be higher than video duration.')
    
    match position:
        case 'B':
            return video.subclipped(0, cuttingTime)
        case 'E':
            return video.subclipped(videoDuration - cuttingTime, videoDuration)
        case _:
            raise Exception('Cutting position', position, 'is not valid.')


def addingText(video: VideoClip, duration: int, text: str, position: str = 'center', fontsize: int = '16',
               color: str = 'black'):
    
    constraintPositiveNumber(duration)
    constraintPositiveNumber(fontsize)
    constraintNotEmptyText(text)
    constraintNotEmptyText(position)
    
    txtClip = TextClip(text=text, font_size=fontsize, color=color)
    txtClip = txtClip.with_position(position).with_duration(duration)
    
    # Overlay the text clip on the first video clip
    return CompositeVideoClip([video, txtClip])
