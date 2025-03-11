<!-- CoatingSelector.svelte -->
<script>
  import { createEventDispatcher } from 'svelte';
  
  export let design;
  
  const dispatch = createEventDispatcher();
  
  // Coating options
  const coatings = [
    { id: 'none', name: 'No Coating', description: 'Raw metal without coating', image: '/images/coatings/none.jpg' },
    { id: 'painted', name: 'Painted', description: 'Smooth painted surface', image: '/images/coatings/painted.jpg' },
    { id: 'powder-coated', name: 'Powder Coated', description: 'Durable matte finish', image: '/images/coatings/powder-coated.jpg' },
    { id: 'anodized', name: 'Anodized', description: 'Only for aluminum, corrosion-resistant', image: '/images/coatings/anodized.jpg' },
    { id: 'galvanized', name: 'Galvanized', description: 'Zinc coating for rust prevention', image: '/images/coatings/galvanized.jpg' }
  ];
  
  // Filter unavailable coatings based on selected material
  $: availableCoatings = coatings.filter(coating => {
    // Anodized only available for aluminum
    if (coating.id === 'anodized' && design.material?.id !== 'aluminum') {
      return false;
    }
    return true;
  });
  
  // Options for color (only for painted or powder-coated)
  const colorOptions = [
    { id: 'black', name: 'Black', hex: '#000000' },
    { id: 'white', name: 'White', hex: '#FFFFFF' },
    { id: 'red', name: 'Red', hex: '#FF0000' },
    { id: 'blue', name: 'Blue', hex: '#0000FF' },
    { id: 'green', name: 'Green', hex: '#008000' },
    { id: 'yellow', name: 'Yellow', hex: '#FFFF00' },
    { id: 'custom', name: 'Custom Color', hex: '#CCCCCC' }
  ];
  
  let selectedColor = colorOptions[0];
  let customColor = '#CCCCCC';
  
  function selectCoating(coating) {
    const coatingWithOptions = {
      ...coating,
      color: coating.id === 'painted' || coating.id === 'powder-coated' ? selectedColor : null
    };
    
    dispatch('update', {
      field: 'coating',
      value: coatingWithOptions
    });
  }
  
  function updateCoatingColor() {
    if (design.coating && (design.coating.id === 'painted' || design.coating.id === 'powder-coated')) {
      const updatedCoating = {
        ...design.coating,
        color: selectedColor.id === 'custom' ? { id: 'custom', name: 'Custom', hex: customColor } : selectedColor
      };
      
      dispatch('update', {
        field: 'coating',
        value: updatedCoating
      });
    }
  }
  
  // When color changes, update the coating
  $: {
    if (selectedColor && design.coating) {
      updateCoatingColor();
    }
  }
</script>

<div>
  <h2 class="title is-4">Select Coating</h2>
  <p class="subtitle is-6 mb-4">Choose a surface finish for your metal piece</p>
  
  <div class="columns is-multiline">
    {#each availableCoatings as coating}
      <div class="column is-half">
        <div 
          class="card coating-card {design.coating?.id === coating.id ? 'is-selected' : ''}" 
          on:click={() => selectCoating(coating)}
        >
          <div class="card-content">
            <div class="columns">
              <div class="column is-4">
                <figure class="image is-square">
                  <img src={coating.image} alt={coating.name} />
                </figure>
              </div>
              <div class="column">
                <p class="title is-5">{coating.name}</p>
                <p class="subtitle is-6">{coating.description}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    {/each}
  </div>
  
  {#if design.coating && (design.coating.id === 'painted' || design.coating.id === 'powder-coated')}
    <div class="box mt-5">
      <h3 class="title is-5">Color Selection</h3>
      
      <div class="field">
        <label class="label">Choose a color</label>
        <div class="control">
          <div class="columns is-multiline">
            {#each colorOptions as color}
              <div class="column is-narrow">
                <div 
                  class="color-option {selectedColor.id === color.id ? 'is-selected' : ''}"
                  style="background-color: {color.hex};"
                  on:click={() => selectedColor = color}
                >
                  {#if selectedColor.id === color.id}
                    <span class="icon has-text-white">
                      <i class="fas fa-check"></i>
                    </span>
                  {/if}
                </div>
                <p class="has-text-centered is-size-7">{color.name}</p>
              </div>
            {/each}
          </div>
        </div>
      </div>
      
      {#if selectedColor.id === 'custom'}
        <div class="field mt-3">
          <label class="label">Custom Color</label>
          <div class="control">
            <input 
              type="color" 
              bind:value={customColor}
              on:change={updateCoatingColor}
            >
          </div>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .coating-card {
    cursor: pointer;
    transition: all 0.3s ease;
    height: 100%;
  }
  
  .coating-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  }
  
  .coating-card.is-selected {
    border: 2px solid #00d1b2;
    box-shadow: 0 5px 15px rgba(0,209,178,0.3);
  }
  
  .color-option {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid #dbdbdb;
    transition: all 0.2s ease;
  }
  
  .color-option:hover {
    transform: scale(1.1);
  }
  
  .color-option.is-selected {
    border: 3px solid #363636;
  }
</style>