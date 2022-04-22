<script>
    export let children  
</script>
  
  {#each children as file}
      <div class="tree">
            {#if file.children}

                <div class="raw">
                    <span class="info-name">{file.name}</span>
                    <svelte:self children={file.children} />
                </div>

            {:else}

                <div class="raw nochild">
                    <span class="info-name">{file.name}</span>
                    <span class="addtask"><button class="btn btn-primary">Add task</button></span>
                </div>

            {/if}
      </div>
   {/each}
   <div class="tree"><button class="btn btn-primary">Add task</button></div>