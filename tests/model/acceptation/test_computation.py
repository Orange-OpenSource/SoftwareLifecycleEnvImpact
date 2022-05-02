from model.impacts.impact_factors import ImpactsFactorsRegistry
from model.impacts.impacts import ImpactIndicator
from model.projects import StandardProject


#
# Acceptation tests on _impacts to assess that changing the inputs on a projects results in the right tasks _impacts
# updates (check propagation and computation)
#
from model.quantities import ELECTRICITY_MIX


def test_build_task_impacts() -> None:
    """Test co2 consequence of updating all project's inputs for build task"""
    s = StandardProject()

    # Dev days
    old_co2 = s.build_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.dev_days = 4432
    assert (
        s.build_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2
    )

    # Design days
    old_co2 = s.build_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.design_days = 12321414
    assert (
        s.build_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2
    )

    # Spec days
    old_co2 = s.build_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.spec_days = 14214
    assert (
        s.build_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2
    )

    # Management days
    old_co2 = s.build_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.management_days = 124421
    assert (
        s.build_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2
    )


def test_run_task_impacts() -> None:
    """Test co2 consequence of updating all project's inputs for run task"""
    s = StandardProject()
    registry = ImpactsFactorsRegistry()

    # Maintenance days
    old_co2 = s.run_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.maintenance_days = 4432
    assert s.run_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2

    # Electricity mix
    old_co2 = s.run_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    registry.electricity_mix = 4432 * ELECTRICITY_MIX
    assert registry.electricity_mix == 4432 * ELECTRICITY_MIX
    assert ImpactsFactorsRegistry().electricity_mix == 4432 * ELECTRICITY_MIX
    assert s.run_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2

    # PUE
    old_co2 = s.run_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    registry.pue = 4432.124
    assert s.run_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2

    # Servers count
    old_co2 = s.run_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.servers_count = 4432
    assert s.run_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2

    # Storage size
    old_co2 = s.run_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.storage_size = 4432
    assert s.run_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2

    # Duration
    old_co2 = s.run_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.run_duration = 4432
    assert s.run_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2

    # Average users
    old_co2 = s.run_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.avg_user = 4432
    assert (
        s.root_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2
    )

    # Average time
    old_co2 = s.run_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.avg_time = 4432
    assert s.run_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2

    # Average data
    old_co2 = s.run_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.avg_data = 4432
    assert s.run_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2


def test_dev_task_impacts() -> None:
    """Test co2 consequence of updating all project's inputs for dev task"""
    s = StandardProject()
    old_co2 = s.dev_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.dev_days = 234832443
    assert s.dev_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2


def test_design_task_impacts() -> None:
    """Test co2 consequence of updating all project's inputs for design task"""
    s = StandardProject()
    old_co2 = s.design_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.design_days = 23123
    assert (
        s.design_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2
    )


def test_spec_task_impacts() -> None:
    """Test co2 consequence of updating all project's inputs for spec task"""
    s = StandardProject()
    old_co2 = s.spec_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.spec_days = 214421
    assert (
        s.spec_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2
    )


def test_implementation_task_impacts() -> None:
    """Test co2 consequence of updating all project's inputs for implementation task"""
    s = StandardProject()

    # Dev days
    old_co2 = s.implementation_task.get_impact_by_indicator(
        ImpactIndicator.CLIMATE_CHANGE
    )
    s.dev_days = 1244
    assert (
        s.implementation_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
        != old_co2
    )

    # Design days
    old_co2 = s.implementation_task.get_impact_by_indicator(
        ImpactIndicator.CLIMATE_CHANGE
    )
    s.design_days = 14421
    assert (
        s.implementation_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
        != old_co2
    )


def test_management_task_impacts() -> None:
    """Test co2 consequence of updating all project's inputs for management task"""
    s = StandardProject()
    old_co2 = s.management_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.management_days = 3243
    assert (
        s.management_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
        != old_co2
    )


def test_maintenance_task_impacts() -> None:
    """Test co2 consequence of updating all project's inputs for maintenance task"""
    s = StandardProject()
    old_co2 = s.maintenance_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.maintenance_days = 234234
    assert (
        s.maintenance_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
        != old_co2
    )


def test_hosting_task_impacts() -> None:
    """Test co2 consequence of updating all project's inputs for hosting task"""
    s = StandardProject()

    # Electricity mix
    old_co2 = s.hosting_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    ImpactsFactorsRegistry().electricity_mix = 2.12312312 * ELECTRICITY_MIX
    assert (
        s.hosting_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
        != old_co2
    )

    # PUE
    old_co2 = s.hosting_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    ImpactsFactorsRegistry().pue = 1.2342342344
    assert (
        s.hosting_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
        != old_co2
    )

    # Servers count
    old_co2 = s.hosting_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.servers_count = 2038764923
    assert (
        s.hosting_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
        != old_co2
    )

    # Storage size
    old_co2 = s.hosting_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.storage_size = 2038764923
    assert (
        s.hosting_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
        != old_co2
    )

    # Duration
    old_co2 = s.hosting_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.run_duration = 4325
    assert (
        s.hosting_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
        != old_co2
    )


def test_usage_task_impacts() -> None:
    """Test co2 consequence of updating all project's inputs for usage task"""
    s = StandardProject()

    # Avg user
    old_co2 = s.usage_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.avg_user = 5325235435
    assert (
        s.usage_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2
    )

    # Avg time   old_co2 = s.root_task.run_task.usage_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.avg_time = 64
    assert (
        s.usage_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2
    )

    # Avg data
    old_co2 = s.usage_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.avg_data = 0.253490
    assert (
        s.usage_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2
    )

    # Duration
    old_co2 = s.usage_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE)
    s.run_duration = 5325235435
    assert (
        s.usage_task.get_impact_by_indicator(ImpactIndicator.CLIMATE_CHANGE) != old_co2
    )
