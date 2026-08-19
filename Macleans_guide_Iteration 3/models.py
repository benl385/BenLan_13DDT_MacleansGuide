# models.py

class User:
    # Represents a logged in user.
    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username

class LocationMarker:
    # Represents a clickable marker on the school map.
    def __init__(self, marker_id: int, name: str, x_coord: int, y_coord: int):
        self.id = marker_id
        self.name = name
        self.x = x_coord
        self.y = y_coord