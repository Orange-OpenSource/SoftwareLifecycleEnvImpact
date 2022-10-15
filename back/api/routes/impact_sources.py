from typing import Any
from impacts_model.impact_sources import get_all_impact_sources


def get_impact_sources() -> Any:
    """
    GET /impactsources/
    :return: all ImpactSource names
    """
    impact_sources = get_all_impact_sources()
    return impact_sources
