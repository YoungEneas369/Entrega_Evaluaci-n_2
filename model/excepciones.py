class AgenciaError(Exception):
    """Excepción base para el sistema de agencia de viajes."""
    pass


class AnticipoInsuficienteError(AgenciaError):
    pass


class SinCuposError(AgenciaError):
    pass


class RecursoNoEncontradoError(AgenciaError):
    pass


class APITipoCambioError(AgenciaError):
    pass


class ValidacionError(AgenciaError):
    pass


class AutenticacionError(AgenciaError):
    pass