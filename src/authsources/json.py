import jsonschema_rs
from frozendict import frozendict
from functools import cached_property
from jsonschema_rs import ValidationError


class ValidationErrors(Exception):

    errors: list[ValidationError]

    def __init__(self, *errors: ValidationError):
        self.errors = errors

    def __iter__(self):
        return iter(self.errors)

    def __len__(self):
        return len(self.errors)


class JSONSchema(frozendict):

    @cached_property
    def validator(self):
        return jsonschema_rs.validator_for(self)

    def validate(self, instance) -> ValidationErrors | None:
        errors = list(self.validator.iter_errors(instance))
        if errors:
            raise ValidationErrors(*errors)
