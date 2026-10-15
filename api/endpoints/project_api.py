from api.base_client import BaseAPIClient
from api.models import ProjectCreatePayload, ProjectResponse
from playwright.sync_api import APIResponse


class ProjectAPI(BaseAPIClient):
    ENDPOINT = "/posts"

    def create_project(self, payload: ProjectCreatePayload) -> ProjectResponse:
        response = self.post(self.ENDPOINT, data=payload.model_dump())
        assert response.ok, f"Failed to create record: {response.status} - {response.text()}"
        return ProjectResponse(**response.json())

    def get_project_raw(self, record_id: str) -> APIResponse:
        return self.get(f"{self.ENDPOINT}/{record_id}")

    def delete_project(self, record_id: str) -> APIResponse:
        return self.delete(f"{self.ENDPOINT}/{record_id}")