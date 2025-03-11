<!-- MaterialSelector.svelte -->
<script>
  import { createEventDispatcher } from 'svelte';
  
  export let design;
  
  const dispatch = createEventDispatcher();
  
  // Material options
  const materials = [
    { id: 'steel', name: 'Steel', description: 'Durable and strong', image: '/images/materials/steel.jpg' },
    { id: 'aluminum', name: 'Aluminum', description: 'Lightweight and corrosion-resistant', image: '/images/materials/aluminum.jpg' },
    { id: 'copper', name: 'Copper', description: 'Excellent conductivity', image: '/images/materials/copper.jpg' },
    { id: 'brass', name: 'Brass', description: 'Good machinability and corrosion resistance', image: '/images/materials/brass.jpg' }
  ];
  
  function selectMaterial(material) {
    dispatch('update', {
      field: 'material',
      value: material
    });
  }
</script>

<div>
  <h2 class="title is-4">Select Material</h2>
  <p class="subtitle is-6 mb-4">Choose the material for your metal piece</p>
  
  <div class="columns is-multiline">
    {#each materials as material}
      <div class="column is-half">
        <div 
          class="card material-card {design.material?.id === material.id ? 'is-selected' : ''}" 
          on:click={() => selectMaterial(material)}
        >
          <div class="card-content">
            <div class="columns">
              <div class="column is-4">
                <figure class="image is-square">
                  <img src={material.image} alt={material.name} />
                </figure>
              </div>
              <div class="column">
                <p class="title is-5">{material.name}</p>
                <p class="subtitle is-6">{material.description}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    {/each}
  </div>
</div>

<style>
  .material-card {
    cursor: pointer;
    transition: all 0.3s ease;
    height: 100%;
  }
  
  .material-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  }
  
  .material-card.is-selected {
    border: 2px solid #00d1b2;
    box-shadow: 0 5px 15px rgba(0,209,178,0.3);
  }
</style>