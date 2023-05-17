class Role:
    def __init__(self, rol):
        self.rol = rol


class Permissions:
    def __init__(self, permiso):
        self.permiso = permiso


class User:
    def __init__(self, name, username, password, role):
        self.name = name
        self.username = username
        self.password = password
        self.role = role