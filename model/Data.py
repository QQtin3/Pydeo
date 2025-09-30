class Data:
    def __init__(self):
        self.assets = []
        self.tracks = []

    # Méthodes existantes pour les assets (non modifiées)
    def addToAssets(self, file_path):
        for asset in self.assets:
            if asset['path'] == file_path:
                return
        new_id = max([asset['id'] for asset in self.assets], default=-1) + 1
        self.assets.append({"id": new_id, "path": file_path})

    def removeFromAssets(self, file_path):
        asset_id = None
        for asset in self.assets:
            if asset['path'] == file_path:
                asset_id = asset['id']
                break
        if asset_id is not None:
            self.removeFromAssetsById(asset_id)

    def removeFromAssetsById(self, id):
        self.assets = [asset for asset in self.assets if asset['id'] != id]
        for track in self.tracks:
            track['elems'] = [elem for elem in track['elems'] if elem['asset'] != id]



    # Nouvelles méthodes pour gérer les pistes
    def addTrack(self, name, type_):
        """Ajoute une nouvelle piste avec un nom et un type spécifiés"""
        self.tracks.append({
            "name": name,
            "type": type_,
            "elems": []
        })

    def removeTrackByIndex(self, index):
        """Supprime une piste par son index"""
        if 0 <= index < len(self.tracks):
            del self.tracks[index]

    def removeTrackByName(self, name):
        """Supprime toutes les pistes ayant le nom spécifié"""
        self.tracks = [track for track in self.tracks if track['name'] != name]

    def addElementToTrack(self, track_index, time, asset_id, effects, start_at, end_at):
        """
        Ajoute un élément à une piste
        :param effects: Liste d'effets au format [{"name": "...", "keyframes": [...]}] ou [{"name": "...", "config": {...}}]
        """
        if not (0 <= track_index < len(self.tracks)):
            return
            
        # Vérification basique de l'existence de l'asset
        if not any(asset['id'] == asset_id for asset in self.assets):
            raise ValueError(f"Asset ID {asset_id} does not exist")
            
        self.tracks[track_index]['elems'].append({
            "time": time,
            "asset": asset_id,
            "effects": effects,
            "start_at": start_at,
            "end_at": end_at
        })

    def removeElementFromTrack(self, track_index, element_index):
        """Supprime un élément d'une piste par index"""
        if not (0 <= track_index < len(self.tracks)):
            return
        elems = self.tracks[track_index]['elems']
        if 0 <= element_index < len(elems):
            del elems[element_index]

    def updateElementInTrack(self, track_index, element_index, **kwargs):
        """
        Met à jour les propriétés d'un élément
        Exemple : updateElementInTrack(0, 0, time=10000, start_at=10)
        """
        if not (0 <= track_index < len(self.tracks)):
            return
        elems = self.tracks[track_index]['elems']
        if not (0 <= element_index < len(elems)):
            return
            
        element = elems[element_index]
        valid_keys = ['time', 'asset', 'effects', 'start_at', 'end_at']
        
        for key, value in kwargs.items():
            if key in valid_keys:
                if key == 'asset':
                    # Vérification de l'existence de l'asset
                    if not any(asset['id'] == value for asset in self.assets):
                        raise ValueError(f"Asset ID {value} does not exist")
                element[key] = value