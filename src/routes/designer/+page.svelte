<!-- MetalDesigner.svelte - Main container component -->
<script>
  import { onMount } from 'svelte';
  import MaterialSelector from '$lib/components/steps/MaterialSelector.svelte';
  import ShapeSelector from '$lib/components/steps/ShapeSelector.svelte';
  import ShapeEditor from '$lib/components/steps/ShapeEditor.svelte';
  import CoatingSelector from '$lib/components/steps/CoatingSelector.svelte';
  import DesignSummary from '$lib/components/steps/DesignSummary.svelte';
  
  // State for the entire design process
  let currentStep = 1;
  let design = {
    material: null,
    shape: null,
    cutouts: [],
    coating: null
  };
  
  // Step definitions
  const steps = [
    { id: 1, name: 'Material', component: MaterialSelector },
    { id: 2, name: 'Shape', component: ShapeSelector },
    { id: 3, name: 'Customize', component: ShapeEditor },
    { id: 4, name: 'Coating', component: CoatingSelector },
    { id: 5, name: 'Summary', component: DesignSummary }
  ];
  
  // Navigation functions
  function goToStep(step) {
    if (step < 1) step = 1;
    if (step > steps.length) step = steps.length;
    currentStep = step;
  }
  
  function nextStep() {
    goToStep(currentStep + 1);
  }
  
  function prevStep() {
    goToStep(currentStep - 1);
  }
  
  // Handle updating design from child components
  function updateDesign(event) {
    const { field, value } = event.detail;
    design[field] = value;
  }
  
  // Submit the design to the backend
  async function submitDesign() {
    try {
      const response = await fetch('/api/metal-designs/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(design)
      });
      
      if (response.ok) {
        alert('Design submitted successfully! You will receive a price quote soon.');
      } else {
        alert('Error submitting design. Please try again.');
      }
    } catch (error) {
      console.error('Error submitting design:', error);
      alert('Error submitting design. Please try again.');
    }
  }
</script>

<div class="container">
  <h1 class="title is-2 has-text-centered my-5">Custom Metal Piece Designer</h1>
  
  <!-- Progress bar -->
  <div class="columns">
    <div class="column is-10 is-offset-1">
      <progress class="progress is-primary" value={currentStep} max={steps.length}></progress>
      
      <div class="steps-indicator">
        {#each steps as step}
          <div class="step-item {currentStep >= step.id ? 'is-active' : ''}">
            <div class="step-marker">{step.id}</div>
            <div class="step-details">{step.name}</div>
          </div>
        {/each}
      </div>
    </div>
  </div>
  
  <!-- Current step component -->
  <div class="columns">
    <div class="column is-10 is-offset-1">
      <div class="box p-5">
        <svelte:component 
          this={steps[currentStep - 1].component} 
          {design}
          on:update={updateDesign}
        />
      </div>
      
      <!-- Navigation buttons -->
      <div class="buttons is-centered mt-4">
        {#if currentStep > 1}
          <button class="button is-medium" on:click={prevStep}>
            <span class="icon">
              <i class="fas fa-arrow-left"></i>
            </span>
            <span>Previous</span>
          </button>
        {/if}
        
        {#if currentStep < steps.length}
          <button class="button is-primary is-medium" on:click={nextStep}>
            <span>Next</span>
            <span class="icon">
              <i class="fas fa-arrow-right"></i>
            </span>
          </button>
        {:else}
          <button class="button is-success is-medium" on:click={submitDesign}>
            <span class="icon">
              <i class="fas fa-check"></i>
            </span>
            <span>Submit Design</span>
          </button>
        {/if}
      </div>
    </div>
  </div>
</div>

<style>
  .steps-indicator {
    display: flex;
    justify-content: space-between;
    margin: 1rem 0;
  }
  
  .step-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
  }
  
  .step-marker {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: #dbdbdb;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-weight: bold;
  }
  
  .step-item.is-active .step-marker {
    background-color: #00d1b2;
  }
  
  .step-details {
    margin-top: 0.5rem;
    font-size: 0.85rem;
    color: #4a4a4a;
  }
  
  .step-item.is-active .step-details {
    font-weight: bold;
    color: #363636;
  }
</style>