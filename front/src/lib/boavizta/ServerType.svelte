<script lang="ts">
	import type { ServerImpact } from "./api/model/serverImpact";
    import { getDefaultModelsName, getServerImpactByModelName } from "./api/server";
import EnvironmentalImpact from "./EnvironmentalImpact.svelte";

    let defaultServers = getDefaultModelsName()

    let selectedServerName: string
    let selectedServerImpact: ServerImpact

    $: selectedServerName, updateImpact()

    async function updateImpact(){
        if(selectedServerName != undefined){
            selectedServerImpact = await getServerImpactByModelName(selectedServerName)
        }
    }

</script>

<div class="container">
    {#await defaultServers}
        <div class="spinner-border" role="status"/>
    {:then defaultServers}
            <label for="serverName">Server type</label>
            <select bind:value={selectedServerName} class="form-control" id="serverName">
                {#each defaultServers as serverName}
                    <option value={serverName}>
                        {serverName}
                    </option>
                {/each}
            </select>
    {:catch error}
        <p style="color: red">{error.message}</p>
    {/await}

    <EnvironmentalImpact impact={selectedServerImpact}/>
</div>

