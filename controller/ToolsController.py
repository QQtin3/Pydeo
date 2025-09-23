from moviepy import VideoClip


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