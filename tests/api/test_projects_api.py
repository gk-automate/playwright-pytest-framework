import pytest
from faker import Faker
from api.endpoints.project_api import ProjectAPI
from api.models import ProjectCreatePayload

fake = Faker()


@pytest.mark.api
@pytest.mark.smoke
def test_create_and_verify_project_api(project_api: ProjectAPI):
    payload = ProjectCreatePayload(
        title=f"API-Release-{fake.uuid4()[:8]}",
        body="Automated API contract test via Playwright APIRequestContext",
        userId=1
    )

    # 1. POST & validate Pydantic schema
    created = project_api.create_project(payload)
    assert created.title == payload.title
    assert created.id is not None

    # 2. GET existing record
    get_res = project_api.get_project_raw(1)
    assert get_res.status == 200

    # 3. DELETE record
    del_res = project_api.delete_project(created.id)
    assert del_res.status == 200