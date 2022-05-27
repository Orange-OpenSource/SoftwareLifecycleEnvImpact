<script>
    export let impactByIndicator;
</script>
{#if impactByIndicator != undefined}
    <h5>By indicator</h5>

    <div class="row d-flex justify-content-start">
        <ul>
            <li>Acidification = {impactByIndicator.ACIDIFICATION}</li>
            <li>Climate change = {impactByIndicator.CLIMATE_CHANGE}</li>
            <li>Electronic waste = {impactByIndicator.ELECTRONIC_WASTE}</li>
            <li>Fine particles = {impactByIndicator.FINE_PARTICLES}</li>
            <li>Ionizing radiations = {impactByIndicator.IONIZING_RADIATIONS}</li>
            <li>Primary energy = {impactByIndicator.PRIMARY_ENERGY}</li>
            <li>Raw materials = {impactByIndicator.RAW_MATERIALS}</li>
            <li>Resource depletion = {impactByIndicator.RESOURCE_DEPLETION}</li>
            <li>Water depletion = {impactByIndicator.WATER_DEPLETION}</li>
        </ul>
    </div>
{/if}

