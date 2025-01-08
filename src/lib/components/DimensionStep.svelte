<script>
  import { onMount } from 'svelte';
  export let design;
  let shapeConfig = {};

  onMount(async () => {
    const response = await fetch(`http://localhost:8000/api/shapes/${design.shape}/config/`);
    shapeConfig = await response.json();
  });

  function updateDimension(key, value) {
    design.dimensions = {...design.dimensions, [key]: Number(value)};
  }
</script>

<div>
  <h2 class="title is-4">Définissez les dimensions</h2>
  {#each Object.entries(shapeConfig.dimensions || {}) as [key, config]}
    <div class="field">
      <label class="label">{config.label} (mm)</label>
      <div class="control">
        <input
          type="number"
          class="input"
          min={config.min}
          max={config.max}
          step={config.step || 1}
          value={design.dimensions[key]}
          on:input={(e) => updateDimension(key, e.target.value)}
        >
      </div>
      <p class="help">Min: {config.min}mm, Max: {config.max}mm</p>
    </div>
  {/each}
</div>

<style>
  .field {
    margin-bottom: 1.5rem;
  }
</style>