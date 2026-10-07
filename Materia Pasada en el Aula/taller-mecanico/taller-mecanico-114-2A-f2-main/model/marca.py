class Marca:
    def __init__(self, nombre: str):
        self.__id=None
        self.__nombre = nombre

    @property
    def id(self)->int:
        return self.__id

    @id.setter
    def id(self, valor:int)->None:
        self.__id=valor
    
    @property
    def nombre(self) -> str:
        return self.__nombre
