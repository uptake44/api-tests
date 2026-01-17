from faker import Faker

from services.university.helpers.group_helper import GroupHelper

fake = Faker()


class TestGroupContract:
    def test_create_group_anonym(self, university_api_utils_anonym):
        group_helper = GroupHelper(api_utils=university_api_utils_anonym)

        response = group_helper.post_group(
            {
                "name": fake.name(),
            }
        )

        assert response.status_code == 401, (
            f"Wrong status code. Actual: {response.status_code}"
            f"Expected: 401"
        )
