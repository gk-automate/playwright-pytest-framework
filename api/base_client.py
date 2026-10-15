from typing import Any, Dict, Optional
from playwright.sync_api import APIRequestContext, APIResponse
from utils.logger import get_logger
import allure

logger = get_logger(__name__)


class BaseAPIClient:
    def __init__(self, request_context: APIRequestContext):
        self.request = request_context

    def _log_and_attach(self, method: str, endpoint: str, response: APIResponse, payload: Any = None) -> None:
        status = response.status
        logger.info(f"API {method} {endpoint} -> Status: {status}")
        
        with allure.step(f"API {method} {endpoint} [{status}]"):
            if payload:
                allure.attach(str(payload), name="Request Payload", attachment_type=allure.attachment_type.JSON)
            try:
                allure.attach(
                    str(response.json()), 
                    name="Response Body", 
                    attachment_type=allure.attachment_type.JSON
                )
            except Exception:
                allure.attach(response.text(), name="Response Text", attachment_type=allure.attachment_type.TEXT)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> APIResponse:
        response = self.request.get(endpoint, params=params)
        self._log_and_attach("GET", endpoint, response)
        return response

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> APIResponse:
        response = self.request.post(endpoint, data=data)
        self._log_and_attach("POST", endpoint, response, payload=data)
        return response

    def delete(self, endpoint: str) -> APIResponse:
        response = self.request.delete(endpoint)
        self._log_and_attach("DELETE", endpoint, response)
        return response