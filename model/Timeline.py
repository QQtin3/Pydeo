import os

from model.TimelineClip import TimelineClip, TimelineVideoClip, TimelineAudioClip
from controller.utils.fileExtensions import isFileVideo

class Timeline:
    clips: list[TimelineClip]
    
    def __init__(self) -> None:
        pass
    
    def addClip(self, path: str) -> None:
        nom = ' '.join(os.path.splitext(os.path.basename(path))[:-1])
        start = 0
        if len(self.clips) != 0:
            lastElement = self.clips[-1]
            start = lastElement.end
        
        isVideo = isFileVideo(path)
        if isVideo:
            self.clips.append(TimelineVideoClip(nom,start, path))
        else:
            self.clips.append(TimelineAudioClip(nom,start, path))

    def delClip(self, path: str) -> None:
        """Supprime un clip de la timeline selon son chemin de fichier."""
        if not self.clips:
            return

        for clip in self.clips:
            if clip.path == path:
                self.clips.remove(clip)
                print(f"Clip supprimé : {clip.name}")
                break
        else:
            print(f"Aucun clip trouvé pour le chemin : {path}")

        
