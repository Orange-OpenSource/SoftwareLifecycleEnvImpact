from impacts_model.impacts.impact_factors import ImpactFactor
from impacts_model.quantities import (
    CUBIC_METER,
    DISEASE_INCIDENCE,
    ELECTRONIC_WASTE,
    KG_BQ_U235E,
    KG_CO2E,
    KG_SBE,
    MOL_HPOS,
    PRIMARY_MJ,
    TONNE_MIPS,
)


class RmVCPUImpact(ImpactFactor):
    """
    Impact factor for one vCPU for one month at Rueil-Malmaison DC
    """

    def __init__(self) -> None:
        super().__init__(
            climate_change=4.506211 * KG_CO2E,
            resource_depletion=0.000000878 * KG_SBE,
            acidification=0.015592121 * MOL_HPOS,
            fine_particles=0.000000111281 * DISEASE_INCIDENCE,
            ionizing_radiations=0.15738558 * KG_BQ_U235E,
            water_depletion=8.61050442 * CUBIC_METER,
            electronic_waste=3.087493 * ELECTRONIC_WASTE,
            primary_energy_consumption=498.310296 * PRIMARY_MJ,
            raw_materials=10.2950296 * TONNE_MIPS,
        )


class VdrCPUImpact(ImpactFactor):
    """
    Impact factor for one vCPU for one month at Val de reuil DC
    """

    def __init__(self) -> None:
        super().__init__(
            climate_change=0.2206123 * KG_CO2E,
            resource_depletion=0.000766107 * KG_SBE,
            acidification=4.85e-08 * MOL_HPOS,
            fine_particles=5.44803e-09 * DISEASE_INCIDENCE,
            ionizing_radiations=0.007705325 * KG_BQ_U235E,
            water_depletion=0.416680258 * CUBIC_METER,
            electronic_waste=0.51490173 * ELECTRONIC_WASTE,
            primary_energy_consumption=0.1496829 * PRIMARY_MJ,
            raw_materials=24.0944172 * TONNE_MIPS,
        )


class RmRAMImpact(ImpactFactor):
    """
    Impact factor for one GB of RAM for one month at Rueil-Malmaison DC
    """

    def __init__(self) -> None:
        super().__init__(
            climate_change=0.5186616 * KG_CO2E,
            resource_depletion=0.00000001055 * KG_SBE,
            acidification=0.002105015 * MOL_HPOS,
            fine_particles=0.0000000115591 * DISEASE_INCIDENCE,
            ionizing_radiations=0.00596069 * KG_BQ_U235E,
            water_depletion=0.228200547 * CUBIC_METER,
            electronic_waste=0.0243686 * ELECTRONIC_WASTE,
            primary_energy_consumption=7.8400366 * PRIMARY_MJ,
            raw_materials=0.12390367 * TONNE_MIPS,
        )


class VdrRAMImpact(ImpactFactor):
    """
    Impact factor for one GB of RAM for one month at Val de Reuil DC
    """

    def __init__(self) -> None:
        super().__init__(
            climate_change=0.267726 * KG_CO2E,
            resource_depletion=0.001086803 * KG_SBE,
            acidification=4.58e-09 * MOL_HPOS,
            fine_particles=5.97501e-09 * DISEASE_INCIDENCE,
            ionizing_radiations=0.002916121 * KG_BQ_U235E,
            water_depletion=0.109300096 * CUBIC_METER,
            electronic_waste=0.053100643 * ELECTRONIC_WASTE,
            primary_energy_consumption=0.00895852 * PRIMARY_MJ,
            raw_materials=3.49000642 * TONNE_MIPS,
        )


class RmStorageImpact(ImpactFactor):
    """
    Impact factor for one GB of storage for one month at Rueil-Malmaison DC
    """

    def __init__(self) -> None:
        super().__init__(
            climate_change=1.1922143 * KG_CO2E,
            resource_depletion=0.00000084877 * KG_SBE,
            acidification=0.004756408 * MOL_HPOS,
            fine_particles=0.00000002585 * DISEASE_INCIDENCE,
            ionizing_radiations=0.041780379 * KG_BQ_U235E,
            water_depletion=0.4456003 * CUBIC_METER,
            electronic_waste=0.1535267 * ELECTRONIC_WASTE,
            primary_energy_consumption=12.1600201 * PRIMARY_MJ,
            raw_materials=0.53460201 * TONNE_MIPS,
        )


class VdrRamStorageImpact(ImpactFactor):
    """
    Impact factor for one GB of storage for one month at Val de Reuil DC
    """

    def __init__(self) -> None:
        super().__init__(
            climate_change=1.1922143 * KG_CO2E,
            resource_depletion=0.004756408 * KG_SBE,
            acidification=8.4877e-07 * MOL_HPOS,
            fine_particles=2.585e-08 * DISEASE_INCIDENCE,
            ionizing_radiations=0.041780379 * KG_BQ_U235E,
            water_depletion=0.4456003 * CUBIC_METER,
            electronic_waste=0.53460201 * ELECTRONIC_WASTE,
            primary_energy_consumption=0.1535267 * PRIMARY_MJ,
            raw_materials=12.1600201 * TONNE_MIPS,
        )
