// src/routes/designer/steps/ReviewStep.svelte
<script>
  import { createEventDispatcher } from 'svelte';
  
  export let design;
  
  const dispatch = createEventDispatcher();
  
  // Materials reference data
  const materials = {
    'steel': { 
      name: 'Steel', 
      density: 7.85, // g/cm³
      color: '#708090'
    },
    'aluminum': { 
      name: 'Aluminum', 
      density: 2.7,
      color: '#E8E8E8'
    },
    'copper': { 
      name: 'Copper', 
      density: 8.96,
      color: '#B87333'
    },
    'brass': { 
      name: 'Brass', 
      density: 8.4,
      color: '#D4AF37'
    }
  };
  
  // Finishes reference data
  const finishes = {
    'none': { name: 'No Finish' },
    'painted': { name: 'Painted' },
    'powder-coated': { name: 'Powder Coated' },
    'galvanized': { name: 'Galvanized' },
    'anodized': { name: 'Anodized' },
    'brushed': { name: 'Brushed' },
    'polished': { name: 'Polished' }
  };
  
  // Part types reference data
  const partTypes = {
    'rectangle': { name: 'Rectangle' },
    'lShape': { name: 'L-Shape' },
    'uShape': { name: 'U-Shape' },
    'circle': { name: 'Circle' }
  };
  
  // Helper function to get dimension value or default
  function getDimension(name, defaultValue = 0) {
    return design.dimensions && design.dimensions[name] !== undefined 
      ? design.dimensions[name] 
      : defaultValue;
  }
  
  // Format dimensions for display
  function formatDimensions() {
    switch (design.partType) {
      case 'rectangle':
        return `${getDimension('width')} × ${getDimension('height')} × ${design.thickness} mm`;
      case 'lShape':
        return `${getDimension('width')} × ${getDimension('height')} × ${design.thickness} mm, Leg Width: ${getDimension('legWidth')} mm`;
      case 'uShape':
        return `${getDimension('width')} × ${getDimension('height')} × ${design.thickness} mm, Leg Width: ${getDimension('legWidth')} mm, Flange Height: ${getDimension('flangeHeight')} mm`;
      case 'circle':
        return `Ø${getDimension('diameter')} × ${design.thickness} mm`;
      default:
        return 'N/A';
    }
  }
  
  // Import the metal API service to get accurate estimates
  import metalApiService from '$lib/services/metalApiService.js';
  
  // State for cost estimate
  let estimatedCost = 0;
  let estimatedProductionDays = 0;
  let isCalculating = false;
  
  // Request cost and production time estimates from the API
  async function requestEstimates() {
    try {
      isCalculating = true;
      
      // In a full implementation, this would call an actual endpoint
      // For now, we'll simulate with a timeout
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Calculate estimated price based on material, dimensions, and features
      estimatedCost = calculateEstimatedCost();
      
      // Calculate production time
      estimatedProductionDays = calculateEstimatedProductionTime();
      
      isCalculating = false;
    } catch (error) {
      console.error('Error fetching estimates:', error);
      isCalculating = false;
    }
  }
  
  // Request estimates when the component mounts
  onMount(() => {
    requestEstimates();
  });
  
  // Recalculate when design changes
  $: if (design) {
    requestEstimates();
  }
  
  // Estimate cost based on the design
  function calculateEstimatedCost() {
    // This is a simplified version - in production this would come from the API
    if (!design.dimensions || !design.material) return 0;
    
    // Base material costs per cm³
    const materialCosts = {
      'steel': 0.08,
      'aluminum': 0.12,
      'copper': 0.25,
      'brass': 0.20
    };
    
    // Calculate the volume and weight
    const volume = calculateVolume();
    const weight = calculateWeight();
    
    // Base cost based on material and volume
    let cost = volume * materialCosts[design.material];
    
    // Add cost for each hole
    const holeCost = (design.holes?.length || 0) * 1.5;
    
    // Add finish cost
    let finishCost = 0;
    switch(design.finish) {
      case 'painted':
      case 'powder-coated':
        finishCost = cost * 0.2;
        break;
      case 'anodized':
        finishCost = cost * 0.4;
        break;
      case 'galvanized':
        finishCost = cost * 0.25;
        break;
      case 'brushed':
      case 'polished':
        finishCost = cost * 0.15;
        break;
    }
    
    // Add fixed costs and minimum price
    const totalCost = Math.max(20, cost + holeCost + finishCost + 15);
    
    return Math.round(totalCost * 100) / 100;
  }
  
  // Estimate production time
  function calculateEstimatedProductionTime() {
    // Base time depends on complexity
    let baseTime = 1; // days
    
    // Add time for complex shapes
    if (design.partType === 'lShape') {
      baseTime += 0.5;
    } else if (design.partType === 'uShape') {
      baseTime += 1;
    }
    
    // Add time for holes
    if (design.holes && design.holes.length > 0) {
      baseTime += Math.min(design.holes.length * 0.2, 2);
    }
    
    // Add time for finishing
    if (design.finish !== 'none') {
      baseTime += 0.5;
    }
    
    return Math.ceil(baseTime * 2) / 2; // Round to nearest half day
  }
  
  // Calculate volume in cm³
  function calculateVolume() {
    if (!design.dimensions) return 0;
    
    const thicknessInCm = design.thickness / 10;
    let volume = 0; // in cm³
    
    // Rest of volume calculation
    switch (design.partType) {
      // ...
    }
    
    return volume;
  }
  
  // Calculate estimated weight
  function calculateWeight() {
    if (!design.dimensions || !design.material) return 0;
    
    const material = materials[design.material];
    if (!material) return 0;
    
    const density = material.density; // g/cm³
    const thicknessInCm = design.thickness / 10;
    let volume = 0; // in cm³
    
    switch (design.partType) {
      case 'rectangle': {
        const width = getDimension('width') / 10; // mm to cm
        const height = getDimension('height') / 10; // mm to cm
        volume = width * height * thicknessInCm;
        break;
      }
      case 'lShape': {
        const width = getDimension('width') / 10;
        const height = getDimension('height') / 10;
        const legWidth = getDimension('legWidth') / 10;
        
        // L-shape area = full rectangle - missing rectangle
        const area = (width * height) - ((width - legWidth) * (height - legWidth));
        volume = area * thicknessInCm;
        break;
      }
      case 'uShape': {
        const width = getDimension('width') / 10;
        const height = getDimension('height') / 10;
        const legWidth = getDimension('legWidth') / 10;
        const flangeHeight = getDimension('flangeHeight') / 10;
        
        // U-shape has two vertical legs and a horizontal connection
        const leftLeg = legWidth * height;
        const rightLeg = legWidth * height;
        const bottom = (width - (2 * legWidth)) * flangeHeight;
        
        volume = (leftLeg + rightLeg + bottom) * thicknessInCm;
        break;
      }
      case 'circle': {
        const radius = getDimension('diameter') / 20; // diameter/2 in cm
        volume = Math.PI * radius * radius * thicknessInCm;
        break;
      }
      default:
        return 0;
    }
    
    // Subtract volume of holes
    if (design.holes && design.holes.length > 0) {
      design.holes.forEach(hole => {
        const holeRadius = hole.diameter / 20; // diameter/2 in cm
        const holeVolume = Math.PI * holeRadius * holeRadius * thicknessInCm;
        volume -= holeVolume;
      });
    }
    
    // Calculate weight in grams
    return volume * density;
  }
  
  // Format weight for display
  function formatWeight() {
    const weight = calculateWeight();
    
    if (weight < 1000) {
      return `${weight.toFixed(1)} g`;
    } else {
      return `${(weight / 1000).toFixed(2)} kg`;
    }
  }
  
  // Calculate SVG viewBox dimensions
  function getViewBoxDimensions() {
    const padding = 40;
    
    switch (design.partType) {
      case 'rectangle': {
        const width = getDimension('width', 200);
        const height = getDimension('height', 100);
        return `0 0 ${width + padding} ${height + padding}`;
      }
      case 'lShape': {
        const width = getDimension('width', 200);
        const height = getDimension('height', 100);
        return `0 0 ${width + padding} ${height + padding}`;
      }
      case 'uShape': {
        const width = getDimension('width', 200);
        const height = getDimension('height', 100);
        return `0 0 ${width + padding} ${height + padding}`;
      }
      case 'circle': {
        const diameter = getDimension('diameter', 100);
        return `0 0 ${diameter + padding} ${diameter + padding}`;
      }
      default:
        return "0 0 300 200";
    }
  }
  
  // Generate SVG path for the part
  function getPartPath() {
    const padding = 20; // Half of the viewBox padding
    
    switch (design.partType) {
      case 'rectangle': {
        const width = getDimension('width', 200);
        const height = getDimension('height', 100);
        return `M ${padding} ${padding} h ${width} v ${height} h -${width} z`;
      }
      case 'lShape': {
        const width = getDimension('width', 200);
        const height = getDimension('height', 100);
        const legWidth = getDimension('legWidth', 50);
        return `M ${padding} ${padding} h ${width} v ${legWidth} h -${width - legWidth} v ${height - legWidth} h -${legWidth} z`;
      }
      case 'uShape': {
        const width = getDimension('width', 200);
        const height = getDimension('height', 100);
        const legWidth = getDimension('legWidth', 50);
        const flangeHeight = getDimension('flangeHeight', 30);
        return `M ${padding} ${padding} h ${legWidth} v ${height - flangeHeight} h ${width - 2 * legWidth} v -${height - flangeHeight} h ${legWidth} v ${height} h -${width} z`;
      }
      case 'circle': {
        const radius = getDimension('diameter', 100) / 2;
        const cx = radius + padding;
        const cy = radius + padding;
        return `M ${cx + radius} ${cy} a ${radius} ${radius} 0 1 0 -${radius * 2} 0 a ${radius} ${radius} 0 1 0 ${radius * 2} 0`;
      }
      default:
        return "";
    }
  }
  
  // Generate side view path
  function getSideViewPath() {
    const padding = 20;
    const halfHeight = 50; // Half height of the SVG view for side view
    const thickness = design.thickness;
    
    switch (design.partType) {
      case 'rectangle': {
        const width = getDimension('width', 200);
        return `M ${padding} ${halfHeight} h ${width} v ${thickness} h -${width} z`;
      }
      case 'lShape': {
        const width = getDimension('width', 200);
        const legWidth = getDimension('legWidth', 50);
        
        // Side view of L-shape depends on orientation
        return `M ${padding} ${halfHeight} h ${width} v ${thickness} h -${width} z`;
      }
      case 'uShape': {
        const width = getDimension('width', 200);
        const legWidth = getDimension('legWidth', 50);
        const flangeHeight = getDimension('flangeHeight', 30);
        
        // U-shape side view (simplified)
        return `
          M ${padding} ${halfHeight} 
          v ${-flangeHeight} h ${thickness} v ${flangeHeight}
          h ${width - 2 * thickness} 
          v ${-flangeHeight} h ${thickness} v ${flangeHeight}
          z
        `;
      }
      case 'circle': {
        const diameter = getDimension('diameter', 100);
        return `M ${padding} ${halfHeight} h ${diameter} v ${thickness} h -${diameter} z`;
      }
      default:
        return "";
    }
  }
  
  // Get fill color based on material and finish
  function getFillColor() {
    if ((design.finish === 'painted' || design.finish === 'powder-coated') && design.finishColor) {
      return design.finishColor;
    }
    
    return materials[design.material]?.color || '#CCC';
  }
  
  // Active view (top or side)
  let activeView = 'top';
</script>

<div class="columns">
  <div class="column is-6">
    <div class="box">
      <h3 class="title is-5">Design Summary</h3>
      
      <table class="table is-fullwidth">
        <tbody>
          <tr>
            <th>Part Type</th>
            <td>{partTypes[design.partType]?.name || design.partType}</td>
          </tr>
          <tr>
            <th>Dimensions</th>
            <td>{formatDimensions()}</td>
          </tr>
          <tr>
            <th>Material</th>
            <td>{materials[design.material]?.name || design.material}</td>
          </tr>
          <tr>
            <th>Finish</th>
            <td>
              {finishes[design.finish]?.name || design.finish}
              {#if design.finish === 'painted' || design.finish === 'powder-coated'}
                <div class="is-flex is-align-items-center mt-1">
                  <div 
                    class="color-swatch mr-2"
                    style="background-color: {design.finishColor};"
                  ></div>
                  <span class="is-size-7">{design.finishColor}</span>
                </div>
              {/if}
            </td>
          </tr>
          <tr>
            <th>Holes</th>
            <td>{design.holes.length} {design.holes.length === 1 ? 'hole' : 'holes'}</td>
          </tr>
          <tr>
            <th>Estimated Weight</th>
            <td>{formatWeight()}</td>
          </tr>
          <tr>
            <th>Design ID</th>
            <td><code class="is-family-code is-size-7">{design.id}</code></td>
          </tr>
        </tbody>
      </table>
      
      <div class="field is-grouped is-grouped-centered mt-4">
        <div class="control">
          <button class="button is-info" on:click={() => window.print()}>
            <span class="icon">
              <i class="fas fa-print"></i>
            </span>
            <span>Print Overview</span>
          </button>
        </div>
        <div class="control">
          <button class="button is-info is-light">
            <span class="icon">
              <i class="fas fa-file-pdf"></i>
            </span>
            <span>Download Drawing</span>
          </button>
        </div>
      </div>
    </div>
    
    {#if design.holes.length > 0}
      <div class="box mt-4">
        <h3 class="title is-5">Holes Specification</h3>
        
        <table class="table is-fullwidth is-striped is-narrow">
          <thead>
            <tr>
              <th>#</th>
              <th>X Position</th>
              <th>Y Position</th>
              <th>Diameter</th>
            </tr>
          </thead>
          <tbody>
            {#each design.holes as hole, index}
              <tr>
                <td>{index + 1}</td>
                <td>{hole.x} mm</td>
                <td>{hole.y} mm</td>
                <td>Ø{hole.diameter} mm</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}
    
    <div class="notification is-info is-light mt-4">
      <p class="has-text-weight-bold">Next Steps:</p>
      <p>Review your design details above. If everything looks correct, click the "Submit Design" button to request a quote. Our team will review your specifications and get back to you shortly.</p>
      <p class="mt-2">You can also save this design as a JSON file for future modifications.</p>
    </div>
  </div>
  
  <div class="column is-6">
    <div class="box">
      <h3 class="title is-5">Technical Drawing</h3>
      
      <div class="tabs is-boxed">
        <ul>
          <li class={activeView === 'top' ? 'is-active' : ''}>
            <a on:click={() => activeView = 'top'}>Top View</a>
          </li>
          <li class={activeView === 'side' ? 'is-active' : ''}>
            <a on:click={() => activeView = 'side'}>Side View</a>
          </li>
        </ul>
      </div>
      
      <div class="preview-container">
        {#if activeView === 'top'}
          <svg width="100%" height="300" viewBox={getViewBoxDimensions()}>
            <!-- Main shape -->
            <path d={getPartPath()} fill={getFillColor()} stroke="#333" stroke-width="2" />
            
            <!-- Holes -->
            {#each design.holes as hole}
              <circle 
                cx={hole.x + 20} 
                cy={hole.y + 20} 
                r={hole.diameter / 2}
                fill="white"
                stroke="#333"
                stroke-width="1.5"
              />
              
              <!-- Hole ID label -->
              <text 
                x={hole.x + 20} 
                y={hole.y + 20 + 3} 
                text-anchor="middle" 
                font-size="8" 
                fill="#333"
                font-weight="bold"
              >
                {design.holes.indexOf(hole) + 1}
              </text>
            {/each}
            
            <!-- Dimensions - Width -->
            {#if design.partType !== 'circle'}
              <g class="dimension-line">
                <line 
                  x1="20" 
                  y1="10" 
                  x2={20 + getDimension('width', 200)} 
                  y2="10" 
                  stroke="#666" 
                  stroke-width="1" 
                  stroke-dasharray="4,2"
                />
                <line x1="20" y1="8" x2="20" y2="12" stroke="#666" stroke-width="1" />
                <line 
                  x1={20 + getDimension('width', 200)} 
                  y1="8" 
                  x2={20 + getDimension('width', 200)} 
                  y2="12" 
                  stroke="#666" 
                  stroke-width="1" 
                />
                <text 
                  x={20 + getDimension('width', 200)/2} 
                  y="16" 
                  text-anchor="middle" 
                  font-size="10" 
                  fill="#666"
                >
                  {getDimension('width', 200)} mm
                </text>
              </g>
              
              <!-- Dimensions - Height -->
              <g class="dimension-line">
                <line 
                  x1="10" 
                  y1="20" 
                  x2="10" 
                  y2={20 + getDimension('height', 100)} 
                  stroke="#666" 
                  stroke-width="1" 
                  stroke-dasharray="4,2"
                />
                <line x1="8" y1="20" x2="12" y2="20" stroke="#666" stroke-width="1" />
                <line 
                  x1="8" 
                  y1={20 + getDimension('height', 100)} 
                  x2="12" 
                  y2={20 + getDimension('height', 100)} 
                  stroke="#666" 
                  stroke-width="1" 
                />
                <text 
                  x="6" 
                  y={20 + getDimension('height', 100)/2} 
                  text-anchor="middle" 
                  font-size="10" 
                  fill="#666"
                  transform={`rotate(270, 6, ${20 + getDimension('height', 100)/2})`}
                >
                  {getDimension('height', 100)} mm
                </text>
              </g>
            {:else}
              <!-- Dimensions for Circle (Diameter) -->
              <g class="dimension-line">
                <line 
                  x1={20} 
                  y1={20 + getDimension('diameter', 100)/2} 
                  x2={20 + getDimension('diameter', 100)} 
                  y2={20 + getDimension('diameter', 100)/2} 
                  stroke="#666" 
                  stroke-width="1" 
                  stroke-dasharray="4,2"
                />
                <text 
                  x={20 + getDimension('diameter', 100)/2} 
                  y={20 + getDimension('diameter', 100)/2 + 16} 
                  text-anchor="middle" 
                  font-size="10" 
                  fill="#666"
                >
                  Ø {getDimension('diameter', 100)} mm
                </text>
              </g>
            {/if}
            
            <!-- Drawing Information -->
            <g transform="translate(20, 20)" opacity="0.7">
              <text x="0" y="-10" font-size="10" fill="#666">TC Pliage</text>
            </g>
          </svg>
        {:else}
          <!-- Side View -->
          <svg width="100%" height="150" viewBox="0 0 280 100">
            <path d={getSideViewPath()} fill={getFillColor()} stroke="#333" stroke-width="2" />
            
            <!-- Thickness dimension -->
            <line 
              x1={280 - 40} 
              y1={50} 
              x2={280 - 40} 
              y2={50 + design.thickness} 
              stroke="#666" 
              stroke-width="1" 
              stroke-dasharray="4,2"
            />
            <line 
              x1={280 - 45} 
              y1={50} 
              x2={280 - 35} 
              y2={50} 
              stroke="#666" 
              stroke-width="1"
            />
            <line 
              x1={280 - 45} 
              y1={50 + design.thickness} 
              x2={280 - 35} 
              y2={50 + design.thickness} 
              stroke="#666" 
              stroke-width="1"
            />
            <text 
              x={280 - 30} 
              y={50 + design.thickness/2 + 3} 
              text-anchor="start" 
              font-size="10" 
              fill="#666"
            >
              {design.thickness} mm
            </text>
          </svg>
        {/if}
      </div>
    </div>
    
    <div class="box mt-4">
      <h3 class="title is-5">Order Information</h3>
      
      <div class="columns">
        <div class="column is-6">
          <div class="field">
            <label class="label">Special Instructions (Optional)</label>
            <div class="control">
              <textarea class="textarea" placeholder="Add any special requirements or notes for our fabrication team"></textarea>
            </div>
          </div>
          
          <div class="field">
            <label class="label">Quantity</label>
            <div class="control">
              <input class="input" type="number" min="1" value="1" id="quantity">
            </div>
          </div>
          
          <div class="field">
            <label class="label">Urgency</label>
            <div class="control">
              <label class="radio">
                <input type="radio" name="urgency" value="standard" checked>
                Standard ({estimatedProductionDays} business days)
              </label>
              <label class="radio">
                <input type="radio" name="urgency" value="expedited">
                Expedited (1-2 business days, +30% surcharge)
              </label>
              <label class="radio">
                <input type="radio" name="urgency" value="urgent">
                Urgent (24 hours, +50% surcharge)
              </label>
            </div>
          </div>
        </div>
        
        <div class="column is-6">
          <div class="price-summary box has-background-light">
            <h4 class="title is-6">Price Summary</h4>
            
            {#if isCalculating}
              <div class="has-text-centered p-4">
                <p>Calculating price...</p>
                <progress class="progress is-small is-primary mt-2"></progress>
              </div>
            {:else}
              <table class="table is-fullwidth">
                <tbody>
                  <tr>
                    <td>Base price (1 item)</td>
                    <td class="has-text-right">€{estimatedCost.toFixed(2)}</td>
                  </tr>
                  <tr>
                    <td>Shipping</td>
                    <td class="has-text-right">€10.00</td>
                  </tr>
                  <tr>
                    <td>
                      <strong>Total</strong>
                      <span class="is-size-7 has-text-grey">VAT included</span>
                    </td>
                    <td class="has-text-right has-text-weight-bold">
                      €{(estimatedCost + 10).toFixed(2)}
                    </td>
                  </tr>
                </tbody>
              </table>
              
              <div class="notification is-info is-light mt-3 is-size-7 mb-0">
                <p><strong>Estimated delivery:</strong> {new Date(Date.now() + estimatedProductionDays * 86400000).toLocaleDateString('fr-FR')}</p>
              </div>
            {/if}
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .preview-container {
    border: 1px solid #eee;
    border-radius: 4px;
    background-color: #f8f8f8;
    padding: 10px;
    min-height: 250px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .dimension-line {
    opacity: 0.8;
  }
  
  .color-swatch {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 1px solid #ddd;
  }
  
  @media print {
    body * {
      visibility: hidden;
    }
    .box, .box * {
      visibility: visible;
    }
    .box {
      position: absolute;
      left: 0;
      top: 0;
      width: 100%;
    }
  }
</style>