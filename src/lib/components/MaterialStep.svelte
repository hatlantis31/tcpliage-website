<!-- MaterialStep.svelte -->
<script>
  export let design;
  
  const materials = [
    { id: 'acier', name: 'Acier' },
    { id: 'aluminium', name: 'Aluminium' },
    { id: 'inox', name: 'Inox' }
  ];
</script>

<div>
  <h2 class="title is-4">Choisissez votre matériau</h2>
  <div class="columns is-multiline">
    {#each materials as material}
      <div class="column is-4">
        <div 
          class="box has-text-centered {design.material === material.id ? 'is-selected' : ''}"
          on:click={() => design.material = material.id}
        >
          <p class="title is-5">{material.name}</p>
        </div>
      </div>
    {/each}
  </div>
</div>

<style>
  .is-selected {
    border: 2px solid #485fc7;
  }
  .box {
    cursor: pointer;
  }
</style>