from moviepy import VideoClip, TextClip


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
    txtClip = TextClip(text=text, font_size=fontsize, color="white")
    
    # Say that you want it to appear for 10s at the center of the screen
    txt_clip = txt_clip.with_position("center").with_duration(10)
    
    # Overlay the text clip on the first video clip
    video = CompositeVideoClip([clip, txt_clip])
