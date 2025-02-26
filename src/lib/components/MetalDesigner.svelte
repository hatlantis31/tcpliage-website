<!-- MetalDesigner.svelte -->
<script>
  import { onMount } from 'svelte';
  
  // Step management
  let currentStep = 0;
  const steps = [
    { name: "Dimensions", description: "Set the basic dimensions of your metal piece" },
    { name: "Shape", description: "Draw or select the shape of your metal piece" },
    { name: "Features", description: "Add holes, cuts, and other features" },
    { name: "Material", description: "Select material type and thickness" },
    { name: "Review", description: "Review your design before submission" }
  ];
  
  // Designer state
  let designState = {
    dimensions: { width: 100, height: 100, depth: 5 },
    material: { type: "steel", thickness: 2, finish: "none" },
    shape: "rectangle",
    features: [],
    customPath: "",
    notes: ""
  };
  
  // SVG drawing variables
  let svgWidth = 500;
  let svgHeight = 300;
  let isDrawing = false;
  let startPoint = { x: 0, y: 0 };
  let currentPath = "";
  let paths = [];
  
  // Material options
  const materialOptions = [
    { id: "steel", name: "Steel", minThickness: 0.5, maxThickness: 10 },
    { id: "aluminum", name: "Aluminum", minThickness: 0.5, maxThickness: 8 },
    { id: "copper", name: "Copper", minThickness: 0.5, maxThickness: 5 },
    { id: "brass", name: "Brass", minThickness: 0.5, maxThickness: 5 }
  ];
  
  // Feature types
  const featureTypes = [
    { id: "hole", name: "Hole", icon: "circle" },
    { id: "slot", name: "Slot", icon: "rectangle" },
    { id: "cutout", name: "Cut-out", icon: "scissors" },
    { id: "bend", name: "Bend", icon: "fold" }
  ];

  // Navigation functions
  function nextStep() {
    if (currentStep < steps.length - 1) {
      currentStep += 1;
    }
  }
  
  function prevStep() {
    if (currentStep > 0) {
      currentStep -= 1;
    }
  }
  
  // Drawing functions
  function startDrawing(e) {
    if (currentStep === 1) { // Only in shape step
      isDrawing = true;
      const rect = e.target.getBoundingClientRect();
      startPoint = {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
      };
      currentPath = `M${startPoint.x},${startPoint.y}`;
    }
  }
  
  function continueDrawing(e) {
    if (isDrawing) {
      const rect = e.target.getBoundingClientRect();
      const point = {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
      };
      currentPath += ` L${point.x},${point.y}`;
    }
  }
  
  function endDrawing() {
    if (isDrawing) {
      isDrawing = false;
      paths.push(currentPath);
      designState.customPath = paths.join(" ");
    }
  }
  
  function addFeature(type) {
    designState.features.push({
      id: `feature-${designState.features.length}`,
      type: type,
      x: svgWidth / 2,
      y: svgHeight / 2,
      size: type === 'hole' ? 10 : 20
    });
  }
  
  // Submission function
  async function submitDesign() {
    try {
      const response = await fetch('/api/metal-design/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(designState)
      });
      
      if (response.ok) {
        const result = await response.json();
        alert('Design submitted! You will receive pricing information soon.');
      } else {
        throw new Error('Failed to submit design');
      }
    } catch (error) {
      console.error('Error submitting design:', error);
      alert('There was a problem submitting your design. Please try again.');
    }
  }
  
  // Reset the design
  function resetDesign() {
    paths = [];
    designState.customPath = "";
    designState.features = [];
  }
  
  onMount(() => {
    // Any initialization code here
  });
</script>

<div class="metal-designer container">
  <h1 class="title is-2">Custom Metal Piece Designer</h1>
  
  <!-- Progress indicator -->
  <div class="steps-container mb-5">
    <ul class="steps">
      {#each steps as step, index}
        <li class="steps-segment {currentStep >= index ? 'is-active' : ''}">
          <span class="steps-marker">{index + 1}</span>
          <div class="steps-content">
            <p class="is-size-5">{step.name}</p>
            <p class="is-size-7">{step.description}</p>
          </div>
        </li>
      {/each}
    </ul>
  </div>
  
  <!-- Steps content -->
  <div class="box">
    {#if currentStep === 0}
      <!-- Step 1: Dimensions -->
      <h2 class="title is-4">Basic Dimensions</h2>
      <div class="columns">
        <div class="column">
          <div class="field">
            <label class="label">Width (mm)</label>
            <div class="control">
              <input class="input" type="number" bind:value={designState.dimensions.width} min="10" max="1000">
            </div>
          </div>
        </div>
        <div class="column">
          <div class="field">
            <label class="label">Height (mm)</label>
            <div class="control">
              <input class="input" type="number" bind:value={designState.dimensions.height} min="10" max="1000">
            </div>
          </div>
        </div>
        <div class="column">
          <div class="field">
            <label class="label">Depth (mm)</label>
            <div class="control">
              <input class="input" type="number" bind:value={designState.dimensions.depth} min="0.5" max="50">
            </div>
          </div>
        </div>
      </div>
    {:else if currentStep === 1}
      <!-- Step 2: Shape -->
      <h2 class="title is-4">Define Shape</h2>
      <div class="columns">
        <div class="column is-4">
          <div class="field">
            <label class="label">Basic Shape</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select bind:value={designState.shape}>
                  <option value="rectangle">Rectangle</option>
                  <option value="circle">Circle</option>
                  <option value="triangle">Triangle</option>
                  <option value="custom">Custom Shape</option>
                </select>
              </div>
            </div>
          </div>
          
          {#if designState.shape === 'custom'}
            <div class="notification is-info is-light mt-3">
              Draw your custom shape in the canvas. Click and drag to create your outline.
            </div>
            <button class="button is-small is-warning" on:click={resetDesign}>Reset Drawing</button>
          {/if}
        </div>
        
        <div class="column is-8">
          <div class="canvas-container" style="border: 1px solid #ddd; border-radius: 4px;">
            <svg 
              width={svgWidth} 
              height={svgHeight}
              on:mousedown={startDrawing}
              on:mousemove={continueDrawing}
              on:mouseup={endDrawing}
              on:mouseleave={endDrawing}
            >
              {#if designState.shape === 'rectangle'}
                <rect 
                  x={svgWidth/2 - designState.dimensions.width/2} 
                  y={svgHeight/2 - designState.dimensions.height/2} 
                  width={designState.dimensions.width} 
                  height={designState.dimensions.height}
                  fill="none" 
                  stroke="#333" 
                  stroke-width="2"
                />
              {:else if designState.shape === 'circle'}
                <circle 
                  cx={svgWidth/2} 
                  cy={svgHeight/2} 
                  r={Math.min(designState.dimensions.width, designState.dimensions.height)/2}
                  fill="none" 
                  stroke="#333" 
                  stroke-width="2"
                />
              {:else if designState.shape === 'triangle'}
                <polygon 
                  points={`${svgWidth/2},${svgHeight/2 - designState.dimensions.height/2} 
                          ${svgWidth/2 - designState.dimensions.width/2},${svgHeight/2 + designState.dimensions.height/2} 
                          ${svgWidth/2 + designState.dimensions.width/2},${svgHeight/2 + designState.dimensions.height/2}`}
                  fill="none" 
                  stroke="#333" 
                  stroke-width="2"
                />
              {:else if designState.shape === 'custom'}
                {#each paths as path}
                  <path d={path} fill="none" stroke="#333" stroke-width="2" />
                {/each}
                {#if isDrawing}
                  <path d={currentPath} fill="none" stroke="#333" stroke-width="2" />
                {/if}
              {/if}
            </svg>
          </div>
        </div>
      </div>
    {:else if currentStep === 2}
      <!-- Step 3: Features -->
      <h2 class="title is-4">Add Features</h2>
      <div class="columns">
        <div class="column is-4">
          <div class="box">
            <h3 class="title is-5">Feature Library</h3>
            <div class="buttons">
              {#each featureTypes as feature}
                <button 
                  class="button" 
                  on:click={() => addFeature(feature.id)}
                >
                  {feature.name}
                </button>
              {/each}
            </div>
          </div>
          
          <div class="box">
            <h3 class="title is-5">Current Features</h3>
            {#if designState.features.length === 0}
              <p class="has-text-grey">No features added yet</p>
            {:else}
              <ul>
                {#each designState.features as feature}
                  <li>
                    {feature.type} - Size: {feature.size}mm
                    <button 
                      class="button is-small is-danger is-outlined ml-2"
                      on:click={() => designState.features = designState.features.filter(f => f.id !== feature.id)}
                    >
                      Remove
                    </button>
                  </li>
                {/each}
              </ul>
            {/if}
          </div>
        </div>
        
        <div class="column is-8">
          <div class="canvas-container" style="border: 1px solid #ddd; border-radius: 4px;">
            <svg width={svgWidth} height={svgHeight}>
              <!-- Base shape -->
              {#if designState.shape === 'rectangle'}
                <rect 
                  x={svgWidth/2 - designState.dimensions.width/2} 
                  y={svgHeight/2 - designState.dimensions.height/2} 
                  width={designState.dimensions.width} 
                  height={designState.dimensions.height}
                  fill="none" 
                  stroke="#333" 
                  stroke-width="2"
                />
              {:else if designState.shape === 'circle'}
                <circle 
                  cx={svgWidth/2} 
                  cy={svgHeight/2} 
                  r={Math.min(designState.dimensions.width, designState.dimensions.height)/2}
                  fill="none" 
                  stroke="#333" 
                  stroke-width="2"
                />
              {:else if designState.shape === 'triangle'}
                <polygon 
                  points={`${svgWidth/2},${svgHeight/2 - designState.dimensions.height/2} 
                          ${svgWidth/2 - designState.dimensions.width/2},${svgHeight/2 + designState.dimensions.height/2} 
                          ${svgWidth/2 + designState.dimensions.width/2},${svgHeight/2 + designState.dimensions.height/2}`}
                  fill="none" 
                  stroke="#333" 
                  stroke-width="2"
                />
              {:else if designState.shape === 'custom'}
                {#each paths as path}
                  <path d={path} fill="none" stroke="#333" stroke-width="2" />
                {/each}
              {/if}
              
              <!-- Features -->
              {#each designState.features as feature}
                {#if feature.type === 'hole'}
                  <circle 
                    cx={feature.x} 
                    cy={feature.y} 
                    r={feature.size/2}
                    fill="#fff" 
                    stroke="#444" 
                    stroke-width="1"
                    stroke-dasharray="3,3"
                  />
                {:else if feature.type === 'slot'}
                  <rect 
                    x={feature.x - feature.size} 
                    y={feature.y - feature.size/4} 
                    width={feature.size * 2} 
                    height={feature.size/2}
                    fill="#fff" 
                    stroke="#444" 
                    stroke-width="1"
                    stroke-dasharray="3,3"
                  />
                {:else if feature.type === 'cutout'}
                  <path 
                    d={`M${feature.x-feature.size},${feature.y-feature.size} L${feature.x+feature.size},${feature.y-feature.size} L${feature.x+feature.size},${feature.y+feature.size} L${feature.x-feature.size},${feature.y+feature.size} Z`}
                    fill="#fff" 
                    stroke="#444" 
                    stroke-width="1"
                    stroke-dasharray="5,5"
                  />
                {:else if feature.type === 'bend'}
                  <line 
                    x1={feature.x - feature.size} 
                    y1={feature.y} 
                    x2={feature.x + feature.size} 
                    y2={feature.y}
                    stroke="#f00" 
                    stroke-width="2"
                    stroke-dasharray="5,5"
                  />
                {/if}
              {/each}
            </svg>
          </div>
        </div>
      </div>
    {:else if currentStep === 3}
      <!-- Step 4: Material -->
      <h2 class="title is-4">Material Selection</h2>
      <div class="columns">
        <div class="column is-6">
          <div class="field">
            <label class="label">Material Type</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select bind:value={designState.material.type}>
                  {#each materialOptions as option}
                    <option value={option.id}>{option.name}</option>
                  {/each}
                </select>
              </div>
            </div>
          </div>
          
          <div class="field">
            <label class="label">Thickness (mm)</label>
            <div class="control">
              <input 
                class="input" 
                type="number" 
                bind:value={designState.material.thickness}
                min={materialOptions.find(m => m.id === designState.material.type).minThickness}
                max={materialOptions.find(m => m.id === designState.material.type).maxThickness}
                step="0.5"
              >
            </div>
            <p class="help">
              Range: {materialOptions.find(m => m.id === designState.material.type).minThickness} - 
              {materialOptions.find(m => m.id === designState.material.type).maxThickness}mm
            </p>
          </div>
          
          <div class="field">
            <label class="label">Surface Finish</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select bind:value={designState.material.finish}>
                  <option value="none">None (Raw)</option>
                  <option value="polished">Polished</option>
                  <option value="brushed">Brushed</option>
                  <option value="painted">Painted</option>
                  <option value="powder-coated">Powder Coated</option>
                </select>
              </div>
            </div>
          </div>
        </div>
        
        <div class="column is-6">
          <div class="notification is-info is-light">
            <h3 class="title is-5">Material Information</h3>
            <p>Selected material: <strong>{materialOptions.find(m => m.id === designState.material.type).name}</strong></p>
            <p>Thickness: <strong>{designState.material.thickness}mm</strong></p>
            <p>Finish: <strong>{designState.material.finish === 'none' ? 'Raw (No finish)' : designState.material.finish}</strong></p>
          </div>
          
          <div class="field">
            <label class="label">Additional Notes</label>
            <div class="control">
              <textarea 
                class="textarea" 
                placeholder="Add any special instructions or requirements"
                bind:value={designState.notes}
              ></textarea>
            </div>
          </div>
        </div>
      </div>
    {:else if currentStep === 4}
      <!-- Step 5: Review -->
      <h2 class="title is-4">Review Your Design</h2>
      <div class="columns">
        <div class="column is-6">
          <div class="box">
            <h3 class="title is-5">Design Summary</h3>
            <table class="table is-fullwidth">
              <tbody>
                <tr>
                  <th>Dimensions</th>
                  <td>{designState.dimensions.width}mm × {designState.dimensions.height}mm × {designState.dimensions.depth}mm</td>
                </tr>
                <tr>
                  <th>Shape</th>
                  <td>{designState.shape}</td>
                </tr>
                <tr>
                  <th>Features</th>
                  <td>{designState.features.length} feature(s)</td>
                </tr>
                <tr>
                  <th>Material</th>
                  <td>{materialOptions.find(m => m.id === designState.material.type).name}, {designState.material.thickness}mm</td>
                </tr>
                <tr>
                  <th>Finish</th>
                  <td>{designState.material.finish === 'none' ? 'Raw (No finish)' : designState.material.finish}</td>
                </tr>
                {#if designState.notes}
                  <tr>
                    <th>Notes</th>
                    <td>{designState.notes}</td>
                  </tr>
                {/if}
              </tbody>
            </table>
          </div>
        </div>
        
        <div class="column is-6">
          <div class="canvas-container box" style="padding: 0;">
            <svg width={svgWidth} height={svgHeight}>
              <!-- Base shape -->
              {#if designState.shape === 'rectangle'}
                <rect 
                  x={svgWidth/2 - designState.dimensions.width/2} 
                  y={svgHeight/2 - designState.dimensions.height/2} 
                  width={designState.dimensions.width} 
                  height={designState.dimensions.height}
                  fill="none" 
                  stroke="#333" 
                  stroke-width="2"
                />
              {:else if designState.shape === 'circle'}
                <circle 
                  cx={svgWidth/2} 
                  cy={svgHeight/2} 
                  r={Math.min(designState.dimensions.width, designState.dimensions.height)/2}
                  fill="none" 
                  stroke="#333" 
                  stroke-width="2"
                />
              {:else if designState.shape === 'triangle'}
                <polygon 
                  points={`${svgWidth/2},${svgHeight/2 - designState.dimensions.height/2} 
                          ${svgWidth/2 - designState.dimensions.width/2},${svgHeight/2 + designState.dimensions.height/2} 
                          ${svgWidth/2 + designState.dimensions.width/2},${svgHeight/2 + designState.dimensions.height/2}`}
                  fill="none" 
                  stroke="#333" 
                  stroke-width="2"
                />
              {:else if designState.shape === 'custom'}
                {#each paths as path}
                  <path d={path} fill="none" stroke="#333" stroke-width="2" />
                {/each}
              {/if}
              
              <!-- Features -->
              {#each designState.features as feature}
                {#if feature.type === 'hole'}
                  <circle 
                    cx={feature.x} 
                    cy={feature.y} 
                    r={feature.size/2}
                    fill="#fff" 
                    stroke="#444" 
                    stroke-width="1"
                    stroke-dasharray="3,3"
                  />
                {:else if feature.type === 'slot'}
                  <rect 
                    x={feature.x - feature.size} 
                    y={feature.y - feature.size/4} 
                    width={feature.size * 2} 
                    height={feature.size/2}
                    fill="#fff" 
                    stroke="#444" 
                    stroke-width="1"
                    stroke-dasharray="3,3"
                  />
                {:else if feature.type === 'cutout'}
                  <path 
                    d={`M${feature.x-feature.size},${feature.y-feature.size} L${feature.x+feature.size},${feature.y-feature.size} L${feature.x+feature.size},${feature.y+feature.size} L${feature.x-feature.size},${feature.y+feature.size} Z`}
                    fill="#fff" 
                    stroke="#444" 
                    stroke-width="1"
                    stroke-dasharray="5,5"
                  />
                {:else if feature.type === 'bend'}
                  <line 
                    x1={feature.x - feature.size} 
                    y1={feature.y} 
                    x2={feature.x + feature.size} 
                    y2={feature.y}
                    stroke="#f00" 
                    stroke-width="2"
                    stroke-dasharray="5,5"
                  />
                {/if}
              {/each}
            </svg>
          </div>
          
          <div class="notification is-warning is-light mt-3">
            <p>After submission, our team will review your design and provide pricing information. You will receive a response within 1-2 business days.</p>
          </div>
        </div>
      </div>
      
      <div class="field">
        <div class="control">
          <button class="button is-success is-large" on:click={submitDesign}>
            Submit Design for Pricing
          </button>
        </div>
      </div>
    {/if}
    
    <!-- Navigation buttons -->
    <div class="buttons mt-5">
      {#if currentStep > 0}
        <button class="button" on:click={prevStep}>Previous</button>
      {/if}
      
      {#if currentStep < steps.length - 1}
        <button class="button is-primary" on:click={nextStep}>Next</button>
      {/if}
    </div>
  </div>
</div>

<style>
  /* Styling for steps indicator */
  .steps {
    display: flex;
    width: 100%;
    margin-bottom: 1rem;
    position: relative;
  }
  
  .steps::before {
    content: '';
    position: absolute;
    top: 1.5rem;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: #dbdbdb;
    z-index: 0;
  }
  
  .steps-segment {
    position: relative;
    flex-grow: 1;
    flex-basis: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .steps-marker {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 3rem;
    height: 3rem;
    border-radius: 50%;
    background-color: #dbdbdb;
    color: white;
    font-weight: bold;
    z-index: 1;
    margin-bottom: 0.5rem;
  }
  
  .steps-segment.is-active .steps-marker {
    background-color: #3273dc;
  }
  
  .steps-content {
    text-align: center;
    max-width: 140px;
  }
  
  /* Canvas container */
  .canvas-container {
    background-color: #f5f5f5;
    overflow: hidden;
  }
  
  /* Override Bulma spacing */
  .mt-3 {
    margin-top: 0.75rem !important;
  }
  
  .mt-5 {
    margin-top: 1.5rem !important;
  }
  
  .mb-5 {
    margin-bottom: 1.5rem !important;
  }
  
  .ml-2 {
    margin-left: 0.5rem !important;
  }
</style>