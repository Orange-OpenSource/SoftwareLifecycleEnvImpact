<script>
    export let children  
</script>
  
  {#each children as file}
      <div class="tree">
            {#if file.children}

                <div class="raw">
                    <span class="info-name">
                        {file.name}
                        <button type="button" class="btn btn-outline-primary btn-sm btnmodifyparent">Modify</button>
                    </span>
                    
                    <svelte:self children={file.children} />
                </div>

            {:else}

                <div class="raw nochildmodify">
                    <span class="info-name">
                        {file.name}
                        <button type="button" class="btn btn-outline-primary btn-sm btnmodify">Modify</button>
                    </span>
                    <span class="addtask"><button class="btn btn-primary">Add task</button></span>
                </div>

            {/if}
      </div>
   {/each}
   <div class="tree"><button class="btn btn-primary">Add task</button></div>