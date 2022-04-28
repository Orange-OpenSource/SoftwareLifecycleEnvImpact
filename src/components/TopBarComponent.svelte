<script>
    import { Link } from "svelte-navigator";
    import { store } from '../stores';

    export let modelsContent;
    export let model_id;

    function emptyModelContent(){
        modelsContent = [];
        model_id = null;
    }

    function logOut(){
        emptyModelContent();
		$store = null;
	}

    function updateModelId(id){
        model_id=id;
    }

    function addModel(){

    }
</script>

{#if $store != null }
<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item">
        <Link on:click={emptyModelContent} class="nav-link" style="color:white;" to="/">Home</Link>
      </li>
      {#each modelsContent as model}
      <li class="nav-item d-flex justify-content-around" style="padding-bottom : 2px;">
          <Link class="nav-link" style="color:white;" to="../../modify/{model.id}">{model.name}</Link>
          <button on:click={updateModelId(model.id)} class="btn btn-light">Preview</button>
      </li>
        {/each}
        {#if model_id != null}
        <li class="nav-item" style="padding-bottom : 5px;">
            <button type="button" class="btn btn-primary" on:click={addModel}>Add model</button>
        </li>
        {/if}

      <li class="nav-item d-flex justify-content-end">
        <button type="button" class="btn btn-secondary" on:click={logOut}>Log out</button>
      </li>
    </ul>
  </div>
  {/if}