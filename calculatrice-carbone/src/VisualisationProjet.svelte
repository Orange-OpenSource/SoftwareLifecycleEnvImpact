<script>
	import TreeView from './TreeView.svelte'
	let children = [
		{
			name: "Project",
			type: "type",
            parent : "",
			children: [
				{
					name: "Build",
					type: "type",
                    parent : "Project",
                    children: [
						{
							name: "Management",
							type: "type",
							parent: "Project/Build"
						},
						{
							name: "Specifications",
							type: "type",
							parent: "Project/Build"
						},
                        {
							name: "Implementation",
							type: "type",
							parent: "Project/Build"
						}
					]
				},
				{
					name: "Run",
					type: "type",
					children: [
						{
							name: "Maintenance",
							type: "type",
							parent: "Project/Run"
						},
						{
							name: "Hosting",
							type: "type",
							parent: "Project/Run"
						}
					]
				}
			]
		}
	]
</script>

<div class="container">

    <div class="row h-100">


      <div class="col">

        <div class="row" style="padding-top : 20px;">
            <div style="max-width : 200px;">
                <input type="email" class="form-control" id="nameproject" placeholder="Name project">
            </div>
            <button type="button" class="btn btn-light" style="max-width : 200px; margin-right: 20px;">Compare</button>
            <button type="button" class="btn btn-light" style="max-width : 200px;">Project</button>
        </div>

        <strong>Preview</strong>
        
        <div class="col">
            <TreeView {children}></TreeView>
        </div>

      </div>

      <div class="col-3 border-right h-100">
          Impact by resource
      </div>
    </div>
</div>

<style>

    .container{
        max-width : 100%;
        height: 90%;
        max-height: 90%;
    }

    .border-right {
        border-left: 1px solid #ddd;
    }

</style>