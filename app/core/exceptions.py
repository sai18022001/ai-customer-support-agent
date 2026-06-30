from fastapi import HTTPException


class NotFoundError(HTTPException):
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            status_code=404,
            detail=f"{resource} with ID '{resource_id}' not found",
        )


class ValidationError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=400, detail=message)


class AIServiceError(HTTPException):
    def __init__(self, message: str = "AI service temporarily unavailable"):
        super().__init__(status_code=503, detail=message)
