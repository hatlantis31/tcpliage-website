// YourPage.svelte
<script>
<<<<<<< HEAD
  import MetalDesigner from '$lib/components/MetalDesigner.svelte';
</script>

<main>
  <MetalDesigner />
</main>
=======
  import { onMount } from 'svelte';
  import { fade } from 'svelte/transition';
  import { designState, designPieces } from '$lib/stores/designStore';
  import MaterialStep from '$lib/components/MaterialStep.svelte';
  import ShapeStep from '$lib/components/ShapeStep.svelte';
  import DimensionStep from '$lib/components/DimensionStep.svelte';
  import DesignPreview from '$lib/components/DesignPreview.svelte';

  let currentStep = 1;
  let isLoading = false;
  let error = null;

  // Use the store directly with $
  $: design = $designState;

  function handleUpdate(event) {
    const newData = event.detail;
    console.log('Updating design with:', newData); // Debug log
    designState.update(state => ({ ...state, ...newData }));
  }

  $: {
    console.log('Current design state:', design); // Debug log
    console.log('Step valid:', isStepValid()); // Debug log
  }

  $: isStepValid = () => {
    switch(currentStep) {
      case 1: 
        console.log('Checking material:', design?.material); // Debug log
        return Boolean(design?.material);
      case 2: 
        return Boolean(design?.shape);
      case 3: 
        return design?.dimensions && Object.keys(design.dimensions).length > 0;
      default: 
        return false;
    }
  };

  function nextStep() {
    if (currentStep < 3 && isStepValid()) {
      currentStep += 1;
    }
  }

  function prevStep() {
    if (currentStep > 1) {
      currentStep -= 1;
    }
  }

  async function submitDesign() {
    isLoading = true;
    error = null;
    try {
      const response = await fetch('http://localhost:8000/api/validate-design/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...design,
          pieces: $designPieces
        })
      });
      
      const result = await response.json();
      if (result.valid) {
        const saveResponse = await fetch('http://localhost:8000/api/designs/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: 'New Design',
            pieces: $designPieces
          })
        });
        
        if (saveResponse.ok) {
          // Handle success
          console.log('Design saved successfully');
          // You might want to redirect or show a success message
        }
      }
    } catch (err) {
      error = err.message;
      console.error('Error:', err);
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="container p-4">
  <div class="columns is-centered">
    <div class="column is-12-mobile is-10-tablet is-8-desktop">
      {#if error}
        <div class="notification is-danger">
          {error}
        </div>
      {/if}

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
        {#key currentStep}
          <div transition:fade>
            {#if currentStep === 1}
              <MaterialStep 
                {design} 
                on:update={handleUpdate}
              />
            {:else if currentStep === 2}
              <ShapeStep 
                {design} 
                on:update={handleUpdate}
              />
            {:else}
              <DimensionStep 
                {design} 
                on:update={handleUpdate}
              />
            {/if}
          </div>
        {/key}

        <div class="buttons mt-5 is-centered">
          {#if currentStep > 1}
            <button class="button" on:click={prevStep}>
              <span class="icon">
                <i class="fas fa-arrow-left"></i>
              </span>
              <span>Précédent</span>
            </button>
          {/if}
          
          {#if currentStep < 3}
            <button 
              class="button is-primary" 
              disabled={!isStepValid()} 
              on:click={nextStep}
            >
              <span>Suivant</span>
              <span class="icon">
                <i class="fas fa-arrow-right"></i>
              </span>
            </button>
          {:else}
            <button 
              class="button is-success" 
              disabled={!isStepValid() || isLoading} 
              on:click={submitDesign}
            >
              {#if isLoading}
                <span class="icon">
                  <i class="fas fa-spinner fa-spin"></i>
                </span>
                <span>Chargement...</span>
              {:else}
                <span class="icon">
                  <i class="fas fa-check"></i>
                </span>
                <span>Valider</span>
              {/if}
            </button>
          {/if}
        </div>
      </div>
      
      <div class="mt-6">
        <DesignPreview {design} />
      </div>
    </div>
  </div>
</div>

<style>
  .steps {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;
    position: relative;
  }
  
  .step-item {
    flex: 1;
    text-align: center;
    position: relative;
  }

  .step-item:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 1rem;
    width: 100%;
    height: 2px;
    background-color: #dbdbdb;
    left: 50%;
  }

  .step-marker {
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    background-color: #dbdbdb;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 0.5rem;
    position: relative;
    z-index: 1;
  }

  .step-details {
    color: #7a7a7a;
  }

  .step-item.is-active .step-marker {
    background-color: #485fc7;
  }

  .step-item.is-active .step-details {
    color: #363636;
    font-weight: 600;
  }

  .step-item.is-active:not(:last-child)::after {
    background-color: #485fc7;
  }

  .box {
    margin-top: 2rem;
    padding: 2rem;
  }

  .buttons {
    margin-top: 2rem;
    display: flex;
    justify-content: space-between;
  }

  @media screen and (max-width: 768px) {
    .step-details {
      display: none;
    }
    
    .step-item:not(:last-child)::after {
      top: 0.75rem;
    }
    
    .step-marker {
      width: 1.5rem;
      height: 1.5rem;
      font-size: 0.875rem;
    }
  }
</style>
>>>>>>> c12881765c31cf1adc41de23ea8096dac86cd4c9
