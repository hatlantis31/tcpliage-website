<!-- DimensionStep.svelte -->
<script>
  import { onMount } from 'svelte';
  import { designState } from '$lib/stores/designStore';

  let shapeConfig = null;
  let isLoading = false;
  let error = null;
  let dimensions = {};
  let validationErrors = {};

  // Get the current design state
  $: design = $designState;
  
  // Watch for shape changes and load config
  $: if (design.shape) {
    loadShapeConfig(design.shape);
  }

  // Validate dimensions whenever they change
  $: {
    validateDimensions(dimensions);
    updateDesignState();
  }

  async function loadShapeConfig(shape) {
    try {
      isLoading = true;
      error = null;
      const response = await fetch(`http://localhost:8000/api/shapes/${shape}/config/` );
      
      if (!response.ok) {
        throw new Error('Failed to load shape configuration');
      }

      shapeConfig = await response.json();
      
      // Initialize dimensions with default values
      dimensions = Object.entries(shapeConfig.dimensions).reduce((acc, [key, config]) => {
        acc[key] = design.dimensions[key] || config.min;
        return acc;
      }, {});

    } catch (err) {
      error = err.message;
      console.error('Error loading shape config:', err);
    } finally {
      isLoading = false;
    }
  }

  function validateDimensions(dims) {
    if (!shapeConfig) return;

    validationErrors = {};
    
    Object.entries(shapeConfig.dimensions).forEach(([key, config]) => {
      const value = Number(dims[key]);
      
      if (isNaN(value)) {
        validationErrors[key] = 'La valeur doit être un nombre';
      } else if (value < config.min) {
        validationErrors[key] = `La valeur minimum est ${config.min}mm`;
      } else if (value > config.max) {
        validationErrors[key] = `La valeur maximum est ${config.max}mm`;
      }
    });
  }

  function updateDesignState() {
    if (Object.keys(validationErrors).length === 0) {
      designState.update(state => ({
        ...state,
        dimensions: { ...dimensions }
      }));
    }
  }

  function handleInput(key, event) {
    const value = event.target.value;
    dimensions[key] = value;
    
    // Force reactivity
    dimensions = { ...dimensions };
  }

  function isValid() {
    return Object.keys(validationErrors).length === 0;
  }
</script>

<div class="dimension-step">
  {#if isLoading}
    <div class="loading">
      <span class="loader"></span>
      <p>Chargement de la configuration...</p>
    </div>
  {:else if error}
    <div class="notification is-danger">
      <button class="delete" on:click={() => error = null}></button>
      {error}
    </div>
  {:else if !design.shape}
    <div class="notification is-warning">
      Veuillez d'abord sélectionner une forme.
    </div>
  {:else if shapeConfig}
    <div class="content">
      <h2 class="title is-4">Dimensions pour {shapeConfig.name}</h2>
      
      <div class="shape-preview">
        <img 
          src={shapeConfig.preview_url} 
          alt={shapeConfig.name} 
          width="200" 
          height="200"
        >
      </div>

      <div class="dimensions-form">
        {#each Object.entries(shapeConfig.dimensions) as [key, config]}
          <div class="field">
            <label class="label" for={key}>{config.label} (mm)</label>
            <div class="control">
              <input
                id={key}
                type="number"
                class="input {validationErrors[key] ? 'is-danger' : ''}"
                min={config.min}
                max={config.max}
                step={config.step || 1}
                value={dimensions[key]}
                on:input={(e) => handleInput(key, e)}
              >
            </div>
            
            {#if validationErrors[key]}
              <p class="help is-danger">{validationErrors[key]}</p>
            {:else}
              <p class="help">
                Min: {config.min}mm, Max: {config.max}mm
                {#if config.step !== 1}
                  , Pas: {config.step}mm
                {/if}
              </p>
            {/if}
          </div>
        {/each}
      </div>

      {#if isValid()}
        <div class="notification is-success is-light">
          <p>Les dimensions sont valides ✓</p>
          <p class="dimensions-summary">
            {#each Object.entries(dimensions) as [key, value]}
              <span>{shapeConfig.dimensions[key].label}: {value}mm</span>
            {/each}
          </p>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .dimension-step {
    padding: 1rem;
  }

  .loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    padding: 2rem;
  }

  .loader {
    width: 2rem;
    height: 2rem;
    border: 3px solid #f3f3f3;
    border-top: 3px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .shape-preview {
    display: flex;
    justify-content: center;
    margin: 1rem 0;
    padding: 1rem;
    background: #f5f5f5;
    border-radius: 4px;
  }

  .shape-preview img {
    max-width: 200px;
    height: auto;
  }

  .dimensions-form {
    max-width: 400px;
    margin: 0 auto;
  }

  .field {
    margin-bottom: 1.5rem;
  }

  .dimensions-summary {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-top: 0.5rem;
    font-size: 0.9em;
  }

  .dimensions-summary span {
    background: rgba(255, 255, 255, 0.5);
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .dimensions-form {
      max-width: 100%;
    }

    .shape-preview img {
      max-width: 150px;
    }
  }
</style>
