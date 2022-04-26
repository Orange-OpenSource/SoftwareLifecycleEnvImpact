<script>
    export let children;
    export let modify;
</script>
  
  {#each children as file}
      <div class="tree">
            {#if file.children}

                <div class="raw">
                    <span class="info-name">
                        {file.name}
                        {#if modify}
                        <button type="button" class="btn btn-outline-primary btn-sm btnmodifyparent">Modify</button>
                        {/if}
                    </span>
                    
                    <svelte:self children={file.children} modify={modify}/>
                </div>

            {:else}

                {#if modify}
                    <div class="raw nochildmodify">
                        <span class="info-name">
                            {file.name}
                            <button type="button" class="btn btn-outline-primary btn-sm btnmodify">Modify</button>
                        </span>
                        <span class="addtask"><button class="btn btn-primary">Add task</button></span>
                    </div>
                {:else}
                    <div class="raw nochild">
                        <span class="info-name">
                            {file.name}
                        </span>
                    </div>
                {/if}

            {/if}
      </div>
   {/each}
   {#if modify}
   <div class="tree"><button class="btn btn-primary">Add task</button></div>
   {/if}