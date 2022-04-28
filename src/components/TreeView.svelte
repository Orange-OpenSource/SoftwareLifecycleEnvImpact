<script>
import ModalComponent from "./ModalComponent.svelte";

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
                        <button data-bs-toggle="modal" data-bs-target="#modal{file.name}" type="button" class="btn btn-outline-primary btn-sm btnmodifyparent">Modify</button>

                        <ModalComponent task_name={file.name}>
                            <span slot="taskName">{file.name}</span>
                            <span slot="body">
                                To do
                            </span>
                        </ModalComponent>
                        {/if}
                    </span>
                    
                    <svelte:self children={file.children} modify={modify}/>
                </div>

            {:else}

                {#if modify}
                    <div class="raw nochildmodify">
                        <span class="info-name">
                            {file.name}
                            <button data-bs-toggle="modal" data-bs-target="#modal{file.name}" type="button" class="btn btn-outline-primary btn-sm btnmodify">Modify</button>

                            <ModalComponent task_name={file.name}>
                                <span slot="taskName">{file.name}</span>
                                <span slot="body">
                                    To do
                                </span>
                            </ModalComponent>
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