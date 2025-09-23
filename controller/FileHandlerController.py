from moviepy import VideoClip, VideoFileClip, AudioClip, AudioFileClip, ImageClip
import os

def readVideoFile(path: str) -> tuple[VideoClip, AudioClip | None]:
    """Open a video file and return VideoClip and AudioClip objects (if audio is available in the video file)

    Args:
        path (str): the path of the file. Supported formats are .mp4, .avi, .mkv, .mov, .flv, .wmv and .webm.

    Returns:
        tuple[VideoClip, AudioClip | None]: Clips extracted from the given file
    """
    if not os.path.isfile(path):
        raise Exception("Given path is not a file")
    
    if os.path.splitext(path)[1] not in [".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv", ".webm"]:
        raise Exception("Wrong video file format. Supported formats are .mp4, .avi, .mkv, .mov, .flv, .wmv and .webm")
    
    clip = VideoFileClip(path)
    audio = clip.audio
    
    return clip, audio

def readAudioFile(path: str) -> AudioClip:
    """Open an audio file and return AudioClip object

    Args:
        path (str): the path of the file. Supported formats are .mp3, .wav, .aac, .ogg, .flac and .opus.

    Returns:
        tuple[VideoClip, AudioClip | None]: Clips extracted from the given file
    """
    if not os.path.isfile(path):
        raise Exception("Given path is not a file")
    
    if os.path.splitext(path)[1] not in [".mp3", ".wav", ".aac", ".ogg", ".flac", ".opus"]:
        raise Exception("Wrong video file format. Supported formats are .mp3, .wav, .aac, .ogg, .flac and .opus")
    
    audio = AudioFileClip(path)
    
    return audio

def readImageFile(path: str) -> ImageClip:
    """Open an image file and return ImageClip object

    Args:
        path (str): the path of the file. Supported formats are .jpg, .png, .gif, .bmp and .tiff

    Returns:
        tuple[VideoClip, AudioClip | None]: Clips extracted from the given file
    """
    if not os.path.isfile(path):
        raise Exception("Given path is not a file")
    
    if os.path.splitext(path)[1] not in [".jpg", ".png", ".gif", ".bmp", ".tiff"]:
        raise Exception("Wrong video file format. Supported formats are .jpg, .png, .gif, .bmp and .tiff")
    
    image = ImageClip(path)
    return image