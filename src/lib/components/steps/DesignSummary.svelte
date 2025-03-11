<!-- DesignSummary.svelte -->
<script>
  export let design;
  
  // Helper to format the shape description
  function getShapeDescription(shape) {
    if (!shape) return 'No shape selected';
    
    let description = `${shape.name}`;
    
    if (shape.dimensions) {
      if (shape.id === 'circle') {
        description += ` (${shape.dimensions.diameter}mm diameter, ${shape.dimensions.thickness}mm thick)`;
      } else {
        description += ` (${shape.dimensions.width}mm × ${shape.dimensions.height}mm, ${shape.dimensions.thickness}mm thick)`;
      }
    }
    
    return description;
  }
  
  // Helper to format the coating description
  function getCoatingDescription(coating) {
    if (!coating) return 'No coating selected';
    
    let description = `${coating.name}`;
    
    if (coating.color) {
      description += ` - ${coating.color.name} color`;
    }
    
    return description;
  }
</script>

<div>
  <h2 class="title is-4">Design Summary</h2>
  <p class="subtitle is-6 mb-4">Review your custom metal piece design</p>
  
  <div class="box">
    <table class="table is-fullwidth">
      <tbody>
        <tr>
          <th>Material</th>
          <td>{design.material ? design.material.name : 'Not selected'}</td>
        </tr>
        <tr>
          <th>Shape</th>
          <td>{design.shape ? getShapeDescription(design.shape) : 'Not selected'}</td>
        </tr>
        <tr>
          <th>Cutouts</th>
          <td>{design.cutouts?.length || 0} custom cutouts</td>
        </tr>
        <tr>
          <th>Coating</th>
          <td>{design.coating ? getCoatingDescription(design.coating) : 'Not selected'}</td>
        </tr>
      </tbody>
    </table>
  </div>
  
  <div class="box mt-4">
    <h3 class="title is-5">Design Preview</h3>
    
    <div class="has-text-centered">
      <!-- Simple preview rendering -->
      <svg width="300" height="200" viewBox="0 0 300 200">
        {#if design.shape}
          <!-- Base shape -->
          {#if design.shape.id === 'rectangle'}
            <rect 
              x="50" 
              y="50" 
              width="200" 
              height="100" 
              fill={design.coating?.color?.hex || '#CCC'} 
              stroke="#333"
              stroke-width="2"
            />
          {:else if design.shape.id === 'circle'}
            <circle 
              cx="150" 
              cy="100" 
              r="75" 
              fill={design.coating?.color?.hex || '#CCC'} 
              stroke="#333"
              stroke-width="2"
            />
          {:else if design.shape.id === 'triangle'}
            <polygon 
              points="150,25 250,175 50,175" 
              fill={design.coating?.color?.hex || '#CCC'} 
              stroke="#333"
              stroke-width="2"
            />
          {:else if design.shape.id === 'L-shape'}
            <path 
              d="M50,50 L150,50 L150,100 L200,100 L200,175 L50,175 Z" 
              fill={design.coating?.color?.hex || '#CCC'} 
              stroke="#333"
              stroke-width="2"
            />
          {/if}
          
          <!-- Cutouts representation (simplified) -->
          {#if design.cutouts && design.cutouts.length > 0}
            {#each design.cutouts as cutout, i}
              <circle
                cx={50 + i * 30} 
                cy="50"
                r="10"
                fill="white"
                stroke="red"
                stroke-width="1"
              />
            {/each}
          {/if}
        {:else}
          <text x="150" y="100" text-anchor="middle">No design to preview</text>
        {/if}
      </svg>
    </div>
    
    <p class="has-text-centered mt-3">Submit your design to receive a price quote.</p>
  </div>
</div>