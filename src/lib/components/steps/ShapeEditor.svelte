<!-- ShapeEditor.svelte -->
<script>
  import { createEventDispatcher, onMount } from 'svelte';
  
  export let design;
  
  const dispatch = createEventDispatcher();
  
  let canvas;
  let ctx;
  let canvasWidth = 600;
  let canvasHeight = 400;
  let scale = 1;
  let cutouts = design.cutouts || [];
  let xOffset = 0;
  let yOffset = 0;
  
  // Cutout options
  const cutoutShapes = [
    { id: 'circle', name: 'Circle' },
    { id: 'rectangle', name: 'Rectangle' },
    { id: 'triangle', name: 'Triangle' }
  ];
  
  // Current cutout being added
  let selectedCutoutShape = cutoutShapes[0];
  let cutoutSize = 50; // Default size in mm
  let isAddingCutout = false;
  let cutoutPosition = { x: 0, y: 0 };
  let isDraggingCutout = false;
  let selectedCutoutIndex = -1;
  
  // Distance from cutout to edge
  let edgeDistance = 20; // Default 20mm
  
  onMount(() => {
    ctx = canvas.getContext('2d');
    renderCanvas();
  });
  
  // Render the shape and cutouts
  function renderCanvas() {
    if (!ctx || !design.shape) return;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);
    
    // Calculate scale to fit shape on canvas
    let shapeWidth, shapeHeight;
    if (design.shape.id === 'circle') {
      shapeWidth = shapeHeight = design.shape.dimensions.diameter;
    } else {
      shapeWidth = design.shape.dimensions.width;
      shapeHeight = design.shape.dimensions.height;
    }
    
    const paddingPercent = 0.2; // 20% padding
    const maxWidth = canvasWidth * (1 - paddingPercent);
    const maxHeight = canvasHeight * (1 - paddingPercent);
    
    scale = Math.min(maxWidth / shapeWidth, maxHeight / shapeHeight);
    
    // Center the shape
    xOffset = (canvasWidth - shapeWidth * scale) / 2;
    yOffset = (canvasHeight - shapeHeight * scale) / 2;
    
    // Draw the shape
    ctx.save();
    ctx.translate(xOffset, yOffset);
    ctx.fillStyle = design.coating?.color?.hex || '#ccc';
    ctx.strokeStyle = '#888';
    ctx.lineWidth = 2;
    
    if (design.shape.id === 'rectangle') {
      ctx.beginPath();
      ctx.rect(0, 0, shapeWidth * scale, shapeHeight * scale);
      ctx.fill();
      ctx.stroke();
    } else if (design.shape.id === 'circle') {
      const radius = (shapeWidth * scale) / 2;
      ctx.beginPath();
      ctx.arc(radius, radius, radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    } else if (design.shape.id === 'triangle') {
      ctx.beginPath();
      ctx.moveTo(shapeWidth * scale / 2, 0);
      ctx.lineTo(shapeWidth * scale, shapeHeight * scale);
      ctx.lineTo(0, shapeHeight * scale);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    } else if (design.shape.id === 'L-shape') {
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(shapeWidth * scale * 0.6, 0);
      ctx.lineTo(shapeWidth * scale * 0.6, shapeHeight * scale * 0.6);
      ctx.lineTo(shapeWidth * scale, shapeHeight * scale * 0.6);
      ctx.lineTo(shapeWidth * scale, shapeHeight * scale);
      ctx.lineTo(0, shapeHeight * scale);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    }
    
    // Draw cutouts
    ctx.fillStyle = 'white';
    ctx.strokeStyle = 'red';
    
    cutouts.forEach((cutout, index) => {
      const isSelected = index === selectedCutoutIndex;
      
      ctx.save();
      if (isSelected) {
        ctx.strokeStyle = 'blue';
        ctx.lineWidth = 3;
      } else {
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 2;
      }
      
      if (cutout.shape === 'circle') {
        ctx.beginPath();
        ctx.arc(
          cutout.x * scale, 
          cutout.y * scale, 
          cutout.size * scale / 2, 
          0, 
          Math.PI * 2
        );
        ctx.fill();
        ctx.stroke();
      } else if (cutout.shape === 'rectangle') {
        ctx.beginPath();
        ctx.rect(
          (cutout.x - cutout.size/2) * scale, 
          (cutout.y - cutout.size/2) * scale, 
          cutout.size * scale, 
          cutout.size * scale
        );
        ctx.fill();
        ctx.stroke();
      } else if (cutout.shape === 'triangle') {
        const halfSize = cutout.size * scale / 2;
        ctx.beginPath();
        ctx.moveTo(cutout.x * scale, (cutout.y - halfSize) * scale);
        ctx.lineTo((cutout.x + halfSize) * scale, (cutout.y + halfSize) * scale);
        ctx.lineTo((cutout.x - halfSize) * scale, (cutout.y + halfSize) * scale);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
      }
      
      // Draw distance to edge (if selected)
      if (isSelected) {
        const distanceLabel = `${Math.round(calculateEdgeDistance(cutout))}mm`;
        ctx.fillStyle = 'blue';
        ctx.font = '12px Arial';
        ctx.fillText(distanceLabel, cutout.x * scale + 10, cutout.y * scale - 10);
      }
      
      ctx.restore();
    });
    
    // Draw preview of cutout being added
    if (isAddingCutout) {
      ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
      ctx.strokeStyle = 'blue';
      
      if (selectedCutoutShape.id === 'circle') {
        ctx.beginPath();
        ctx.arc(
          cutoutPosition.x * scale, 
          cutoutPosition.y * scale, 
          cutoutSize * scale / 2, 
          0, 
          Math.PI * 2
        );
        ctx.fill();
        ctx.stroke();
      } else if (selectedCutoutShape.id === 'rectangle') {
        ctx.beginPath();
        ctx.rect(
          (cutoutPosition.x - cutoutSize/2) * scale, 
          (cutoutPosition.y - cutoutSize/2) * scale, 
          cutoutSize * scale, 
          cutoutSize * scale
        );
        ctx.fill();
        ctx.stroke();
      } else if (selectedCutoutShape.id === 'triangle') {
        const halfSize = cutoutSize * scale / 2;
        ctx.beginPath();
        ctx.moveTo(cutoutPosition.x * scale, (cutoutPosition.y - halfSize) * scale);
        ctx.lineTo((cutoutPosition.x + halfSize) * scale, (cutoutPosition.y + halfSize) * scale);
        ctx.lineTo((cutoutPosition.x - halfSize) * scale, (cutoutPosition.y + halfSize) * scale);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
      }
      
      // Display distance to edge
      const distance = calculateEdgeDistanceForPreview();
      const distanceLabel = `${Math.round(distance)}mm`;
      ctx.fillStyle = 'blue';
      ctx.font = '12px Arial';
      ctx.fillText(distanceLabel, cutoutPosition.x * scale + 10, cutoutPosition.y * scale - 10);
    }
    
    ctx.restore();
  }
  
  function calculateEdgeDistance(cutout) {
    // Convert cutout position to original dimensions
    const x = cutout.x;
    const y = cutout.y;
    const size = cutout.size;
    
    let minDistance = Infinity;
    
    if (design.shape.id === 'rectangle') {
      const width = design.shape.dimensions.width;
      const height = design.shape.dimensions.height;
      
      // Calculate distances to each edge
      const distances = [
        x - size/2,                // Left edge
        y - size/2,                // Top edge
        width - (x + size/2),      // Right edge
        height - (y + size/2)      // Bottom edge
      ];
      
      minDistance = Math.min(...distances);
    } else if (design.shape.id === 'circle') {
      const radius = design.shape.dimensions.diameter / 2;
      const centerX = radius;
      const centerY = radius;
      
      // Distance from cutout center to shape center
      const dx = x - centerX;
      const dy = y - centerY;
      const distToCenter = Math.sqrt(dx*dx + dy*dy);
      
      // For circle, the distance to edge is the distance from 
      // the outer edge of the cutout to the edge of the circle
      minDistance = radius - distToCenter - size/2;
    } else if (design.shape.id === 'triangle') {
      // For triangle, this is an approximation
      const width = design.shape.dimensions.width;
      const height = design.shape.dimensions.height;
      
      // Approximate distances (this is simplified)
      minDistance = Math.min(
        x - size/2,                // Left edge
        y - size/2,                // Top edge
        width - (x + size/2),      // Right edge
        height - (y + size/2)      // Bottom edge
      );
    }
    
    return Math.max(0, minDistance);
  }
  
  function calculateEdgeDistanceForPreview() {
    // Same as above but for the preview cutout
    return calculateEdgeDistance({
      x: cutoutPosition.x,
      y: cutoutPosition.y,
      size: cutoutSize,
      shape: selectedCutoutShape.id
    });
  }
  
  function startCutoutPlacement(event) {
    if (!design.shape) return;
    
    const rect = canvas.getBoundingClientRect();
    const mouseX = (event.clientX - rect.left - xOffset) / scale;
    const mouseY = (event.clientY - rect.top - yOffset) / scale;
    
    // Check if clicking on an existing cutout
    const clickedCutoutIndex = cutouts.findIndex(cutout => {
      if (cutout.shape === 'circle') {
        const dx = cutout.x - mouseX;
        const dy = cutout.y - mouseY;
        const distance = Math.sqrt(dx*dx + dy*dy);
        return distance <= cutout.size/2;
      } else if (cutout.shape === 'rectangle') {
        return (
          mouseX >= cutout.x - cutout.size/2 &&
          mouseX <= cutout.x + cutout.size/2 &&
          mouseY >= cutout.y - cutout.size/2 &&
          mouseY <= cutout.y + cutout.size/2
        );
      } else if (cutout.shape === 'triangle') {
        // Simplified triangle hit testing (bounding box)
        return (
          mouseX >= cutout.x - cutout.size/2 &&
          mouseX <= cutout.x + cutout.size/2 &&
          mouseY >= cutout.y - cutout.size/2 &&
          mouseY <= cutout.y + cutout.size/2
        );
      }
      return false;
    });
    
    if (clickedCutoutIndex >= 0) {
      // Start dragging existing cutout
      isDraggingCutout = true;
      selectedCutoutIndex = clickedCutoutIndex;
      isAddingCutout = false;
    } else {
      // Start adding a new cutout
      isAddingCutout = true;
      selectedCutoutIndex = -1;
      cutoutPosition = { x: mouseX, y: mouseY };
    }
    
    renderCanvas();
  }
  
  function moveHandler(event) {
    if (!isAddingCutout && !isDraggingCutout) return;
    
    const rect = canvas.getBoundingClientRect();
    const mouseX = (event.clientX - rect.left - xOffset) / scale;
    const mouseY = (event.clientY - rect.top - yOffset) / scale;
    
    if (isAddingCutout) {
      cutoutPosition = { x: mouseX, y: mouseY };
    } else if (isDraggingCutout && selectedCutoutIndex >= 0) {
      cutouts[selectedCutoutIndex].x = mouseX;
      cutouts[selectedCutoutIndex].y = mouseY;
      
      // Update edge distance display
      edgeDistance = calculateEdgeDistance(cutouts[selectedCutoutIndex]);
    }
    
    renderCanvas();
  }
  
  function endHandler() {
    if (isAddingCutout) {
      // Add the new cutout
      const newCutout = {
        shape: selectedCutoutShape.id,
        x: cutoutPosition.x,
        y: cutoutPosition.y,
        size: cutoutSize
      };
      
      cutouts = [...cutouts, newCutout];
      
      // Update the design
      dispatch('update', {
        field: 'cutouts',
        value: cutouts
      });
    } else if (isDraggingCutout) {
      // Update the design with the new cutout positions
      dispatch('update', {
        field: 'cutouts',
        value: cutouts
      });
    }
    
    isAddingCutout = false;
    isDraggingCutout = false;
    renderCanvas();
  }
  
  function updateCutoutSize() {
    renderCanvas();
    
    if (selectedCutoutIndex >= 0) {
      // Update selected cutout size
      cutouts[selectedCutoutIndex].size = cutoutSize;
      
      // Update the design
      dispatch('update', {
        field: 'cutouts',
        value: cutouts
      });
    }
  }
  
  function deleteCutout() {
    if (selectedCutoutIndex >= 0) {
      cutouts = cutouts.filter((_, index) => index !== selectedCutoutIndex);
      selectedCutoutIndex = -1;
      
      // Update the design
      dispatch('update', {
        field: 'cutouts',
        value: cutouts
      });
      
      renderCanvas();
    }
  }
  
  function updateEdgeDistance() {
    if (selectedCutoutIndex >= 0) {
      const cutout = cutouts[selectedCutoutIndex];
      const currentDistance = calculateEdgeDistance(cutout);
      const difference = edgeDistance - currentDistance;
      
      // Move cutout to maintain desired edge distance
      // This is a simplified approach and might need refinement
      if (design.shape.id === 'rectangle') {
        const width = design.shape.dimensions.width;
        const height = design.shape.dimensions.height;
        
        // Find which edge is closest
        const leftDist = cutout.x - cutout.size/2;
        const topDist = cutout.y - cutout.size/2;
        const rightDist = width - (cutout.x + cutout.size/2);
        const bottomDist = height - (cutout.y + cutout.size/2);
        
        const minDist = Math.min(leftDist, topDist, rightDist, bottomDist);
        
        if (minDist === leftDist) {
          cutout.x += difference;
        } else if (minDist === topDist) {
          cutout.y += difference;
        } else if (minDist === rightDist) {
          cutout.x -= difference;
        } else {
          cutout.y -= difference;
        }
      } else if (design.shape.id === 'circle') {
        const radius = design.shape.dimensions.diameter / 2;
        const centerX = radius;
        const centerY = radius;
        
        // Move towards or away from center
        const dx = cutout.x - centerX;
        const dy = cutout.y - centerY;
        const dist = Math.sqrt(dx*dx + dy*dy);
        
        if (dist > 0) {
          // Calculate new distance from center
          const newDistFromCenter = radius - edgeDistance - cutout.size/2;
          const scaleFactor = newDistFromCenter / dist;
          
          cutout.x = centerX + dx * scaleFactor;
          cutout.y = centerY + dy * scaleFactor;
        }
      }
      
      // Update the design
      dispatch('update', {
        field: 'cutouts',
        value: cutouts
      });
      
      renderCanvas();
    }
  }
  
  $: if (design.shape) {
    // If the shape changes, re-render the canvas
    renderCanvas();
  }
</script>

<div>
  <h2 class="title is-4">Customize Shape</h2>
  <p class="subtitle is-6 mb-4">Add and position cutout shapes</p>
  
  <div class="box p-4">
    <div class="level mb-3">
      <div class="level-left">
        <div class="field is-horizontal">
          <div class="field-label is-normal">
            <label class="label">Cutout Shape</label>
          </div>
          <div class="field-body">
            <div class="field is-narrow">
              <div class="control">
                <div class="select">
                  <select bind:value={selectedCutoutShape}>
                    {#each cutoutShapes as shape}
                      <option value={shape}>{shape.name}</option>
                    {/each}
                  </select>
                </div>
              </div>
            </div>
            
            <div class="field is-narrow">
              <div class="control">
                <div class="field has-addons">
                  <p class="control">
                    <input 
                      class="input" 
                      type="number" 
                      bind:value={cutoutSize}
                      on:change={updateCutoutSize}
                      min="5" 
                      max="200"
                      step="5"
                    >
                  </p>
                  <p class="control">
                    <a class="button is-static">
                      mm
                    </a>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="level-right">
        <div class="buttons">
          <button class="button is-small is-danger" on:click={deleteCutout} disabled={selectedCutoutIndex < 0}>
            <span class="icon is-small">
              <i class="fas fa-trash"></i>
            </span>
            <span>Delete Cutout</span>
          </button>
        </div>
      </div>
    </div>
    
    {#if selectedCutoutIndex >= 0}
      <div class="field is-horizontal mb-4">
        <div class="field-label is-normal">
          <label class="label">Edge Distance</label>
        </div>
        <div class="field-body">
          <div class="field has-addons">
            <p class="control">
              <input 
                class="input" 
                type="number" 
                bind:value={edgeDistance}
                on:change={updateEdgeDistance}
                min="5" 
                max="100"
                step="1"
              >
            </p>
            <p class="control">
              <a class="button is-static">
                mm
              </a>
            </p>
          </div>
        </div>
      </div>
    {/if}
    
    <div class="canvas-container has-background-light">
      <canvas 
        bind:this={canvas} 
        width={canvasWidth} 
        height={canvasHeight}
        on:mousedown={startCutoutPlacement}
        on:mousemove={moveHandler}
        on:mouseup={endHandler}
        on:mouseleave={endHandler}
      ></canvas>
    </div>
    
    <p class="help mt-2">Click to add a new cutout shape. Click and drag existing cutouts to reposition them.</p>
  </div>
</div>

<style>
  .canvas-container {
    border: 1px solid #dbdbdb;
    border-radius: 4px;
    overflow: hidden;
    display: flex;
    justify-content: center;
  }
  
  canvas {
    cursor: crosshair;
  }
</style>