<!-- ShapeSelector.svelte -->
<script>
  import { createEventDispatcher } from 'svelte';
  
  export let design;
  
  const dispatch = createEventDispatcher();
  
  // Shape options
  const shapes = [
    { id: 'rectangle', name: 'Rectangle', description: 'Simple rectangular piece', svg: 'M10,10 L190,10 L190,90 L10,90 Z' },
    { id: 'circle', name: 'Circle', description: 'Circular piece', svg: 'M100,50 a50,50 0 1,0 0.1,0 Z' },
    { id: 'triangle', name: 'Triangle', description: 'Triangular piece', svg: 'M100,10 L190,90 L10,90 Z' },
    { id: 'L-shape', name: 'L-Shape', description: 'L-shaped piece', svg: 'M10,10 L90,10 L90,50 L150,50 L150,90 L10,90 Z' }
  ];
  
  // Custom dimensions for the selected shape
  let dimensions = {
    width: 100,
    height: 100,
    diameter: 100,
    thickness: 3
  };
  
  function selectShape(shape) {
    // Combine shape with dimensions
    const shapeWithDimensions = {
      ...shape,
      dimensions: { ...dimensions }
    };
    
    dispatch('update', {
      field: 'shape',
      value: shapeWithDimensions
    });
  }
  
  function updateDimensions() {
    if (design.shape) {
      const updatedShape = {
        ...design.shape,
        dimensions: { ...dimensions }
      };
      
      dispatch('update', {
        field: 'shape',
        value: updatedShape
      });
    }
  }
</script>

<div>
  <h2 class="title is-4">Select Shape</h2>
  <p class="subtitle is-6 mb-4">Choose the basic shape for your metal piece</p>
  
  <div class="columns is-multiline">
    {#each shapes as shape}
      <div class="column is-half">
        <div 
          class="card shape-card {design.shape?.id === shape.id ? 'is-selected' : ''}" 
          on:click={() => selectShape(shape)}
        >
          <div class="card-content">
            <div class="columns">
              <div class="column is-4">
                <svg width="100%" height="100" viewBox="0 0 200 100">
                  <path d={shape.svg} fill="#ccc" stroke="#888" stroke-width="2"/>
                </svg>
              </div>
              <div class="column">
                <p class="title is-5">{shape.name}</p>
                <p class="subtitle is-6">{shape.description}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    {/each}
  </div>
  
  {#if design.shape}
    <div class="box mt-5">
      <h3 class="title is-5">Dimensions</h3>
      
      <div class="columns">
        {#if design.shape.id !== 'circle'}
          <div class="column">
            <div class="field">
              <label class="label">Width (mm)</label>
              <div class="control">
                <input 
                  class="input" 
                  type="number" 
                  min="10" 
                  max="1000" 
                  bind:value={dimensions.width}
                  on:change={updateDimensions}
                >
              </div>
            </div>
          </div>
          
          <div class="column">
            <div class="field">
              <label class="label">Height (mm)</label>
              <div class="control">
                <input 
                  class="input" 
                  type="number" 
                  min="10" 
                  max="1000" 
                  bind:value={dimensions.height}
                  on:change={updateDimensions}
                >
              </div>
            </div>
          </div>
        {:else}
          <div class="column">
            <div class="field">
              <label class="label">Diameter (mm)</label>
              <div class="control">
                <input 
                  class="input" 
                  type="number" 
                  min="10" 
                  max="1000" 
                  bind:value={dimensions.diameter}
                  on:change={updateDimensions}
                >
              </div>
            </div>
          </div>
        {/if}
        
        <div class="column">
          <div class="field">
            <label class="label">Thickness (mm)</label>
            <div class="control">
              <input 
                class="input" 
                type="number" 
                min="0.5" 
                max="50" 
                step="0.5"
                bind:value={dimensions.thickness}
                on:change={updateDimensions}
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .shape-card {
    cursor: pointer;
    transition: all 0.3s ease;
    height: 100%;
  }
  
  .shape-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  }
  
  .shape-card.is-selected {
    border: 2px solid #00d1b2;
    box-shadow: 0 5px 15px rgba(0,209,178,0.3);
  }
</style>