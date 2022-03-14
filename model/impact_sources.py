class ImpactSource:
    """
    Abstract class to define a source of impact emission(s)
    """

    def __init__(self, co2: float) -> None:
        self.co2: float = co2


class DeviceImpact(ImpactSource):
    """
    ImpactSource for devices (smartphone, pc) usage/amortization induced by application transferred
    Ratio for 1h/user
    """

    SMARTPHONE_CO2 = 88.75
    SMARTPHONE_LIFE = 2
    SMARTPHONE_DAILY_USE = 3.12 # https://ieeexplore.ieee.org/abstract/document/6360448

    LAPTOP_CO2 = 307.37  # Boavizta - https://github.com/Boavizta/environmental-footprint-data
    LAPTOP_LIFE = 4.34
    PC_DAILY_USE = 7

    def __init__(self) -> None:
        smartphone_day_co2 = self.SMARTPHONE_CO2 / (self.SMARTPHONE_LIFE * 365)
        smartphone_hour_co2 = smartphone_day_co2 / self.SMARTPHONE_DAILY_USE

        laptop_day_co2 = self.LAPTOP_CO2 / (self.LAPTOP_LIFE * 365)
        laptop_hour_co2 = laptop_day_co2 / self.PC_DAILY_USE

        co2 = laptop_hour_co2 * 0.5 + smartphone_hour_co2 * 0.5

        super().__init__(co2)


# TODO add different devices
# TODO better devices RATIO


class NetworkImpact(ImpactSource):
    """
    ImpactSource for network usage caused by software induced data transferred
    Ratio/gb transferred
    """

    def __init__(self) -> None:
        super().__init__(0.0015)


class OfficeImpact(ImpactSource):
    """
    ImpactSource for offices buildings construction and amortization
    Ratio / day / person
    """

    # Legifrance
    # https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000042994780
    # 18m2/office, offices occupancy rate 70%
    OFFICE_SIZE = ((18 * 100) / 70) # TODO remove computation

    # Observatoire de l'immobilier durable
    # https://resources.taloen.fr/resources/documents/7765_191210_poids_carbone_ACV_vdef.pdf
    # LCA offices, emissions/m2
    BUILDING_EMISSIONS = 3900
    BUILDING_LIFE_EXPECTANCY = 50  # years

    def __init__(self) -> None:
        office_emissions_sqr_meter_day = self.BUILDING_EMISSIONS / (self.BUILDING_LIFE_EXPECTANCY * 365)
        office_co2_person = self.OFFICE_SIZE * office_emissions_sqr_meter_day
        super().__init__(office_co2_person)  # TODO explain ratio


class ServerImpact(ImpactSource):
    """
    ImpactSource for servers
    Ratio/day
    """

    # Boavizta
    # https://github.com/Boavizta/environmental-footprint-data
    SERVER_POWER_IDLE = 234
    SERVER_POWER_RUN = 1100
    SERVER_LIFE = 3.89
    SERVER_FABRICATION_CO2 = 1613.25
    SERVER_USAGE = 0.7

    def __init__(self, electricity_mix: float, pue: float) -> None:
        amortization_day = self.SERVER_FABRICATION_CO2 / (self.SERVER_LIFE * 365)

        wh = (
                     self.SERVER_POWER_RUN - self.SERVER_POWER_IDLE
             ) * self.SERVER_USAGE + self.SERVER_POWER_IDLE
        wh_pue = wh * pue
        kwh_day = (wh_pue * 24) / 1000
        server_day = kwh_day * electricity_mix + amortization_day
        super().__init__(server_day)


class StorageImpact(ImpactSource):
    """
    Impact source for storage (disks)
    Ratio / tb / hour
    """

    SSD_TB_CONS = 1.52

    DISK_LIFE = 4
    DISK_FABRICATION_CO2 = 250 # TODO not used

    def __init__(self, electricity_mix: float, pue: float) -> None:
        wh_to = self.SSD_TB_CONS
        wh_pue = wh_to * pue
        kwh = wh_pue / 1000
        disk_hour = kwh * electricity_mix

        super().__init__(disk_hour)

    # TODO REDO


class TransportImpact(ImpactSource):
    """
    ImpactSource for all transports
    Ratio/person/day
    """

    # INSEE Déplacements cadres et professions intellectuelles, toutes activités  dans un rayon de  80 km
    # https://www.statistiques.developpement-durable.gouv.fr/resultats-detailles-de-lenquete-mobilite-des-personnes-de-2019?rubrique=60&dossier=1345
    FOOT_PERCENTAGE = 1.3818
    BIKE_PERCENTAGE = 1.44675
    PUBLIC_TRANSPORT_PERCENTAGE = 17.77558
    CAR_PERCENTAGE = 76.32407 + 0.15459  # other categories (tractors...)
    MOTORBIKE_PERCENTAGE = 2.91722

    # Observatoire des territoires
    # https://www.observatoire-des-territoires.gouv.fr/kiosque/2019-mobilite-10-les-cadres-parcourent-chaque-annee-pres-de-3000-km-de-plus-que-les
    MEAN_DISTANCE = 19 * 2

    def __init__(self) -> None:
        co2 = (
                      self.FOOT_PERCENTAGE * 0
                      + self.BIKE_PERCENTAGE * BikeImpact().co2
                      + self.PUBLIC_TRANSPORT_PERCENTAGE * PublicTransportImpact().co2
                      + self.CAR_PERCENTAGE * CarImpact().co2
                      + self.MOTORBIKE_PERCENTAGE * MotorbikeImpact().co2
              ) / 100
        super().__init__(co2)


class CarImpact(ImpactSource):
    """
    ImpactSource for car
    Ratio /km
    """

    # ADEME
    # https://bilans-ges.ademe.fr/fr/basecarbone/donnees-consulter/liste-element/categorie/151
    def __init__(self) -> None:
        super().__init__(0.218)


class BikeImpact(ImpactSource):
    """
    ImpactSource for bike
    Ratio /km
    """

    # TREK
    # https://view.publitas.com/trek-bicycle/trek-bicycle-2021-sustainability-report/page/5

    def __init__(self) -> None:
        super().__init__(0.00348)  # TODO ratio computation


class PublicTransportImpact(ImpactSource):
    """
    ImpactSource for public transport
    Ratio / km / person
    """

    # ADEME
    # https://bilans-ges.ademe.fr/fr/accueil/documentation-gene/index/page/Ferroviaire2
    def __init__(self) -> None:
        super().__init__(0.00503)


class MotorbikeImpact(ImpactSource):
    """
    ImpactSource for motorbike
    Ratio / km / person
    """

    # ADEME
    # https://bilans-ges.ademe.fr/fr/accueil/documentation-gene/index/page/Routier2
    def __init__(self) -> None:
        super().__init__(0.191)
