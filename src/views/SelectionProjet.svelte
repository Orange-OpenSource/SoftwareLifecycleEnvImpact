<script>
	import TreeView from '../components/TreeView.svelte'
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
      <div class="col-3 border-right h-100">
        <strong>My projects :</strong>

        <ul class="list-group list-group-flush">
            <li class="list-group-item">Projet 1</li>
            <li class="list-group-item">Projet 2</li>
            <li class="list-group-item">Projet 3</li>
          </ul>
      </div>
      <div class="col">
        <strong>Preview</strong>
        
        <div class="col">
            <TreeView {children}></TreeView>
        </div>

      </div>
    </div>
</div>