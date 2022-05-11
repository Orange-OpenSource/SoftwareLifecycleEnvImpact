from typing import Any, List

from pint import Quantity

from impacts_model.impacts.impact_factors import ImpactFactor
from impacts_model.impacts.impacts import ImpactIndicator, ImpactsList, merge_impacts_lists
from impacts_model.quantities import Q_

ResourceName = str

ResourcesList = dict[ResourceName, ImpactsList]


def merge_resource_list(
    first_list: ResourcesList, second_list: ResourcesList
) -> ResourcesList:
    """
    Merge two list of Resource, adding them if they are in each list or merge them
    :param first_list: first list to merge
    :param second_list: second list to merge with
    :return: a new list containing the parameters merged
    """

    result = {**first_list, **second_list}
    for resource_name, _ in result.items():
        if resource_name in first_list and resource_name in second_list:
            result[resource_name] = merge_impacts_lists(
                first_list[resource_name], second_list[resource_name]
            )
    return result


class Resource:

    """
    Abstract definition of a resource, with a quantity and one or multiple ImpactFactor
    Should not be directly instantiated
    """

    def __init__(self, name: ResourceName, impacts: List[ImpactFactor], quantity: float = 1.0):
        """
        Should only be used by implementations, define the name and impacts_sources of the resource
        :param name: name of the resource
        :param impacts: list of resource ImpactSources
        """
        self.name = name
        self._impacts = impacts
        self._quantity = quantity

    @property
    def quantity(self) -> float:
        """
        Quantity consumed by the resource, define by implementations
        :return: implementation quantity
        """
        return self._quantity

    def get_impact(self, impact_indicator: ImpactIndicator) -> Quantity[Any]:
        """
        Compute and return the corresponding indicator impact associated to the given quantity
        :return: the impact
        """
        impacts: List[Quantity[Any]] = [
            i.impacts_list[impact_indicator] * self.quantity for i in self._impacts
        ]

        return Q_(sum(impacts))

    def get_impacts(self) -> ImpactsList:
        """
        Return all impacts_list for the resource, with the format ImpactsList For each impact kind, it's multiplied by the
        resource quantity example:
        >>> self.get_impacts()
         {
            'Climate change': <Quantity(10000.123, 'kg_co2e')>,
            'Natural resources depletion': <Quantity(0, 'kg_Sbe')>,
            'Acidification': <Quantity(0,'mol_Hpos')>,
            'Fine particles': <Quantity(0, 'disease_incidence')>,
            'Ionizing radiations': <Quantity(0, 'kg_Bq_u235e')>,
            'Water depletion': <Quantity(0, 'cubic_meter')>,
            'Electronic waste': <Quantity(0, 'electronic_waste')>,
            'Primary energy consumption': <Quantity(0, 'primary_MJ')>,
            'Raw materials': <Quantity(213.3, 'tonne_mips')>
         }
        :return: ImpactsList for the resource
        """
        impacts: ImpactsList = {}

        for impact_source in self._impacts:
            impact_source_quantities = {}

            for impact_indicator in impact_source.impacts_list:
                impact_source_quantities[impact_indicator] = (
                    impact_source.impacts_list[impact_indicator] * self.quantity
                )

            impacts = merge_impacts_lists(impacts, impact_source_quantities)

        return impacts
