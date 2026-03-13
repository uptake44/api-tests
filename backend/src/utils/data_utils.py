from faker import Faker

fake = Faker()


class DataUtils:
    @staticmethod
    def get_password(
            length: int = 32,
            special_chars: bool = True,
            digits: bool = True,
            upper_case: bool = True,
            lower_case: bool = True,
    ) -> str:
        return fake.password(
            length=length,
            special_chars=special_chars,
            digits=digits,
            upper_case=upper_case,
            lower_case=lower_case,
        )
