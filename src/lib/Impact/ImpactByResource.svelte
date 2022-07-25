<script>
    import ImpactByIndicator from "./ImpactByIndicator.svelte";

    export let impactByResource;
    let entries

    function updateValues() {
        if (impactByResource != undefined){
            entries = Object.entries(impactByResource)
        }
    }
    $: impactByResource, updateValues();

</script>
{#if impactByResource != undefined}
    <ul>
        {#each entries as [key, value]}
            <li>
                {key}
                <ImpactByIndicator impactByIndicator={value}/>
            </li>
        {/each}
    </ul>
{/if}

