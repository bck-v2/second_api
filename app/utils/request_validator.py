from datetime import datetime
from pyramid.httpexceptions import HTTPBadRequest


class RequestValidator:
    def __init__(self, request=None, **fields):
        self.request = request
        self.invalid = []
        self.validated = {}
        self.fields = fields or {}  # Allows for dynamic fields

    def validate_date_format(self, param_name):
        """Validate if the date is in ISO format."""
        date_str = self.request.GET.get(param_name)
        try:
            # If the date exists, attempt to parse it
            self.validated[param_name] = (
                datetime.fromisoformat(date_str) if date_str else None
            )
        except ValueError:
            # If parsing fails, add an error message
            self.invalid.append(
                f"Invalid date format for {param_name}. Please use (YYYY-MM-DD) format."
            )

    def validate_number(self, param_name):
        """Validate if the field is a number."""
        value = self.request.GET.get(param_name)

        if value:
            try:
                # Try to convert the value to a float (covers both integer and decimal numbers)
                float(value)
            except ValueError:
                self.invalid.append(f"{param_name} must be a valid number.")
            else:
                # If valid, store it as a float in the validated dictionary
                self.validated[param_name] = float(value)
        else:
            self.validated[param_name] = None

    def validate_required_field(self, param_name):
        """Validate if the field is required."""

        if param_name not in self.request.GET or not self.request.GET[param_name]:
            self.invalid.append(f"{param_name} is required")
        else:
            self.validated[param_name] = self.request.GET[param_name]

    def validate(self):
        if self.fields:
            for key, rules in self.fields.items():
                for rule in rules.split(","):
                    if rule == "required":
                        self.validate_required_field(key)
                    elif rule == "date":
                        self.validate_date_format(key)
                    elif rule == "number":
                        self.validate_number(key)

            if self.invalid:
                raise HTTPBadRequest(
                    f"Validation fields error: {' '.join(self.invalid)}"
                )
            return self.validated
