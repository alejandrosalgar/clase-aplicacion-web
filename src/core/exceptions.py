"""
Excepciones de aplicación para manejo unificado de errores en la API.
Cada excepción se traduce a una respuesta HTTP con estructura estándar.
"""


class AppException(Exception):
    """Base para excepciones de la API con código HTTP y mensaje."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        code: str | None = None,
        details: dict | list | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.code = code or "ERROR"
        self.details = details
        super().__init__(message)


class NotFoundError(AppException):
    """Recurso no encontrado (404)."""

    def __init__(self, message: str = "Recurso no encontrado", details: dict | list | None = None):
        super().__init__(message=message, status_code=404, code="NOT_FOUND", details=details)


class ConflictError(AppException):
    """Conflicto: recurso duplicado o regla de negocio (409 o 400)."""

    def __init__(self, message: str, status_code: int = 409, details: dict | list | None = None):
        super().__init__(message=message, status_code=status_code, code="CONFLICT", details=details)


class BadRequestError(AppException):
    """Solicitud inválida (400)."""

    def __init__(self, message: str, details: dict | list | None = None):
        super().__init__(message=message, status_code=400, code="BAD_REQUEST", details=details)


class ValidationError(AppException):
    """Error de validación de datos (422)."""

    def __init__(self, message: str, details: dict | list | None = None):
        super().__init__(message=message, status_code=422, code="VALIDATION_ERROR", details=details)
