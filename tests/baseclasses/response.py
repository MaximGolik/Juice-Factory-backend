from pydantic import ValidationError


class Response:
    def __init__(self, response):
        self.response = response
        self.response_json = response.json
        self.response_status_code = response.status_code

    def validate(self, schema):
        try:
            if isinstance(schema, list):
                for item in self.response_json:
                    schema.model_validate(item)
            else:
                schema.model_validate(self.response_json)
        except ValidationError as exc:
            assert False, f'Field validation error:\n{exc}'

    def assert_status_code(self, status_code):
        if isinstance(status_code, list):
            assert self.response_status_code in status_code, f"\nWrong status code.\nRequest: {self.response.request}" \
                                                             f"\nActual Status code: {self.response_status_code}\n" \
                                                             f"\nExpected code: {status_code}" \
                                                             f"\nMessage: {self.response_json}"
        else:
            assert self.response_status_code == status_code, f"\nWrong status code!\nRequest: {self.response.request}" \
                                                             f"\nActual Status code: {self.response_status_code}" \
                                                             f"\nExpected code: {status_code}" \
                                                             f"\nMessage: {self.response_json}"
        return self


