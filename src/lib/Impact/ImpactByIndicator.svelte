<script>
    export let impactByIndicator;

    let entries = undefined

    $: impactByIndicator, updateEntries()

    function updateEntries(){
        if (impactByIndicator != undefined){
            entries = Object.entries(impactByIndicator)
        }
    }
</script>

{#if entries != undefined}
    <ul>
        {#each entries as [key, impact]}
            {#if impact.value != 0}
                <li>
                    {key}: <b>{impact.value}</b> {impact.unit}
                </li>
            {/if}
        {/each}
    </ul>
{/if}