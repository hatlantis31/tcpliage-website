<!-- DesignSummary.svelte -->
<script>
  export let design;
  
  // Pricing constants (would normally come from backend)
  const MATERIAL_PRICES = {
    steel: 3.5,     // €/kg
    aluminum: 5.2,  // €/kg
    copper: 8.75,   // €/kg
    brass: 7.3      // €/kg
  };
  
  const MATERIAL_DENSITIES = {
    steel: 7.85,    // g/cm³
    aluminum: 2.7,  // g/cm³
    copper: 8.96,   // g/cm³
    brass: 8.4      // g/cm³
  };
  
  const COATING_FACTORS = {
    none: 1.0,
    painted: 1.2,
    'powder-coated': 1.5,
    anodized: 1.8,
    galvanized: 1.3
  };
  
  // Cutout pricing
  const BASE_CUTOUT_PRICE = 5; // € per cutout
  const CUTOUT_SIZE_FACTOR = 0.05; // € per mm of size
  
  // Helper to format the shape description
  function getShapeDescription(shape) {
    if (!shape) return 'No shape selected';
    
    let description = `${shape.name}`;
    
    if (shape.dimensions) {
      if (shape.id === 'circle') {
        description += ` (${shape.dimensions.diameter}mm diameter, ${shape.dimensions.thickness}mm thick)`;
      } else {
        description += ` (${shape.dimensions.width}mm × ${shape.dimensions.height}mm, ${shape.dimensions.thickness}mm thick)`;
      }
    }
    
    return description;
  }
  
  // Helper to format the coating description
  function getCoatingDescription(coating) {
    if (!coating) return 'No coating selected';
    
    let description = `${coating.name}`;
    
    if (coating.color) {
      description += ` - ${coating.color.name} color`;
    }
    
    return description;
  }
  
  // Calculate base price based on material volume and weight
  function calculateBaseMaterialPrice() {
    if (!design.material || !design.shape) return 0;
    
    const materialId = design.material.id;
    const density = MATERIAL_DENSITIES[materialId] || 1;
    const pricePerKg = MATERIAL_PRICES[materialId] || 1;
    
    // Calculate volume in cm³
    let volume;
    
    if (design.shape.id === 'circle') {
      const radius = design.shape.dimensions.diameter / 2 / 10; // mm to cm
      const thickness = design.shape.dimensions.thickness / 10; // mm to cm
      volume = Math.PI * radius * radius * thickness;
    } else if (design.shape.id === 'rectangle') {
      const width = design.shape.dimensions.width / 10; // mm to cm
      const height = design.shape.dimensions.height / 10; // mm to cm
      const thickness = design.shape.dimensions.thickness / 10; // mm to cm
      volume = width * height * thickness;
    } else if (design.shape.id === 'triangle') {
      const width = design.shape.dimensions.width / 10; // mm to cm
      const height = design.shape.dimensions.height / 10; // mm to cm
      const thickness = design.shape.dimensions.thickness / 10; // mm to cm
      // Area of triangle = 1/2 * base * height
      volume = 0.5 * width * height * thickness;
    } else if (design.shape.id === 'L-shape') {
      const width = design.shape.dimensions.width / 10; // mm to cm
      const height = design.shape.dimensions.height / 10; // mm to cm
      const thickness = design.shape.dimensions.thickness / 10; // mm to cm
      // Simplified L-shape as rectangle minus smaller rectangle
      const smallWidth = width * 0.4;
      const smallHeight = height * 0.4;
      volume = (width * height - smallWidth * smallHeight) * thickness;
    }
    
    // Calculate weight in kg
    const weight = volume * density / 1000;
    
    // Calculate price
    return weight * pricePerKg;
  }
  
  // Calculate price for cutouts
  function calculateCutoutsPrice() {
    if (!design.cutouts || !design.cutouts.length) return 0;
    
    return design.cutouts.reduce((total, cutout) => {
      // Base price per cutout plus size-dependent component
      return total + BASE_CUTOUT_PRICE + (cutout.size * CUTOUT_SIZE_FACTOR);
    }, 0);
  }
  
  // Calculate coating price
  function calculateCoatingPrice(basePrice) {
    if (!design.coating) return 0;
    
    const factor = COATING_FACTORS[design.coating.id] || 1;
    return basePrice * (factor - 1); // Only the additional cost
  }
  
  // Calculate the total price
  function calculateTotalPrice() {
    const basePrice = calculateBaseMaterialPrice();
    const cutoutsPrice = calculateCutoutsPrice();
    const coatingPrice = calculateCoatingPrice(basePrice);
    
    return basePrice + cutoutsPrice + coatingPrice;
  }
  
  $: baseMaterialPrice = calculateBaseMaterialPrice();
  $: cutoutsPrice = calculateCutoutsPrice();
  $: coatingPrice = calculateCoatingPrice(baseMaterialPrice);
  $: totalPrice = calculateTotalPrice();
</script>

<div>
  <h2 class="title is-4">Design Summary</h2>
  <p class="subtitle is-6 mb-4">Review your custom metal piece design</p>
  
  <div class="box">
    <table class="table is-fullwidth">
      <tbody>
        <tr>
          <th>Material</th>
          <td>{design.material ? design.material.name : 'Not selected'}</td>
        </tr>
        <tr>
          <th>Shape</th>
          <td>{design.shape ? getShapeDescription(design.shape) : 'Not selected'}</td>
        </tr>
        <tr>
          <th>Cutouts</th>
          <td>{design.cutouts?.length || 0} custom cutouts</td>
        </tr>
        <tr>
          <th>Coating</th>
          <td>{design.coating ? getCoatingDescription(design.coating) : 'Not selected'}</td>
        </tr>
      </tbody>
    </table>
  </div>
  
  <div class="box mt-4">
    <h3 class="title is-5">Design Preview</h3>
    
    <div class="has-text-centered">
      <!-- Simple preview rendering -->
      <svg width="300" height="200" viewBox="0 0 300 200">
        {#if design.shape}
          <!-- Base shape -->
          {#if design.shape.id === 'rectangle'}
            <rect 
              x="50" 
              y="50" 
              width="200" 
              height="100" 
              fill={design.coating?.color?.hex || '#CCC'} 
              stroke="#333"
              stroke-width="2"
            />
          {:else if design.shape.id === 'circle'}
            <circle 
              cx="150" 
              cy="100" 
              r="75" 
              fill={design.coating?.color?.hex || '#CCC'} 
              stroke="#333"
              stroke-width="2"
            />
          {:else if design.shape.id === 'triangle'}
            <polygon 
              points="150,25 250,175 50,175" 
              fill={design.coating?.color?.hex || '#CCC'} 
              stroke="#333"
              stroke-width="2"
            />
          {:else if design.shape.id === 'L-shape'}
            <path 
              d="M50,50 L150,50 L150,100 L200,100 L200,175 L50,175 Z" 
              fill={design.coating?.color?.hex || '#CCC'} 
              stroke="#333"
              stroke-width="2"
            />
          {/if}
          
          <!-- Cutouts representation -->
          {#if design.cutouts && design.cutouts.length > 0}
            {#each design.cutouts as cutout, i}
              {#if cutout.shape === 'circle'}
                <circle
                  cx={50 + (cutout.x / 2)}
                  cy={50 + (cutout.y / 2)}
                  r={cutout.size / 4}
                  fill="white"
                  stroke="red"
                  stroke-width="1"
                />
              {:else if cutout.shape === 'rectangle'}
                <rect
                  x={50 + (cutout.x / 2) - (cutout.size / 4)}
                  y={50 + (cutout.y / 2) - (cutout.size / 4)}
                  width={cutout.size / 2}
                  height={cutout.size / 2}
                  fill="white"
                  stroke="red"
                  stroke-width="1"
                />
              {:else if cutout.shape === 'triangle'}
                <polygon
                  points="
                    ${50 + (cutout.x / 2)},${50 + (cutout.y / 2) - (cutout.size / 4)}
                    ${50 + (cutout.x / 2) + (cutout.size / 4)},${50 + (cutout.y / 2) + (cutout.size / 4)}
                    ${50 + (cutout.x / 2) - (cutout.size / 4)},${50 + (cutout.y / 2) + (cutout.size / 4)}
                  "
                  fill="white"
                  stroke="red"
                  stroke-width="1"
                />
              {/if}
            {/each}
          {/if}
        {:else}
          <text x="150" y="100" text-anchor="middle">No design to preview</text>
        {/if}
      </svg>
    </div>
    
    <p class="has-text-centered mt-3">Review your design and price quote below.</p>
  </div>
  
  <div class="box mt-4">
    <h3 class="title is-5">Price Quote</h3>
    
    <table class="table is-fullwidth">
      <tbody>
        <tr>
          <th>Base Material Cost</th>
          <td class="has-text-right">€{baseMaterialPrice.toFixed(2)}</td>
        </tr>
        <tr>
          <th>Cutouts ({design.cutouts?.length || 0})</th>
          <td class="has-text-right">€{cutoutsPrice.toFixed(2)}</td>
        </tr>
        <tr>
          <th>Coating ({design.coating?.name || 'None'})</th>
          <td class="has-text-right">€{coatingPrice.toFixed(2)}</td>
        </tr>
        <tr class="is-selected">
          <th>Total Price</th>
          <td class="has-text-right has-text-weight-bold">€{totalPrice.toFixed(2)}</td>
        </tr>
      </tbody>
    </table>
    
    <div class="notification is-info is-light mt-4">
      <p>This quote is an estimate based on your design specifications. The final price may vary based on manufacturing details and additional requirements.</p>
    </div>
  </div>
</div>