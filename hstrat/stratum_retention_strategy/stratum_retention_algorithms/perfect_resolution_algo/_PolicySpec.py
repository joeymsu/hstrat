import typing

from .._detail import PolicySpecABC


@PolicySpecABC.register
class PolicySpec:
    """Contains all policy parameters, if any."""

    def __eq__(self: "PolicySpec", other: typing.Any) -> bool:
        return isinstance(other, PolicySpecABC) and (
            self.GetEvalCtor() == other.GetEvalCtor()
        )

    def __repr__(self: "PolicySpec") -> str:
        return f"""{
            self.GetAlgoIdentifier()
        }.{
            PolicySpec.__qualname__
        }()"""

    def __str__(self: "PolicySpec") -> str:
        return self.GetAlgoTitle()

    def GetEvalCtor(self: "PolicySpec") -> str:
        return f"hstrat.{self!r}"

    @staticmethod
    def GetAlgoIdentifier() -> str:
        """Get programatic name for underlying retention algorithm."""
        return __package__.split(".")[-1]

    @staticmethod
    def GetAlgoTitle() -> str:
        """Get human-readable name for underlying retention algorithm."""
        return "Perfect Resolution Stratum Retention Algorithm"
