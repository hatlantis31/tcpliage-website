<script>
  import { onMount } from 'svelte';
  import { designState } from './stores/designStore';
  import MaterialStep from '$lib/components/MaterialStep.svelte';
  import ShapeStep from '$lib/components/ShapeStep.svelte';
  import DimensionStep from '$lib/components/DimensionStep.svelte';
  import DesignPreview from '$lib/components/DesignPreview.svelte';

  let currentStep = 1;
  let design = {
    material: '',
    shape: '',
    dimensions: {}
  };

  $: isStepValid = () => {
    switch(currentStep) {
      case 1: return design.material;
      case 2: return design.shape;
      case 3: return Object.keys(design.dimensions || {}).length > 0;
      default: return false;
    }
  };

  function nextStep() {
    if (currentStep < 3) {
      currentStep = currentStep + 1;
    }
  }

  function prevStep() {
    if (currentStep > 1) {
      currentStep = currentStep - 1;
    }
  }

  function updateDesign(newData) {
    design = { ...design, ...newData };
  }

  async function submitDesign() {
    try {
      const response = await fetch('http://localhost:8000/api/validate-design/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(design)
      });
      const result = await response.json();
      if (result.valid) {
        // Handle success
      }
    } catch (error) {
      // Handle error
    }
  }
</script>

<div class="container p-4">
  <div class="steps mb-5">
    <div class="step-item {currentStep >= 1 ? 'is-active' : ''}">
      <div class="step-marker">1</div>
      <div class="step-details">Matériau</div>
    </div>
    <div class="step-item {currentStep >= 2 ? 'is-active' : ''}">
      <div class="step-marker">2</div>
      <div class="step-details">Forme</div>
    </div>
    <div class="step-item {currentStep >= 3 ? 'is-active' : ''}">
      <div class="step-marker">3</div>
      <div class="step-details">Dimensions</div>
    </div>
  </div>

  <div class="box">
    {#if currentStep === 1}
      <MaterialStep bind:design />
    {:else if currentStep === 2}
      <ShapeStep bind:design />
    {:else}
      <DimensionStep bind:design />
    {/if}

    <div class="buttons mt-5">
      {#if currentStep > 1}
        <button class="button" on:click={prevStep}>Précédent</button>
      {/if}
      
      {#if currentStep < 3}
        <button class="button is-primary" disabled={!isStepValid()} on:click={nextStep}>
          Suivant
        </button>
      {:else}
        <button class="button is-success" disabled={!isStepValid()} on:click={submitDesign}>
          Valider
        </button>
      {/if}
    </div>
  </div>
  <DesignPreview bind:design={design} />
</div>

<style>
  .steps {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;
  }
  
  .step-item {
    flex: 1;
    text-align: center;
  }
</style>