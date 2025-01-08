<script>
  import { onMount } from 'svelte';
  export let design;
  let shapes = [];

  onMount(async () => {
    const response = await fetch('http://localhost:8000/api/shapes/');
    shapes = await response.json();
  });
</script>

<div>
  <h2 class="title is-4">Sélectionnez une forme</h2>
  <div class="columns is-multiline">
    {#each shapes as shape}
      <div class="column is-4">
        <div 
          class="box has-text-centered {design.shape === shape.id ? 'is-selected' : ''}"
          on:click={() => design.shape = shape.id}
        >
          <figure class="image is-square">
            <img src={shape.preview_url} alt={shape.name}>
          </figure>
          <p class="title is-5 mt-2">{shape.name}</p>
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