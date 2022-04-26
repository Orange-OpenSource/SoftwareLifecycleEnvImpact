<script lang="ts">
    import { getModel } from "../controllers/RequestController";
    import TreeView from "./TreeView.svelte";
    import {tick} from 'svelte';

    export let modify;
    export let model_id;

    let children = [];

    export async function updateTree() {
        await tick();
        children = await getModel(model_id);
    }
</script>

<div class="col scroll">
    <TreeView children={children} modify={modify}></TreeView>
</div>