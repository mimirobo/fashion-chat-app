import re
import html

from abc import ABC, abstractmethod
from typing import Tuple, List


class StreamValidator(ABC):
    """
    Abstract base class for stream validators.
    """

    @abstractmethod
    def validate(self, data: str) -> Tuple[bool, str]:
        """
        Validate the stream and return a tuple of (is_valid, error_message).
        """
        pass


class StreamLengthValidator(StreamValidator):
    """
    stream validator for checking the stream length.
    """

    def __init__(self, max_length: int):
        self.max_length = max_length

    def validate(self, data: str) -> Tuple[bool, str]:
        if len(data) > self.max_length:
            return (
                False,
                f"Stream size exceeds the maximum of {self.max_length}",
            )
        return True, ""


class StreamRegexValidator(StreamValidator):
    """
    Concrete stream validator for checking regular expressions.
    """

    def __init__(self, allowed_pattern: str):
        self.allowed_pattern = re.compile(allowed_pattern)

    def validate(self, data: str) -> Tuple[bool, str]:
        if self.allowed_pattern.match(data):
            return True, ""
        return (False, "Invalid stream format")


class HTMLEscapeValidator(StreamValidator):
    """
    Concrete stream validator for checking HTML escape codes.
    """

    def validate(self, data: str) -> Tuple[bool, str]:
        try:
            html.escape(data)
            return True, ""
        except Exception:
            return False, "Input stream sounds malicious"


class CompositeStreamValidator(StreamValidator):
    """
    Composite stream validator that combines multiple stream validators.
    """

    def __init__(self, validators: List[StreamValidator]):
        self.validators = validators

    def validate(self, data: str) -> Tuple[bool, str]:
        for validator in self.validators:
            is_valid, error_message = validator.validate(data)
            if not is_valid:
                return is_valid, error_message
        return True, ""


class StreamValidatorBuilder:
    """
    Builder class for creating a composite stream validator.
    """

    def __init__(self):
        self.validators = []

    def add_length_validator(self, max_length: int) -> "StreamValidatorBuilder":
        self.validators.append(StreamLengthValidator(max_length))
        return self

    def add_regex_validator(self, allowed_pattern: str) -> "StreamValidatorBuilder":
        self.validators.append(StreamRegexValidator(allowed_pattern))
        return self

    def add_html_escape_validator(self):
        self.validators.append(HTMLEscapeValidator())
        return self

    def build(self) -> CompositeStreamValidator:
        """
        Create a composite file validator.
        """
        return CompositeStreamValidator(self.validators)
