class Persona:

    def __init__(self, nombre: str, rut: str):
        self.nombre = nombre
        self.rut = rut

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        valor = str(valor).strip()
        if len(valor) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres.")
        if not valor.replace(" ", "").isalpha():
            raise ValueError("El nombre solo puede contener letras.")
        self._nombre = valor

    @property
    def rut(self):
        return self._rut

    @rut.setter
    def rut(self, valor):
        valor = str(valor).strip()
        if not valor:
            raise ValueError("El RUT no puede estar vacío.")
        if "-" not in valor or len(valor) < 8:
            raise ValueError("El RUT debe incluir guión y tener un formato válido (Ej: 11111111-1).")
        self._rut = valor 