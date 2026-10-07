class Repuesto:
    def __init__(self, codigo: str, nombre: str, stock: int, es_importado: bool, precio:float):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__stock = stock
        self.__es_importado = es_importado
        self.__precio =precio

    def precio_en_pesos(self, dolar:float)->int:
        if self.__es_importado:
            return round(self.__precio*dolar)
        return round(self.__precio)
    
    @property
    def codigo(self) -> str:
        return self.__codigo

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def es_importado(self) -> bool:
        return self.__es_importado

    def hay_stock(self) -> bool:
        return self.__stock > 0
