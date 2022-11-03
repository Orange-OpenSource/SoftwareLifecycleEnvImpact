from typing import Any
from impacts_model.impact_sources import impact_sources


def get_impact_sources() -> Any:
    """
    GET /impactsources/
    :return: all ImpactSource names
    """
    return impact_sources
