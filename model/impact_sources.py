from pint import Quantity

from model.units import ureg

ImpactKind = str
ImpactsList = dict[str, float]


class ImpactsRegistry:
    """
    Singleton registry containing the model calculations base values
    """

    __instance = None

    def __init__(self) -> None:
        self.pue: float = 1.5
        # ADEME https://bilans-ges.ademe.fr/fr/accueil/documentation-gene/index/page/Electricite_reglementaire
        self.electricity_mix: Quantity["electricity_mix"] = 0.0599 * ureg.electricity_mix  # type: ignore

    def __new__(cls, *args: object, **kwargs: object) -> object:  # type: ignore
        if ImpactsRegistry.__instance is None:
            ImpactsRegistry.__instance = super(ImpactsRegistry, cls).__new__(
                cls, *args, **kwargs
            )
        return ImpactsRegistry.__instance


class ImpactSource:
    """
    Abstract class to define a source of impact emission(s)
    """

    def __init__(self, co2: Quantity["kg_co2e"]):  # type: ignore
        """
        Should be used by implementations, define the different impacts sources
        :param co2: co2 emitted by one unit of the ImpactSource
        """
        self._co2: Quantity["kg_co2e"] = co2  # type: ignore

    @property
    def co2(self) -> Quantity["kg_co2e"]:  # type: ignore
        """
        Getter for co2 property
        :return: co2 as float
        """
        return self._co2


class UserDeviceImpact(ImpactSource):
    """
    ImpactSource for devices (smartphone, pc) usage/amortization induced by application transferred
    Ratio for 1h/user
    """

    RATIO_TABLET = 0.0784
    RATIO_PC = 0.1373
    RATIO_TV = 0.2549
    RATIO_SMARTPHONE = 0.5294

    def __init__(self) -> None:
        """
        Standard ratio for one hour of user device, half on a laptop and the other on a smartphone
        """
        self.smartphone_impact = SmartphoneImpact()
        self.laptop_impact = LaptopImpact()
        self.tablet_impact = TabletImpact()
        self.tv_impact = TelevisionImpact()
        super().__init__(self.co2)

    @property
    def co2(self) -> Quantity["kg_co2e"]:  # type: ignore
        """
        Compute a standard UserDevice hour impact, by using the registry ratio of devices
        :return: kg_co2e impact for 1h of UserDevice
        """
        co2: Quantity["kg_co2e"] = (  # type: ignore
            self.RATIO_TABLET * self.tablet_impact.co2
            + self.RATIO_PC * self.laptop_impact.co2
            + self.RATIO_TV * self.tv_impact.co2
            + self.RATIO_SMARTPHONE * self.smartphone_impact.co2
        )
        return co2


class LaptopImpact(ImpactSource):
    """
    ImpactSource for a laptop usage/amortization induced by application transferred
    Ratio for 1h/laptop
    """

    # Boavizta - https://github.com/Boavizta/environmental-footprint-data
    LAPTOP_CO2 = 307.37
    LAPTOP_LIFE = 4.34
    PC_DAILY_USE = 7

    def __init__(self) -> None:
        """
        Init a laptop hour usage co2 emissions as amortization by hour
        co2 for 1h of usage
        """
        laptop_day_co2 = self.LAPTOP_CO2 / (self.LAPTOP_LIFE * 365)
        laptop_hour_co2 = (laptop_day_co2 / self.PC_DAILY_USE) * ureg.kg_co2e

        super().__init__(laptop_hour_co2)


class SmartphoneImpact(ImpactSource):
    """
    ImpactSource for a smartphone usage/amortization induced by application transferred
    Ratio for 1h/smartphone # TODO update and add uncertainty
    """

    SMARTPHONE_CO2 = 88.75
    SMARTPHONE_LIFE = 2
    SMARTPHONE_DAILY_USE = 3.12  # https://ieeexplore.ieee.org/abstract/document/6360448

    def __init__(self) -> None:
        """
        Init a smartphone hour usage co2 emissions as amortization by hour
        co2 for 1h of usage
        """
        smartphone_day_co2 = self.SMARTPHONE_CO2 / (self.SMARTPHONE_LIFE * 365)
        smartphone_hour_co2 = smartphone_day_co2 / self.SMARTPHONE_DAILY_USE

        super().__init__(smartphone_hour_co2 * ureg.kg_co2e)


class TabletImpact(ImpactSource):
    """
    ImpactSource for a Tablet usage/amortization induced by application
    Ratio for 1h/smartphone
    """

    TABLET_LIFE = 5
    TABLET_DAILY_USE = 1

    def __init__(self) -> None:
        tablet_co2 = 63.2 * ureg.kg_co2e  # .plus_minus(0.5, relative=True)
        # Source: https://bilans-ges.ademe.fr/fr/basecarbone/donnees-consulter/liste-element?recherche=tablette
        tablet_day_co2 = tablet_co2 / (self.TABLET_LIFE * 365)
        tablet_hour_co2 = tablet_day_co2 / self.TABLET_DAILY_USE
        super().__init__(tablet_hour_co2)


class TelevisionImpact(ImpactSource):
    """
    ImpactSource for a 49-inch tv usage/amortization induced by application
    Ratio for 1h watched
    """

    TELEVISION_LIFE = 10
    TELEVISION_DAILY_USE = 3

    def __init__(self) -> None:
        television_co2 = 500 * ureg.kg_co2e  # .plus_minus(0.5, relative=True)
        # Source: https://bilans-ges.ademe.fr/fr/basecarbone/donnees-consulter/liste-element?recherche=tablette
        tablet_day_co2 = television_co2 / (self.TELEVISION_LIFE * 365)
        tablet_hour_co2 = tablet_day_co2 / self.TELEVISION_DAILY_USE
        super().__init__(tablet_hour_co2)


class NetworkImpact(ImpactSource):
    """
    ImpactSource for network usage caused by software induced data transferred
    Ratio/gb transferred
    """

    def __init__(self) -> None:
        super().__init__(0.0015 * ureg.kg_co2e)


class OfficeImpact(ImpactSource):
    """
    ImpactSource for offices buildings construction and amortization
    Ratio / day / person
    """

    # Legifrance
    # https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000042994780
    # 18m2/office, offices occupancy rate 70%
    OFFICE_SIZE = 18
    OFFICES_OCCUPANCY = 0.7

    # Observatoire de l'immobilier durable
    # https://resources.taloen.fr/resources/documents/7765_191210_poids_carbone_ACV_vdef.pdf
    # LCA offices, emissions/m2
    BUILDING_EMISSIONS = 3900
    BUILDING_LIFE_EXPECTANCY = 50  # years

    def __init__(self) -> None:
        """
        Define a space per person as office space + corridors, halls, lavatory etc... then multiply by square meter
        LCA / building expectancy
        """
        sqr_meter_office = (
            self.OFFICE_SIZE / self.OFFICES_OCCUPANCY
        )  # Adding corridors halls etc. to single offices
        office_emissions_sqr_meter_day = self.BUILDING_EMISSIONS / (
            self.BUILDING_LIFE_EXPECTANCY * 365
        )
        office_co2_person = sqr_meter_office * office_emissions_sqr_meter_day
        super().__init__(office_co2_person * ureg.kg_co2e)


class ServerImpact(ImpactSource):
    """
    ImpactSource for servers
    Ratio/day
    """

    # Boavizta
    # https://github.com/Boavizta/environmental-footprint-data
    SERVER_POWER_IDLE = 234 * ureg.watt_hour
    SERVER_POWER_RUN = 1100 * ureg.watt_hour
    SERVER_LIFE = 3.89
    SERVER_FABRICATION_CO2 = 1613.25 * ureg.kg_co2e
    SERVER_USAGE = 0.7

    def __init__(self) -> None:
        """
        Server impact source, defined by the electricity mix used to make it run, and the pue of its datacenter
        Uses the impactRegistry to get pue and electricity_mix
        """
        self.registry = ImpactsRegistry()
        super().__init__(self.co2)

    @property
    def co2(self) -> Quantity["kg_co2e"]:  # type: ignore
        """
        Compute the co2 cost of a server, adding consumption pondered with pue and amortization
        :return: kg_co2e / day
        """

        amortization_day = self.SERVER_FABRICATION_CO2 / (self.SERVER_LIFE * 365)
        kwh = (
            (self.SERVER_POWER_RUN - self.SERVER_POWER_IDLE) * self.SERVER_USAGE
            + self.SERVER_POWER_IDLE
        )
        # using SERVER_USAGE to avoid having the server at full power
        # all the time
        kwh_pue = kwh * self.registry.pue  # Pondering the consumption with the PUE
        kwh_day = kwh_pue * 24  # wh consumed for a complete day
        consumption_co2 = (kwh_day * self.registry.electricity_mix)  # consumption co2 emissions
        co2_total: Quantity["kg_co2e"] = consumption_co2 + amortization_day  # type: ignore
        return co2_total


class StorageImpact(ImpactSource):
    """
    Impact source for storage (disks)
    Ratio / tb / day
    """

    SSD_WH = 1.52 * ureg.watt_hour

    DISK_LIFE = 4
    DISK_FABRICATION_CO2 = 250

    def __init__(self) -> None:
        """
        Storage impact source, defined by the electricity mix used to make it run, and the pue of its datacenter
        Uses the impactRegistry to get pue and electricity_mix
        """
        self.registry = ImpactsRegistry()
        super().__init__(self.co2)

    @property
    def co2(self) -> Quantity["kg_co2e"]:  # type: ignore
        """
        Compute the co2 of a 1tb disk for a day, using amortization and power consumption
        :return: kg_co2e/disk(1tb)
        """
        amortization_day: Quantity["ureg.kg_co2e"] = (self.DISK_FABRICATION_CO2 / (self.DISK_LIFE * 365)) * ureg.kg_co2e  # type: ignore
        wh_pue = (
            self.SSD_WH * self.registry.pue
        )  # Pondering the consumption with the PUE
        wh_day = wh_pue * 24  # wh consumed for a complete day
        kwh_day = wh_day.to("kWh")
        consumption_co2 = (
            kwh_day * self.registry.electricity_mix
        )  # consumption co2 emissions
        co2_total: Quantity["kg_co2e"] = consumption_co2 + amortization_day  # type: ignore
        return co2_total


class TransportImpact(ImpactSource):
    """
    ImpactSource for all transports
    Ratio/person/day
    """

    # INSEE Déplacements cadres et professions intellectuelles, toutes activités  dans un rayon de  80 km
    # https://www.statistiques.developpement-durable.gouv.fr/resultats-detailles-de-lenquete-mobilite-des-personnes-de-2019?rubrique=60&dossier=1345
    FOOT_PERCENTAGE = 1.3818
    BIKE_PERCENTAGE = 1.44675
    PUBLIC_TRANSPORT_PERCENTAGE = 17.77558  # 10% uncertainty
    CAR_PERCENTAGE = (
        76.32407 + 0.15459
    )  # other categories (tractors...) # 10% uncertainty
    MOTORBIKE_PERCENTAGE = 2.91722

    # Observatoire des territoires
    # https://www.observatoire-des-territoires.gouv.fr/kiosque/2019-mobilite-10-les-cadres-parcourent-chaque-annee-pres-de-3000-km-de-plus-que-les
    MEAN_DISTANCE = 19 * 2

    def __init__(self) -> None:
        """
        Using the ratios of transportation mode, define a generic co2 emissions/km
        Then multiply by the mean distance per day per person
        """
        co2_km = (
            self.FOOT_PERCENTAGE * 0
            + self.BIKE_PERCENTAGE * BikeImpact().co2
            + self.PUBLIC_TRANSPORT_PERCENTAGE * PublicTransportImpact().co2
            + self.CAR_PERCENTAGE * CarImpact().co2
            + self.MOTORBIKE_PERCENTAGE * MotorbikeImpact().co2
        ) / 100
        co2_day = co2_km * self.MEAN_DISTANCE
        super().__init__(co2_day)


class CarImpact(ImpactSource):
    """
    ImpactSource for car
    Ratio /km
    """

    # ADEME
    # 0.218 incertitude = 60%
    # https://bilans-ges.ademe.fr/fr/basecarbone/donnees-consulter/liste-element/categorie/151
    def __init__(self) -> None:
        super().__init__(0.218 * ureg.kg_co2e)


class BikeImpact(ImpactSource):
    """
    ImpactSource for bike
    Ratio /km
    """

    # TREK
    # https://view.publitas.com/trek-bicycle/trek-bicycle-2021-sustainability-report/page/5

    def __init__(self) -> None:
        super().__init__(0.00348 * ureg.kg_co2e)


class PublicTransportImpact(ImpactSource):
    """
    ImpactSource for public transport
    Ratio / km / person
    """

    # ADEME
    # https://bilans-ges.ademe.fr/fr/accueil/documentation-gene/index/page/Ferroviaire2
    def __init__(self) -> None:
        super().__init__(0.00503 * ureg.kg_co2e)


class MotorbikeImpact(ImpactSource):
    """
    ImpactSource for motorbike
    Ratio / km / person
    """

    # ADEME
    # https://bilans-ges.ademe.fr/fr/accueil/documentation-gene/index/page/Routier2
    def __init__(self) -> None:
        super().__init__(0.191 * ureg.kg_co2e)
