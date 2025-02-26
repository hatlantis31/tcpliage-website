<script>
  import { createEventDispatcher } from 'svelte';
  
  export let design;
  const dispatch = createEventDispatcher();
  
  const materials = [
    { id: 'acier', name: 'Acier' },
    { id: 'aluminium', name: 'Aluminium' },
    { id: 'inox', name: 'Inox' }
  ];

  function selectMaterial(materialId) {
    console.log('Selecting material:', materialId); // Debug log
    dispatch('update', { material: materialId });
  }

  $: console.log('Current design in MaterialStep:', design); // Debug log
</script>

<div>
  <h2 class="title is-4">Choisissez votre matériau</h2>
  <div class="columns is-multiline">
    {#each materials as material}
      <div class="column is-4">
        <div 
          class="box has-text-centered {design?.material === material.id ? 'is-selected' : ''}"
          on:click={() => selectMaterial(material.id)}
        >
          <p class="title is-5">{material.name}</p>
          {#if design?.material === material.id}
            <span class="icon has-text-success">
              <i class="fas fa-check"></i>
            </span>
          {/if}
        </div>
      </div>
    {/each}
  </div>
</div>

<style>
  .is-selected {
    border: 2px solid #485fc7;
    background-color: #f5f5f5;
  }
  .box {
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
  }
  .box:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  }
  .icon {
    position: absolute;
    top: 8px;
    right: 8px;
  }
</style>
