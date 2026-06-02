from dataclasses import dataclass


@dataclass
class ARDSModel:
    """
    Models ARDS severity and its physiological impact.
    """

    severity: str = "moderate"

    def __post_init__(self):
        """
        Validate severity after object creation.
        """
        valid_levels = ["mild", "moderate", "severe"]

        if self.severity.lower() not in valid_levels:
            raise ValueError(
                f"Severity must be one of {valid_levels}"
            )

    def get_compliance_factor(self) -> float:
        """
        Returns lung compliance reduction factor based on ARDS severity.
        """

        severity_map = {
            "mild": 0.7,
            "moderate": 0.45,
            "severe": 0.2
        }

        return severity_map[self.severity.lower()]

    def get_oxygen_transfer_efficiency(self) -> float:
        """
        Returns oxygen transfer efficiency based on ARDS severity.
        """

        efficiency_map = {
            "mild": 0.75,
            "moderate": 0.55,
            "severe": 0.35
        }

        return efficiency_map[self.severity.lower()]

    def get_state(self) -> dict:
        """
        Returns ARDS physiological impact summary.
        """

        return {
            "severity": self.severity,
            "compliance_factor": self.get_compliance_factor(),
            "oxygen_transfer_efficiency": self.get_oxygen_transfer_efficiency()
        }