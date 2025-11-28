class MissingParameterError(Exception):
    def __init__(self, parameter: str):
        self.parameter = parameter
        super().__init__(f"Missing required parameter: {parameter}")


class BusinessError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.status_code = status_code
        super().__init__(message)


class EntityNotFoundError(BusinessError):
    def __init__(self, entity_name: str, entity_id: str):
        message = f"{entity_name} with ID '{entity_id}' not found."
        super().__init__(message, status_code=404)


class EntityAlreadyExistsError(BusinessError):
    def __init__(self, entity_name: str, identifier: str = ""):
        message = f"{entity_name} already exists."
        if identifier:
            message = f"{entity_name} with identifier '{identifier}' already exists."
        super().__init__(message, status_code=409)
