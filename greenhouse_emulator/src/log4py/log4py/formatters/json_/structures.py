import json
from dataclasses import asdict, dataclass

from .. import structures as base_struct


@dataclass(slots=True)
class LogJSON(base_struct.Log):
    def to_value_only_dict(self) -> dict:
        return asdict(
            self,
            dict_factory=lambda x: {k: v for (k, v) in x if v is not None},
        )

    def __str__(self) -> str:
        return json.dumps(self.to_value_only_dict(), ensure_ascii=False)
