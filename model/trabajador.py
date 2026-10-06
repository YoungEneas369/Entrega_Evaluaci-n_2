from model.persona import Persona


class Trabajador(Persona):

    def __init__(
        self,
        nombre: str,
        rut: str,
        usuario: str,
        password_hash: str
    ):
        super().__init__(nombre, rut)

        self.usuario = usuario
        self.password_hash = password_hash

    @property
    def usuario(self):
        return self._usuario

    @usuario.setter
    def usuario(self, valor):
        valor = valor.strip()

        if len(valor) < 3:
            raise ValueError(
                "El usuario debe tener al menos 3 caracteres."
            )

        self._usuario = valor

    @property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, valor):

        if not valor:
            raise ValueError(
                "La contraseña protegida es obligatoria."
            )

        self._password_hash = valor 