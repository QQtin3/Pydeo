import os


def isFileAudio(path: str) -> bool:
	return os.path.splitext(path)[1] in [".mp3", ".wav", ".aac", ".ogg", ".flac", ".opus"]


def isFileVideo(path: str) -> bool:
	return os.path.splitext(path)[1] in [".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv", ".webm"]