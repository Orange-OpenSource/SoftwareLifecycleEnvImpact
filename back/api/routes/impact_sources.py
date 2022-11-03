from typing import Any
from impacts_model.impact_sources import impact_sources


def get_impact_sources() -> Any:
    """
    GET /impactsources/
    :return: all ImpactSource names
    """
    impact_source_dict = {}
    for impact_source in impact_sources:
        impact_source_dict[impact_source.id] = impact_source.name
    return impact_source_dict
