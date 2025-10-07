from moviepy import CompositeVideoClip, VideoClip, VideoFileClip, AudioClip, AudioFileClip, ImageClip
from .utils.Exceptions import UnhandledFileFormatException
import os

def readVideoFile(path: str) -> tuple[VideoClip, AudioClip | None, int]:
    """Open a video file and return VideoClip and AudioClip objects (if audio is available in the video file)

    Args:
        path (str): the path of the file. Supported formats are .mp4, .avi, .mkv, .mov, .flv, .wmv and .webm.

    Returns:
        tuple[VideoClip, AudioClip | None, int]: Clips and framerate extracted from the given file
        
    Raises:
        FileNotFoundError: The specified location is not an existing file
        UnhandledFileFormatException: The specified file extension is not supported
    """
    if not os.path.isfile(path):
        raise FileNotFoundError("Given path is not a file")
    
    if os.path.splitext(path)[1] not in [".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv", ".webm"]:
        raise UnhandledFileFormatException("Wrong video file format. Supported formats are .mp4, .avi, .mkv, .mov, .flv, .wmv and .webm")
    
    clip = VideoFileClip(path)
    audio = clip.audio
    
    return clip, audio, clip.fps

def readAudioFile(path: str) -> tuple[AudioClip, int]:
    """Open an audio file and return AudioClip object

    Args:
        path (str): the path of the file. Supported formats are .mp3, .wav, .aac, .ogg, .flac and .opus.

    Returns:
        tuple[AudioClip, int]: Clips extracted from the given file and its frequency
        
    Raises:
        FileNotFoundError: The specified location is not an existing file
        UnhandledFileFormatException: The specified file extension is not supported
    """
    if not os.path.isfile(path):
        raise FileNotFoundError("Given path is not a file")
    
    if os.path.splitext(path)[1] not in [".mp3", ".wav", ".aac", ".ogg", ".flac", ".opus"]:
        raise UnhandledFileFormatException("Wrong video file format. Supported formats are .mp3, .wav, .aac, .ogg, .flac and .opus")
    
    audio = AudioFileClip(path)
    
    return audio, audio.fps

def readImageFile(path: str) -> ImageClip:
    """Open an image file and return ImageClip object

    Args:
        path (str): the path of the file. Supported formats are .jpg, .png, .gif, .bmp and .tiff

    Returns:
        tuple[VideoClip, AudioClip | None]: Clips extracted from the given file
        
    Raises:
        FileNotFoundError: The specified location is not an existing file
        UnhandledFileFormatException: The specified file extension is not supported
    """
    if not os.path.isfile(path):
        raise FileNotFoundError("Given path is not a file")
    
    if os.path.splitext(path)[1] not in [".jpg", ".png", ".gif", ".bmp", ".tiff"]:
        raise UnhandledFileFormatException("Wrong video file format. Supported formats are .jpg, .png, .gif, .bmp and .tiff")
    
    image = ImageClip(path)
    return image

def exportVideo(clips: CompositeVideoClip, path: str) -> None:
    """Export Composite clip to video file at the specified location

    Args:
        clips (CompositeVideoClip): The array of clips
        path (str): The path of the file to export

    Raises:
        FileExistsError: The specified location is already an existing file
        UnhandledFileFormatException: The specified file extension is not supported
    """
    if not os.path.isfile(path):
        raise FileExistsError("File already exists")
    
    if os.path.splitext(path)[1] not in [".mp3", ".wav", ".aac", ".ogg", ".flac", ".opus"]:
        raise UnhandledFileFormatException("Wrong video file format. Supported formats are .mp3, .wav, .aac, .ogg, .flac and .opus")
    
    clips.write_videofile(path)