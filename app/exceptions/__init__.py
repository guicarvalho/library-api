import re

from sqlalchemy.exc import IntegrityError


class IntegrityErrorParser:
    def __init__(self, exc: IntegrityError):
        self.exc = exc
        self.orig_msg = str(exc.orig)

    def is_foreign_key_violation(self) -> bool:
        return "foreign key constraint" in self.orig_msg.lower()

    def is_unique_violation(self) -> bool:
        return "unique constraint" in self.orig_msg.lower()

    def extract_fk_details(self):
        match = re.search(
            r'Key \((.*?)\)=\((.*?)\) is not present in table "(.*?)"',
            self.orig_msg,
        )
        if match:
            field, value, related_table = match.groups()
            return {
                "field": field,
                "value": value,
                "related_table": related_table,
                "type": "foreign_key",
            }
        return None

    def extract_unique_violation(self):
        match = re.search(
            r'duplicate key value violates unique constraint "(.*?)"',
            self.orig_msg,
        )
        if match:
            constraint = match.group(1)
            return {"constraint": constraint, "type": "unique"}
        return None

    def build_exception_message(self):
        if self.is_foreign_key_violation():
            details = self.extract_fk_details()
            return (
                f"The value '{details['value']}' informed to the field "
                f"'{details['field']}' does not exists in the table "
                f"'{details['related_table']}'."
            )
        elif self.is_unique_violation():
            details = self.extract_unique_violation()
            return f"Unique constraint violation ({details['constraint']})."
        else:
            return "Error of integrity in the data sent."


class GenericError(Exception):
    def __init__(self, detail: str, code: int | None = None) -> None:
        self.detail = detail
        self.code = code
