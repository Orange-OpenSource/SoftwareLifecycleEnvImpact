SMARTPHONE_CO2 = 88.75
SMARTPHONE_LIFE = 2
SMARTPHONE_DAILY_USE = 3.12

LAPTOP_CO2 = 307.37
LAPTOP_LIFE = 4.34
PC_DAILY_USE = 7

HDD_TB_CONS = 0.89
SSD_TB_CONS = 1.52

DISK_SIZE = 4
DISK_LIFE = 4
DISK_FABRICATION_CO2 = 250

SERVER_POWER_IDLE = 234
SERVER_POWER_RUN = 1100
SERVER_LIFE = 3.89
SERVER_FABRICATION_CO2 = 1613.25
SERVER_USAGE = 0.7

ELECTRICITY_MIX = 0.0599
PUE = 1.5

FOOT_PERCENTAGE = 1.3818
BIKE_PERCENTAGE = 1.44675
PUBLIC_TRANSPORT_PERCENTAGE = 17.77558
CAR_PERCENTAGE = 76.32407 + 0.15459  # other categories (tractors...)
MOTORBIKE_PERCENTAGE = 2.91722


# TODO move


class ImpactSource:
    def __init__(self, co2: float) -> None:
        self.co2: float = co2


class DeviceImpact(ImpactSource):
    def __init__(self) -> None:
        smartphone_day_co2 = SMARTPHONE_CO2 / (SMARTPHONE_LIFE * 365)
        smartphone_hour_co2 = smartphone_day_co2 / SMARTPHONE_DAILY_USE

        laptop_day_co2 = LAPTOP_CO2 / (LAPTOP_LIFE * 365)
        laptop_hour_co2 = laptop_day_co2 / PC_DAILY_USE

        co2 = laptop_hour_co2 * 0.5 + smartphone_hour_co2 * 0.5

        super().__init__(co2)


# TODO add different devices


class NetworkImpact(ImpactSource):
    def __init__(self) -> None:
        super().__init__(0.0015)


class OfficeImpact(ImpactSource):
    def __init__(self) -> None:
        office_emissions_sqr_meter_day = 3900 / (50 * 365)
        office_co2_person = ((18 * 100) / 70) * office_emissions_sqr_meter_day
        super().__init__(office_co2_person)


class ServerImpact(ImpactSource):
    def __init__(self) -> None:
        amortization_day = SERVER_FABRICATION_CO2 / (SERVER_LIFE * 365)

        wh = (SERVER_POWER_RUN - SERVER_POWER_IDLE) * SERVER_USAGE + SERVER_POWER_IDLE
        wh_pue = wh * PUE
        kwh_day = (wh_pue * 24) / 1000
        server_day = kwh_day * ELECTRICITY_MIX + amortization_day
        super().__init__(server_day)


class StorageImpact(ImpactSource):
    def __init__(self) -> None:
        wh_to = SSD_TB_CONS
        wh_disk = DISK_SIZE * wh_to
        wh_pue = wh_disk * PUE
        kwh = wh_pue / 1000
        disk_hour = kwh * ELECTRICITY_MIX

        super().__init__(disk_hour)

    # TODO REDO


class TransportImpact(ImpactSource):
    def __init__(self) -> None:
        co2 = (
            FOOT_PERCENTAGE * 0
            + BIKE_PERCENTAGE * BikeImpact().co2
            + PUBLIC_TRANSPORT_PERCENTAGE * PublicTransportImpact().co2
            + CAR_PERCENTAGE * CarImpact().co2
            + MOTORBIKE_PERCENTAGE * MotorbikeImpact().co2
        ) / 100
        super().__init__(co2)


class CarImpact(ImpactSource):
    def __init__(self) -> None:
        super().__init__(0.218)


class BikeImpact(ImpactSource):
    def __init__(self) -> None:
        super().__init__(0.00348)


class PublicTransportImpact(ImpactSource):
    def __init__(self) -> None:
        super().__init__(0.00503)


class MotorbikeImpact(ImpactSource):
    def __init__(self) -> None:
        super().__init__(0.191)
