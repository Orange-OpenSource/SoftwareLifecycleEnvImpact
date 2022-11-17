from typing import Any
from impacts_model.impact_sources import ImpactSourceSchema, impact_sources


def get_impact_sources() -> Any:
    """
    GET /impactsources/
    :return: all ImpactSource names
    """
    schema = ImpactSourceSchema(many=True)
    return schema.dump(impact_sources)
