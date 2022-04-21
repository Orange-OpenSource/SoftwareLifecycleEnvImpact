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
  
  <style>
    div.tree {
        padding: 50px 0px 0px 96px;
        position: relative;
        text-align: start;

        line-height:300%;
    }

    div.tree:before {
        
        content: "";
        position: absolute;
        top: 3px;
        left: 15px;
        border-left: 2px dashed #a2a5b5;
        width: 1px;
        height: 100%;
    }

    div.tree:after {
        content: "";
        position: absolute;
        border-top: 2px dashed #a2a5b5;
        top: 70px;
        left: 20px;
        width: 60px;
    }

    div.tree:last-child:before {
        top: -22px;
        height: 90px;
    }

    span {
        background-color: #ececece1;
        border-radius: 3px;
        border : none;
        padding : 10px  20px 10px 20px;
        -webkit-box-shadow: 5px 5px 3px -6px #000000; 
        box-shadow: 5px 5px 3px -6px #000000;
    }
    
  </style>