<!-- src/routes/designer/+page.svelte -->
<script>
  import { onMount } from 'svelte';
  import MaterialSelector from '$lib/components/steps/MaterialSelector.svelte';
  import ShapeSelector from '$lib/components/steps/ShapeSelector.svelte';
  import ShapeEditor from '$lib/components/steps/ShapeEditor.svelte';
  import CoatingSelector from '$lib/components/steps/CoatingSelector.svelte';
  import DesignSummary from '$lib/components/steps/DesignSummary.svelte';
  import { v4 as uuidv4 } from 'uuid';
  
  // State for the entire design process
  let currentStep = 1;
  let design = {
    id: uuidv4(),
    material: null,
    shape: null,
    cutouts: [],
    coating: null,
    created_at: new Date().toISOString()
  };
  
  // Submission state
  let isSubmitting = false;
  let submitSuccess = null;
  let submitError = null;
  
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
  
  // Validate current step before proceeding
  function validateCurrentStep() {
    switch (currentStep) {
      case 1: // Material
        return !!design.material;
      case 2: // Shape
        return !!design.shape && !!design.shape.dimensions;
      case 3: // Customize (always valid)
        return true;
      case 4: // Coating
        return !!design.coating;
      default:
        return true;
    }
  }
  
  // Submit the design to the backend
  async function submitDesign() {
    try {
      isSubmitting = true;
      submitSuccess = null;
      submitError = null;
      
      // Prepare data for submission
      const designData = {
        material_id: design.material?.id,
        shape_template_id: design.shape?.id,
        shape_dimensions: design.shape?.dimensions,
        cutouts: design.cutouts,
        coating_id: design.coating?.id,
        color_id: design.coating?.color?.id,
        notes: ''
      };
      
      const response = await fetch('/api/metal-piece/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(designData)
      });
      
      if (response.ok) {
        const result = await response.json();
        submitSuccess = 'Design submitted successfully! You will receive a price quote soon.';
        // Clear or reset the design
        // design = { id: uuidv4(), material: null, shape: null, cutouts: [], coating: null };
      } else {
        const errorData = await response.json();
        submitError = errorData.error || 'Error submitting design. Please try again.';
      }
    } catch (error) {
      console.error('Error submitting design:', error);
      submitError = 'Error connecting to server. Please try again later.';
    } finally {
      isSubmitting = false;
    }
  }
  
  // Check if we can proceed to the next step
  $: canProceed = validateCurrentStep();
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
      
      <!-- Display validation warnings -->
      {#if !canProceed && currentStep < steps.length}
        <div class="notification is-warning mt-3">
          <p>
            {#if currentStep === 1}
              Please select a material to continue.
            {:else if currentStep === 2}
              Please specify a shape and its dimensions to continue.
            {:else if currentStep === 4}
              Please select a coating to continue.
            {:else}
              Please complete this step before continuing.
            {/if}
          </p>
        </div>
      {/if}
      
      <!-- Submission messages -->
      {#if submitSuccess}
        <div class="notification is-success mt-3">
          <p>{submitSuccess}</p>
        </div>
      {/if}
      
      {#if submitError}
        <div class="notification is-danger mt-3">
          <p>{submitError}</p>
        </div>
      {/if}
      
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
          <button 
            class="button is-primary is-medium" 
            on:click={nextStep}
            disabled={!canProceed}
          >
            <span>Next</span>
            <span class="icon">
              <i class="fas fa-arrow-right"></i>
            </span>
          </button>
        {:else}
          <button 
            class="button is-success is-medium" 
            on:click={submitDesign}
            disabled={isSubmitting}
          >
            <span class="icon">
              <i class="fas fa-check"></i>
            </span>
            <span>{isSubmitting ? 'Submitting...' : 'Submit Design'}</span>
          </button>
        {/if}
      </div>
    </div>
  </div>
  
  <!-- Design overview -->
  {#if currentStep > 1}
    <div class="columns mt-5">
      <div class="column is-8 is-offset-2">
        <div class="box">
          <h3 class="title is-5">Design Overview</h3>
          <div class="columns">
            <div class="column is-4">
              <div class="has-text-weight-bold">Material</div>
              <p>{design.material?.name || 'Not selected'}</p>
            </div>
            <div class="column is-4">
              <div class="has-text-weight-bold">Shape</div>
              <p>
                {#if design.shape}
                  {design.shape.name} 
                  {#if design.shape.dimensions}
                    {#if design.shape.id === 'circle'}
                      (Ø{design.shape.dimensions.diameter}mm)
                    {:else}
                      ({design.shape.dimensions.width}×{design.shape.dimensions.height}mm)
                    {/if}
                  {/if}
                {:else}
                  Not selected
                {/if}
              </p>
            </div>
            <div class="column is-4">
              <div class="has-text-weight-bold">Cutouts & Coating</div>
              <p>{design.cutouts?.length || 0} cutouts, {design.coating?.name || 'No coating'}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  {/if}
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