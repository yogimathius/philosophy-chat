"""Global error handlers for the Philosophy Chat API."""

import logging
import traceback
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, OperationalError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


class BusinessLogicError(Exception):
    """Custom exception for business logic errors."""
    
    def __init__(self, message: str, error_code: str = "BUSINESS_ERROR", status_code: int = 400):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(message)


def create_error_response(
    status_code: int,
    message: str,
    error_code: str = "UNKNOWN_ERROR",
    details: Any = None,
    request_id: str = None,
) -> JSONResponse:
    """Create a standardized error response."""
    error_data: Dict[str, Any] = {
        "success": False,
        "error": {
            "code": error_code,
            "message": message,
            "status_code": status_code,
        }
    }
    
    if details:
        error_data["error"]["details"] = details
    
    if request_id:
        error_data["error"]["request_id"] = request_id
        
    return JSONResponse(
        status_code=status_code,
        content=error_data
    )


def add_error_handlers(app: FastAPI) -> None:
    """Add global error handlers to the FastAPI app."""
    
    @app.exception_handler(BusinessLogicError)
    async def business_logic_error_handler(request: Request, exc: BusinessLogicError):
        """Handle custom business logic errors."""
        logger.warning(f"Business logic error: {exc.message}")
        return create_error_response(
            status_code=exc.status_code,
            message=exc.message,
            error_code=exc.error_code,
        )
    
    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        """Handle Pydantic validation errors."""
        logger.warning(f"Validation error: {exc}")
        errors = []
        for error in exc.errors():
            field = " -> ".join(str(x) for x in error["loc"])
            errors.append(f"{field}: {error['msg']}")
        
        return create_error_response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Validation failed",
            error_code="VALIDATION_ERROR",
            details=errors,
        )
    
    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        """Handle database integrity errors."""
        logger.error(f"Database integrity error: {exc}")
        
        # Common integrity error patterns
        error_msg = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
        
        if "unique constraint" in error_msg.lower():
            return create_error_response(
                status_code=status.HTTP_409_CONFLICT,
                message="Resource already exists",
                error_code="DUPLICATE_RESOURCE",
            )
        elif "foreign key constraint" in error_msg.lower():
            return create_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Referenced resource does not exist",
                error_code="INVALID_REFERENCE",
            )
        else:
            return create_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Database constraint violation",
                error_code="DATABASE_CONSTRAINT_ERROR",
            )
    
    @app.exception_handler(OperationalError)
    async def operational_error_handler(request: Request, exc: OperationalError):
        """Handle database operational errors."""
        logger.error(f"Database operational error: {exc}")
        return create_error_response(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            message="Database temporarily unavailable",
            error_code="DATABASE_UNAVAILABLE",
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle FastAPI HTTP exceptions."""
        logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
        return create_error_response(
            status_code=exc.status_code,
            message=exc.detail,
            error_code=f"HTTP_{exc.status_code}",
        )
    
    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle Starlette HTTP exceptions."""
        logger.warning(f"Starlette HTTP exception: {exc.status_code} - {exc.detail}")
        return create_error_response(
            status_code=exc.status_code,
            message=exc.detail,
            error_code=f"HTTP_{exc.status_code}",
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all other exceptions."""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        
        # In production, don't expose internal error details
        if hasattr(request.app.state, 'settings') and request.app.state.settings.environment == 'production':
            message = "Internal server error"
            details = None
        else:
            message = str(exc)
            details = traceback.format_exc()
        
        return create_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            error_code="INTERNAL_SERVER_ERROR",
            details=details,
        )


# Convenience functions for raising business logic errors
def raise_not_found(resource: str, identifier: str = "") -> None:
    """Raise a not found error."""
    message = f"{resource} not found"
    if identifier:
        message += f": {identifier}"
    raise BusinessLogicError(message, "RESOURCE_NOT_FOUND", 404)


def raise_already_exists(resource: str, field: str = "", value: str = "") -> None:
    """Raise an already exists error."""
    message = f"{resource} already exists"
    if field and value:
        message += f": {field} = {value}"
    raise BusinessLogicError(message, "RESOURCE_ALREADY_EXISTS", 409)


def raise_unauthorized(action: str = "") -> None:
    """Raise an unauthorized error."""
    message = "Unauthorized"
    if action:
        message += f": {action}"
    raise BusinessLogicError(message, "UNAUTHORIZED", 401)


def raise_forbidden(action: str = "") -> None:
    """Raise a forbidden error."""
    message = "Access forbidden"
    if action:
        message += f": {action}"
    raise BusinessLogicError(message, "FORBIDDEN", 403)


def raise_invalid_operation(operation: str, reason: str = "") -> None:
    """Raise an invalid operation error."""
    message = f"Invalid operation: {operation}"
    if reason:
        message += f" - {reason}"
    raise BusinessLogicError(message, "INVALID_OPERATION", 400)