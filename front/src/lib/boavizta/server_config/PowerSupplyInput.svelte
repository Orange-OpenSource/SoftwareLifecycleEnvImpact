<script lang="ts">
    import type { PowerSupply } from "$lib/model/powerSupply";
    export let power_supply:PowerSupply = {}
</script>

<div class="form-group">
    <label for="psWeight">Weight (kg)</label>
    <input bind:value={power_supply.unit_weight} class="form-control" type="number" id="psWeight" min="1" max="10">
</div>