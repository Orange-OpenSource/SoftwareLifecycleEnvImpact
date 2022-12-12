from __future__ import annotations

import importlib
import inspect
import re
from impacts_model.impacts import EnvironmentalImpact, ImpactCategory
from pint import Quantity, Unit
from typing import Any, Optional
import yaml
from impacts_model.quantities.quantities import (
    deserialize_quantity,
    deserialize_unit,
)
from marshmallow import Schema, fields


class ImpactSource:
    """
    A source of environmental impact_sources
    """

    def __init__(
        self,
        id: str,
        name: str,
        unit: str,
        climate_change: str,
        resource_depletion: str = "0 " + ImpactCategory.RESOURCE_DEPLETION.value,
        acidification: str = "0 " + ImpactCategory.ACIDIFICATION.value,
        fine_particles: str = "0 " + ImpactCategory.FINE_PARTICLES.value,
        ionizing_radiations: str = "0 " + ImpactCategory.IONIZING_RADIATIONS.value,
        water_depletion: str = "0 " + ImpactCategory.WATER_DEPLETION.value,
        electronic_waste: str = "0 " + ImpactCategory.ELECTRONIC_WASTE.value,
        primary_energy_consumption: str = "0 " + ImpactCategory.PRIMARY_ENERGY.value,
        raw_materials: str = "0 " + ImpactCategory.RAW_MATERIALS.value,
        source: str = "",
        methodology: str = "",
    ):
        """
        :param climate_change: Climate change as kgeqCO2
        :param resource_depletion: Depletion of natural abiotic resources as kgeqSb
        :param acidification: acidification (PEF-AP) as mol H+ eq
        :param ionizing_radiations: ionizing radiations ( PEF-IR) as kBq U235 eq
        :param water_depletion: Depletion of water resources (PEF-WU) as m3 world eq
        :param electronic_waste: mass of electrical and electronic waste generated as Tonne
        :param primary_energy_consumption: Primary energy consumed as MJ
        :param raw_materials: Raw materials consumed as Ton
        """

        if resource_depletion is None:
            resource_depletion = "0 " + ImpactCategory.RESOURCE_DEPLETION.value
        if acidification is None:
            acidification = "0 " + ImpactCategory.ACIDIFICATION.value
        if fine_particles is None:
            fine_particles = "0 " + ImpactCategory.FINE_PARTICLES.value
        if ionizing_radiations is None:
            ionizing_radiations = "0 " + ImpactCategory.IONIZING_RADIATIONS.value
        if water_depletion is None:
            water_depletion = "0 " + ImpactCategory.WATER_DEPLETION.value
        if electronic_waste is None:
            electronic_waste = "0 " + ImpactCategory.ELECTRONIC_WASTE.value
        if primary_energy_consumption is None:
            primary_energy_consumption = "0 " + ImpactCategory.PRIMARY_ENERGY.value
        if raw_materials is None:
            raw_materials = "0 " + ImpactCategory.RAW_MATERIALS.value

        self.id = id
        self.name = name
        self.unit = deserialize_unit(unit)
        # Mandatory to let pint handle the division by unit in parsing,
        # else bug with multi-dimension ones
        self.climate_change = deserialize_quantity(climate_change + "/" + unit)
        self.resource_depletion = deserialize_quantity(resource_depletion + "/" + unit)
        self.acidification = deserialize_quantity(acidification + "/" + unit)
        self.fine_particles = deserialize_quantity(fine_particles + "/" + unit)
        self.ionizing_radiations = deserialize_quantity(
            ionizing_radiations + "/" + unit
        )
        self.water_depletion = deserialize_quantity(water_depletion + "/" + unit)
        self.electronic_waste = deserialize_quantity(electronic_waste + "/" + unit)
        self.primary_energy_consumption = deserialize_quantity(
            primary_energy_consumption + "/" + unit
        )
        self.raw_materials = deserialize_quantity(raw_materials + "/" + unit)
        self.source = source
        self.methodology = methodology

    @property
    def environmental_impact(
        self,
    ) -> EnvironmentalImpact:
        """
        Getter for co2 property
        :return: co2 as float
        """
        return EnvironmentalImpact(
            impacts={
                ImpactCategory.CLIMATE_CHANGE: self.climate_change,
                ImpactCategory.RESOURCE_DEPLETION: self.resource_depletion,
                ImpactCategory.ACIDIFICATION: self.acidification,
                ImpactCategory.FINE_PARTICLES: self.fine_particles,
                ImpactCategory.IONIZING_RADIATIONS: self.ionizing_radiations,
                ImpactCategory.WATER_DEPLETION: self.water_depletion,
                ImpactCategory.ELECTRONIC_WASTE: self.electronic_waste,
                ImpactCategory.PRIMARY_ENERGY: self.primary_energy_consumption,
                ImpactCategory.RAW_MATERIALS: self.raw_materials,
            }
        )

    @property
    def has_time_input(self) -> bool:
        units_split = re.split(r"[*,/]", str(self.unit))
        units_split_len = len(units_split)
        if units_split_len < 2:
            return False
        else:
            return deserialize_quantity(1 * units_split[0]).check(
                "[time]"
            ) or deserialize_quantity(1 * units_split[1]).check("[time]")


class ImpactSourceSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    unit = fields.Str()
    source = fields.Str(
        allow_none=True,
    )
    methodology = fields.Str(
        allow_none=True,
    )


def _get_all_impact_sources() -> list[ImpactSource]:
    def constructor(loader, node):
        fields = loader.construct_mapping(node)
        return ImpactSource(**fields)

    yaml.add_constructor("!ImpactSource", constructor)

    list = []
    with open("impacts_model/data/impact_sources/default.yaml", "r") as stream:
        data_loaded = yaml.load_all(stream, Loader=yaml.Loader)
        for data in data_loaded:
            list.append(data)
    return list


impact_sources = _get_all_impact_sources()


class ImpactSourceError(Exception):
    pass


def impact_source_factory(id: str) -> ImpactSource:
    """
    Factory class to create an ImpactSource object from its id
    :param id: id of the ImpactSource to create
    :return: an ImpactSource object
    """
    res = next((x for x in impact_sources if x.id == id), None)
    if res is None:
        raise ImpactSourceError("No corresponding impact source")
    return res


# class ImpactsSourceRegistry:
#     """
#     Singleton registry containing the model calculations base values
#     """

#     _instance = None

#     def __new__(cls) -> ImpactsSourceRegistry:
#         if cls._instance is None:
#             cls._instance = super(ImpactsSourceRegistry, cls).__new__(cls)

#             # Values
#             cls.pue: float = 1.5
#             # ADEME https://bilans-ges.ademe.fr/fr/accueil/documentation-gene/index/page/Electricite_reglementaire
#             cls.electricity_mix: ELECTRICITY_MIX = 0.0599 * ELECTRICITY_MIX
#         return cls._instance


# class ElectricityImpactSource(ImpactSource):
#     """
#     ImpactSource for electricity in France
#     Ratio /kWh
#     """

#     def __init__(self) -> None:
#         super().__init__(
#             unit=KWH,
#             climate_change=0.136 * KG_CO2E,
#             resource_depletion=0.000000017 * KG_SBE,
#             acidification=0.000468 * MOL_HPOS,
#             fine_particles=0.00000000337 * DISEASE_INCIDENCE,
#             ionizing_radiations=0.00478 * KG_BQ_U235E,
#             water_depletion=0.267 * CUBIC_METER,
#             electronic_waste=0.0952 * ELECTRONIC_WASTE,
#             primary_energy_consumption=15.5 * PRIMARY_MJ,
#             raw_materials=0.298 * TONNE_MIPS,
#         )


# class UserDeviceImpactSource(ImpactSource):
#     """
#     ImpactSource for devices (smartphone, pc) usage/amortization induced by application transferred
#     Ratio for 1h/user
#     """

#     RATIO_TABLET = 0.0784
#     RATIO_PC = 0.1373
#     RATIO_TV = 0.2549
#     RATIO_SMARTPHONE = 0.5294

#     def __init__(self) -> None:
#         """
#         Standard ratio for one hour of user device, half on a laptop and the other on a smartphone
#         """
#         self.unit = USER_DEVICE / HOUR
#         self.smartphone_impact = SmartphoneImpactSource().co2 * HOUR / SMARTPHONE
#         self.laptop_impact = LaptopImpactSource().co2 * HOUR / LAPTOP
#         self.tablet_impact = TabletImpactSource().co2 * HOUR / TABLET
#         self.tv_impact = TelevisionImpactSource().co2 * HOUR / TELEVISION
#         super().__init__(unit=self.unit, climate_change=self.co2)

#     @property
#     def co2(self) -> (KG_CO2E * USER_DEVICE / HOUR):
#         """
#         Compute a standard UserDevice hour impact, by using the registry ratio of devices
#         :return: KG_CO2E impact for 1h of UserDevice
#         """
#         co2: KG_CO2E = (
#             self.RATIO_TABLET * self.tablet_impact
#             + self.RATIO_PC * self.laptop_impact
#             + self.RATIO_TV * self.tv_impact
#             + self.RATIO_SMARTPHONE * self.smartphone_impact
#         )
#         return co2 * self.unit


# class LaptopImpactSource(ImpactSource):
#     """
#     ImpactSource for a laptop usage/amortization induced by application transferred
#     Ratio for 1h/laptop
#     """

#     # Boavizta - https://github.com/Boavizta/environmental-footprint-data
#     FABRICATION_CO2 = 307.37 * KG_CO2E
#     LIFE_EXPECTANCY = 4.34 * YEAR
#     DAILY_USE = 7 * HOUR

#     DAY_AMORTIZATION = (FABRICATION_CO2 / LIFE_EXPECTANCY).to("amortization")

#     def __init__(self) -> None:
#         """
#         Init a laptop hour usage co2 emissions as amortization by hour
#         co2 for 1h of usage
#         """

#         one_day_amortization = self.DAY_AMORTIZATION * (
#             1 * DAY
#         )  # compute the co2 for 1 day
#         hour_amortization = (one_day_amortization / self.DAILY_USE) * (
#             1 * HOUR
#         )  # Cannot directly compute as laptop isn't used 24h/24h. Take 1 hour

#         super().__init__(
#             unit=LAPTOP / HOUR, climate_change=hour_amortization.to("kg_co2e")
#         )


# class SmartphoneImpactSource(ImpactSource):
#     """
#     ImpactSource for a smartphone usage/amortization induced by application transferred
#     Ratio for 1h/smartphone
#     """

#     FABRICATION_CO2 = 88.75 * KG_CO2E
#     LIFE_EXPECTANCY = 2 * YEAR
#     DAILY_USE = 3.12 * HOUR  # https://ieeexplore.ieee.org/abstract/document/6360448
#     DAY_AMORTIZATION = (FABRICATION_CO2 / LIFE_EXPECTANCY).to("amortization")

#     def __init__(self) -> None:
#         """
#         Init a smartphone hour usage co2 emissions as amortization by hour
#         co2 for 1h of usage
#         """
#         one_day_amortization = self.DAY_AMORTIZATION * (
#             1 * DAY
#         )  # compute the co2 for 1 day
#         hour_amortization = (one_day_amortization / self.DAILY_USE) * (
#             1 * HOUR
#         )  # Cannot directly compute as smartphone isn't used 24h/24h. Take 1 hour

#         super().__init__(
#             unit=SMARTPHONE / HOUR, climate_change=hour_amortization.to("kg_co2e")
#         )


# class TabletImpactSource(ImpactSource):
#     """
#     ImpactSource for a Tablet usage/amortization induced by application
#     Ratio for 1h/smartphone
#     """

#     FABRICATION_CO2 = (
#         63.2 * KG_CO2E
#     )  # Source: https://bilans-ges.ademe.fr/fr/basecarbone/donnees-consulter/liste-element?recherche=tablettej
#     LIFE_EXPECTANCY = 5 * YEAR
#     DAILY_USE = 1 * HOUR

#     DAY_AMORTIZATION = (FABRICATION_CO2 / LIFE_EXPECTANCY).to("amortization")

#     def __init__(self) -> None:
#         one_day_amortization = self.DAY_AMORTIZATION * (
#             1 * DAY
#         )  # compute the co2 for 1 day
#         hour_amortization = (one_day_amortization / self.DAILY_USE) * (
#             1 * HOUR
#         )  # Cannot directly compute as tablet isn't used 24h/24h. Take 1 hour

#         super().__init__(
#             unit=TABLET / HOUR, climate_change=hour_amortization.to("kg_co2e")
#         )


# class TelevisionImpactSource(ImpactSource):
#     """
#     ImpactSource for a 49-inch tv usage/amortization induced by application
#     Ratio for 1h watched
#     """

#     FABRICATION_CO2 = 500 * KG_CO2E
#     # Source: https://bilans-ges.ademe.fr/fr/basecarbone/donnees-consulter/liste-element?recherche=tablette
#     LIFE_EXPECTANCY = 10 * YEAR
#     DAILY_USE = 3 * HOUR

#     DAY_AMORTIZATION = (FABRICATION_CO2 / LIFE_EXPECTANCY).to("amortization")

#     def __init__(self) -> None:
#         """
#         Init a television hour usage co2 emissions as amortization by hour
#         co2 for 1h of usage
#         """
#         one_day_amortization = self.DAY_AMORTIZATION * (
#             1 * DAY
#         )  # compute the co2 for 1 day
#         hour_amortization = (one_day_amortization / self.DAILY_USE) * (
#             1 * HOUR
#         )  # Cannot directly compute as television isn't used 24h/24h. Take 1 hour

#         super().__init__(
#             unit=TELEVISION / HOUR, climate_change=hour_amortization.to("kg_co2e")
#         )


# class NetworkImpactSource(ImpactSource):
#     """
#     ImpactSource for network usage caused by software induced data transferred
#     Ratio/gb transferred
#     """

#     def __init__(self) -> None:
#         super().__init__(unit=GIGABYTE, climate_change=0.0015 * KG_CO2E)


# class OfficeImpactSource(ImpactSource):
#     """
#     ImpactSource for offices buildings construction and amortization
#     Ratio / day / person
#     """

#     # Legifrance
#     # https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000042994780
#     # 18m2/office, offices occupancy rate 70%
#     OFFICE_SIZE = 18
#     OFFICES_OCCUPANCY = 0.7

#     # Observatoire de l'immobilier durable
#     # https://resources.taloen.fr/resources/documents/7765_191210_poids_carbone_ACV_vdef.pdf
#     # LCA offices, emissions/m2
#     BUILDING_EMISSIONS = 3900 * KG_CO2E
#     LIFE_EXPECTANCY = 50  # years

#     def __init__(self) -> None:
#         """
#         Define a space per person as office space + corridors, halls, lavatory etc... then multiply by square meter
#         LCA / building expectancy
#         """
#         sqr_meter_office = (
#             self.OFFICE_SIZE / self.OFFICES_OCCUPANCY
#         )  # Adding corridors halls etc. to single offices
#         office_emissions_sqr_meter_day = self.BUILDING_EMISSIONS / (
#             self.LIFE_EXPECTANCY * 365
#         )
#         office_co2_person = sqr_meter_office * office_emissions_sqr_meter_day
#         super().__init__(unit=MAN_DAY, climate_change=office_co2_person)


# class PeopleImpactSource(ImpactSource):
#     """
#     ImpactSource for a people day
#     Ratio/person/day
#     """

#     def __init__(self) -> None:
#         laptop = LaptopImpactSource().co2 * (7 * HOUR) / LAPTOP
#         office = OfficeImpactSource().co2 / MAN_DAY
#         transport = TransportImpactSource().co2 / MAN_DAY
#         super().__init__(unit=MAN_DAY, climate_change=office + transport + laptop)


# class StorageImpactSource(ImpactSource):
#     """
#     EnvironmentalImpact source for storage (disks)
#     Ratio / tb / day
#     """

#     SSD_WH = 1.52 * WATT_HOUR

#     LIFE_EXPECTANCY = 4
#     FABRICATION_CO2 = 250 * KG_CO2E

#     def __init__(self) -> None:
#         """
#         Storage impact source, defined by the electricity mix used to make it run, and the pue of its datacenter
#         Uses the impactRegistry to get pue and electricity_mix
#         """
#         self.registry = ImpactsSourceRegistry()
#         self.unit = TERABYTE / DAY
#         super().__init__(unit=self.unit, climate_change=self.co2)

#     @property
#     def co2(self) -> (KG_CO2E * TERABYTE / DAY):
#         """
#         Compute the co2 of a 1tb disk for a day, using amortization and power consumption
#         :return: KG_CO2E/disk(1tb)
#         """
#         amortization_day = self.FABRICATION_CO2 / (self.LIFE_EXPECTANCY * 365)
#         wh_pue = (
#             self.SSD_WH * self.registry.pue
#         )  # Pondering the consumption with the PUE
#         wh_day = wh_pue * 24  # wh consumed for a complete day
#         kwh_day = wh_day.to("kWh")
#         consumption_co2 = (
#             kwh_day * self.registry.electricity_mix
#         )  # consumption co2 emissions
#         co2_total: KG_CO2E = consumption_co2 + amortization_day
#         return (
#             Q_(co2_total.magnitude, KG_CO2E) * self.unit
#         )


# class ServerImpactSource(ImpactSource):
#     """
#     ImpactSource for servers
#     Ratio/day
#     """

#     # Boavizta
#     # https://github.com/Boavizta/environmental-footprint-data
#     SERVER_POWER_IDLE = 234 * WATT_HOUR
#     SERVER_POWER_RUN = 1100 * WATT_HOUR
#     LIFE_EXPECTANCY = 3.89
#     FABRICATION_CO2 = 1613.25 * KG_CO2E
#     SERVER_USAGE = 0.7

#     def __init__(self) -> None:
#         """
#         Server impact source, defined by the electricity mix used to make it run, and the pue of its datacenter
#         Uses the impactRegistry to get pue and electricity_mix
#         """
#         self.registry = ImpactsSourceRegistry()
#         self.unit = SERVER / DAY
#         super().__init__(unit=self.unit, climate_change=self.co2)

#     @property
#     def co2(self) -> (KG_CO2E * SERVER / DAY):
#         """
#         Compute the co2 cost of a server, adding consumption pondered with pue and amortization
#         :return: KG_CO2E / day
#         """

#         amortization_day = self.FABRICATION_CO2 / (self.LIFE_EXPECTANCY * 365)
#         kwh = (
#             self.SERVER_POWER_RUN - self.SERVER_POWER_IDLE
#         ) * self.SERVER_USAGE + self.SERVER_POWER_IDLE
#         # using SERVER_USAGE to avoid having the server at full power
#         # all the time
#         kwh_pue = kwh * self.registry.pue  # Pondering the consumption with the PUE
#         kwh_day = kwh_pue * 24  # wh consumed for a complete day
#         consumption_co2 = (
#             kwh_day * self.registry.electricity_mix
#         )  # consumption co2 emissions
#         co2_total: KG_CO2E = consumption_co2 + amortization_day
#         return co2_total.to("kg_co2e") * self.unit


# class TransportImpactSource(ImpactSource):
#     """
#     ImpactSource for all transports
#     Ratio/person/day
#     """

#     # INSEE Déplacements cadres et professions intellectuelles, toutes activités  dans un rayon de  80 km
#     # https://www.statistiques.developpement-durable.gouv.fr/resultats-detailles-de-lenquete-mobilite-des-personnes-de-2019?rubrique=60&dossier=1345
#     FOOT_PERCENTAGE = 1.3818
#     BIKE_PERCENTAGE = 1.44675
#     PUBLIC_TRANSPORT_PERCENTAGE = 17.77558  # 10% uncertainty
#     CAR_PERCENTAGE = (
#         76.32407 + 0.15459
#     )  # other categories (tractors...) # 10% uncertainty
#     MOTORBIKE_PERCENTAGE = 2.91722

#     # Observatoire des territoires
#     # https://www.observatoire-des-territoires.gouv.fr/kiosque/2019-mobilite-10-les-cadres-parcourent-chaque-annee-pres-de-3000-km-de-plus-que-les
#     MEAN_DISTANCE = 19 * 2

#     def __init__(self) -> None:
#         """
#         Using the ratios of transportation mode, define a generic co2 emissions/km
#         Then multiply by the mean distance per day per person
#         """
#         co2_km = (
#             (
#                 self.FOOT_PERCENTAGE * 0
#                 + self.BIKE_PERCENTAGE * BikeImpactSource().co2
#                 + self.PUBLIC_TRANSPORT_PERCENTAGE * PublicTransportImpactSource().co2
#                 + self.CAR_PERCENTAGE * CarImpactSource().co2
#                 + self.MOTORBIKE_PERCENTAGE * MotorbikeImpactSource().co2
#             )
#             / 100
#             / MAN_DAY  # Remove the man_day attribute from the subclasses to avoid MAN_DAY ** 2
#         )
#         co2_day = co2_km * self.MEAN_DISTANCE
#         super().__init__(unit=MAN_DAY, climate_change=co2_day)


# class CarImpactSource(ImpactSource):
#     """
#     ImpactSource for car
#     Ratio /km
#     """

#     # ADEME
#     # 0.218 incertitude = 60%
#     # https://bilans-ges.ademe.fr/fr/basecarbone/donnees-consulter/liste-element/categorie/151
#     def __init__(self) -> None:
#         super().__init__(unit=MAN_DAY, climate_change=0.218 * KG_CO2E)


# class BikeImpactSource(ImpactSource):
#     """
#     ImpactSource for bike
#     Ratio /km
#     """

#     # TREK
#     # https://view.publitas.com/trek-bicycle/trek-bicycle-2021-sustainability-report/page/5

#     def __init__(self) -> None:
#         super().__init__(unit=MAN_DAY, climate_change=0.00348 * KG_CO2E)


# class PublicTransportImpactSource(ImpactSource):
#     """
#     ImpactSource for public transport
#     Ratio / km / person
#     """

#     # ADEME
#     # https://bilans-ges.ademe.fr/fr/accueil/documentation-gene/index/page/Ferroviaire2
#     def __init__(self) -> None:
#         super().__init__(unit=MAN_DAY, climate_change=0.00503 * KG_CO2E)


# class MotorbikeImpactSource(ImpactSource):
#     """
#     ImpactSource for motorbike
#     Ratio / km / personq
#     """

#     # ADEME
#     # https://bilans-ges.ademe.fr/fr/accueil/documentation-gene/index/page/Routier2
#     def __init__(self) -> None:
#         super().__init__(unit=MAN_DAY, climate_change=0.191 * KG_CO2E)


# class RmVCPUImpactSource(ImpactSource):
#     """
#     ImpactSource for one vCPU for one month at Rueil-Malmaison DC
#     """

#     def __init__(self) -> None:
#         super().__init__(
#             unit=VCPU / DAY,
#             climate_change=4.506211 * KG_CO2E,
#             resource_depletion=0.000000878 * KG_SBE,
#             acidification=0.015592121 * MOL_HPOS,
#             fine_particles=0.000000111281 * DISEASE_INCIDENCE,
#             ionizing_radiations=0.15738558 * KG_BQ_U235E,
#             water_depletion=8.61050442 * CUBIC_METER,
#             electronic_waste=3.087493 * ELECTRONIC_WASTE,
#             primary_energy_consumption=498.310296 * PRIMARY_MJ,
#             raw_materials=10.2950296 * TONNE_MIPS,
#         )


# class VdrCPUImpactSource(ImpactSource):
#     """
#     ImpactSource for one vCPU for one month at Val de reuil DC
#     """

#     def __init__(self) -> None:
#         super().__init__(
#             climate_change=0.2206123 * KG_CO2E,
#             resource_depletion=0.000766107 * KG_SBE,
#             acidification=4.85e-08 * MOL_HPOS,
#             fine_particles=5.44803e-09 * DISEASE_INCIDENCE,
#             ionizing_radiations=0.007705325 * KG_BQ_U235E,
#             water_depletion=0.416680258 * CUBIC_METER,
#             electronic_waste=0.51490173 * ELECTRONIC_WASTE,
#             primary_energy_consumption=0.1496829 * PRIMARY_MJ,
#             raw_materials=24.0944172 * TONNE_MIPS,
#         )


# class RmRAMImpactSource(ImpactSource):
#     """
#     ImpactSource for one GB of RAM for one month at Rueil-Malmaison DC
#     """

#     def __init__(self) -> None:
#         super().__init__(
#             climate_change=0.5186616 * KG_CO2E,
#             resource_depletion=0.00000001055 * KG_SBE,
#             acidification=0.002105015 * MOL_HPOS,
#             fine_particles=0.0000000115591 * DISEASE_INCIDENCE,
#             ionizing_radiations=0.00596069 * KG_BQ_U235E,
#             water_depletion=0.228200547 * CUBIC_METER,
#             electronic_waste=0.0243686 * ELECTRONIC_WASTE,
#             primary_energy_consumption=7.8400366 * PRIMARY_MJ,
#             raw_materials=0.12390367 * TONNE_MIPS,
#         )


# class VdrRAMImpactSource(ImpactSource):
#     """
#     ImpactSource for one GB of RAM for one month at Val de Reuil DC
#     """

#     def __init__(self) -> None:
#         super().__init__(
#             climate_change=0.267726 * KG_CO2E,
#             resource_depletion=0.001086803 * KG_SBE,
#             acidification=4.58e-09 * MOL_HPOS,
#             fine_particles=5.97501e-09 * DISEASE_INCIDENCE,
#             ionizing_radiations=0.002916121 * KG_BQ_U235E,
#             water_depletion=0.109300096 * CUBIC_METER,
#             electronic_waste=0.053100643 * ELECTRONIC_WASTE,
#             primary_energy_consumption=0.00895852 * PRIMARY_MJ,
#             raw_materials=3.49000642 * TONNE_MIPS,
#         )


# class RmStorageImpactSource(ImpactSource):
#     """
#     ImpactSource for one GB of storage for one month at Rueil-Malmaison DC
#     """

#     def __init__(self) -> None:
#         super().__init__(
#             climate_change=1.1922143 * KG_CO2E,
#             resource_depletion=0.00000084877 * KG_SBE,
#             acidification=0.004756408 * MOL_HPOS,
#             fine_particles=0.00000002585 * DISEASE_INCIDENCE,
#             ionizing_radiations=0.041780379 * KG_BQ_U235E,
#             water_depletion=0.4456003 * CUBIC_METER,
#             electronic_waste=0.1535267 * ELECTRONIC_WASTE,
#             primary_energy_consumption=12.1600201 * PRIMARY_MJ,
#             raw_materials=0.53460201 * TONNE_MIPS,
#         )


# class VdrRamStorageImpactSource(ImpactSource):
#     """
#     ImpactSource for one GB of storage for one month at Val de Reuil DC
#     """

#     def __init__(self) -> None:
#         super().__init__(
#             climate_change=1.1922143 * KG_CO2E,
#             resource_depletion=0.004756408 * KG_SBE,
#             acidification=8.4877e-07 * MOL_HPOS,
#             fine_particles=2.585e-08 * DISEASE_INCIDENCE,
#             ionizing_radiations=0.041780379 * KG_BQ_U235E,
#             water_depletion=0.4456003 * CUBIC_METER,
#             electronic_waste=0.53460201 * ELECTRONIC_WASTE,
#             primary_energy_consumption=0.1535267 * PRIMARY_MJ,
#             raw_materials=12.1600201 * TONNE_MIPS,
#         )
