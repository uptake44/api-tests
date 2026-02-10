import pytest

from university.conftest import university_admin_service


@pytest.mark.positive
@pytest.mark.business
class TestGradesStatsPositive:
    def test_grades_stats_count(
            self,
            university_admin_service,
            created_grades
    ):
        grades_response = university_admin_service.get_grades()
        stats_response = university_admin_service.get_grades_stats()

        actual_count = len(grades_response.grades)

        assert actual_count == stats_response.count, (
            "Grade count doesn't match\n"
            f"Actual: {stats_response.count}\n"
            f"Expected: {len(grades_response.grades)}"
        )

    def test_grades_stats_avg(
            self,
            university_admin_service,
            created_grades
    ):
        stats_response = university_admin_service.get_grades_stats()

        actual_avg = stats_response.avg
        expected_avg = (sum(created_grades) / len(created_grades))

        assert actual_avg == expected_avg, (
            "Grades average isn't correct\n"
            f"Actual: {actual_avg}\n"
            f"Expected: {expected_avg}"
        )

    def test_grades_stats_min(
            self,
            university_admin_service,
            created_grades
    ):
        stats_response = university_admin_service.get_grades_stats()

        actual_min = stats_response.min
        expected_min = (min(created_grades))

        assert actual_min == expected_min, (
            "Grades minimal value isn't correct\n"
            f"Actual: {actual_min}\n"
            f"Expected: {expected_min}"
        )

    def test_grades_stats_max(
            self,
            university_admin_service,
            created_grades
    ):
        stats_response = university_admin_service.get_grades_stats()

        actual_max = stats_response.max
        expected_max = (max(created_grades))

        assert actual_max == expected_max, (
            "Grades maximum value isn't correct\n"
            f"Actual: {actual_max}\n"
            f"Expected: {expected_max}"
        )


@pytest.mark.positive
@pytest.mark.business
class TestGradesStatsFilter:
    def test_grades_stats_filter_by_student(
            self,
            university_admin_service,
            created_student,
            student_grades
    ):
        stats_response = university_admin_service.get_grades_stats(
            student_id=created_student.id,
        )
        expected_student_grade_count = len(student_grades)

        assert stats_response.count == expected_student_grade_count, (
            f"Grades count doesn't match\n"
            f"Actual: {stats_response.count}\n"
            f"Expected: {expected_student_grade_count}"
        )
