<script>
    export let children  
</script>
  
  {#each children as file}
      <div class="tree">
          <span>{file.name}</span>
          {#if file.children}
              <svelte:self children={file.children} />
          {/if}
 
      </div>
   {/each}
   <div class="tree"><button class="btn btn-primary">Add task</button></div>