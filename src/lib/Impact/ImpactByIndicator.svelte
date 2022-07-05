<script>
    export let impactByIndicator;
</script>
{#if impactByIndicator != undefined}
    <h5>By indicator</h5>

    <ul>
        <li>Acidification: {impactByIndicator.task_impact.ACIDIFICATION}</li>
        <li>Climate change: {impactByIndicator.task_impact.CLIMATE_CHANGE}</li>
        <li>Electronic waste: {impactByIndicator.task_impact.ELECTRONIC_WASTE}</li>
        <li>Fine particles: {impactByIndicator.task_impact.FINE_PARTICLES}</li>
        <li>Ionizing radiations: {impactByIndicator.task_impact.IONIZING_RADIATIONS}</li>
        <li>Primary energy: {impactByIndicator.task_impact.PRIMARY_ENERGY}</li>
        <li>Raw materials: {impactByIndicator.task_impact.RAW_MATERIALS}</li>
        <li>Resource depletion: {impactByIndicator.task_impact.RESOURCE_DEPLETION}</li>
        <li>Water depletion: {impactByIndicator.task_impact.WATER_DEPLETION}</li>
    </ul>
{/if}

