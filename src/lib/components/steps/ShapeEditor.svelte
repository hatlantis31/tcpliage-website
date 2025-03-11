<!-- ShapeEditor.svelte -->
<script>
  import { createEventDispatcher, onMount } from 'svelte';
  
  export let design;
  
  const dispatch = createEventDispatcher();
  
  let canvas;
  let ctx;
  let canvasWidth = 600;
  let canvasHeight = 400;
  let isDrawing = false;
  let cutouts = design.cutouts || [];
  let currentCutout = [];
  let scale = 1;
  
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
    const xOffset = (canvasWidth - shapeWidth * scale) / 2;
    const yOffset = (canvasHeight - shapeHeight * scale) / 2;
    
    // Draw the shape
    ctx.save();
    ctx.translate(xOffset, yOffset);
    ctx.fillStyle = '#ccc';
    ctx.strokeStyle = '#888';
    ctx.lineWidth = 2;
    
    if (design.shape.id === 'rectangle') {
      ctx.fillRect(0, 0, shapeWidth * scale, shapeHeight * scale);
      ctx.strokeRect(0, 0, shapeWidth * scale, shapeHeight * scale);
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
    
    for (const cutout of cutouts) {
      ctx.beginPath();
      for (let i = 0; i < cutout.length; i++) {
        const [x, y] = cutout[i];
        if (i === 0) {
          ctx.moveTo(x * scale, y * scale);
        } else {
          ctx.lineTo(x * scale, y * scale);
        }
      }
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    }
    
    // Draw current cutout if drawing
    if (currentCutout.length > 0) {
      ctx.beginPath();
      for (let i = 0; i < currentCutout.length; i++) {
        const [x, y] = currentCutout[i];
        if (i === 0) {
          ctx.moveTo(x * scale, y * scale);
        } else {
          ctx.lineTo(x * scale, y * scale);
        }
      }
      ctx.stroke();
    }
    
    ctx.restore();
  }
  
  function startDrawing(event) {
    if (!design.shape) return;
    
    isDrawing = true;
    
    // Get canvas-relative coordinates
    const rect = canvas.getBoundingClientRect();
    const x = (event.clientX - rect.left) / scale;
    const y = (event.clientY - rect.top) / scale;
    
    currentCutout = [[x, y]];
    renderCanvas();
  }
  
  function draw(event) {
    if (!isDrawing) return;
    
    // Get canvas-relative coordinates
    const rect = canvas.getBoundingClientRect();
    const x = (event.clientX - rect.left) / scale;
    const y = (event.clientY - rect.top) / scale;
    
    currentCutout.push([x, y]);
    renderCanvas();
  }
  
  function stopDrawing() {
    if (!isDrawing) return;
    
    isDrawing = false;
    
    if (currentCutout.length > 2) {
      // Close the shape if needed
      cutouts = [...cutouts, currentCutout];
      
      // Update the design
      dispatch('update', {
        field: 'cutouts',
        value: cutouts
      });
    }
    
    currentCutout = [];
    renderCanvas();
  }
  
  function clearLastCutout() {
    if (cutouts.length > 0) {
      cutouts = cutouts.slice(0, -1);
      
      dispatch('update', {
        field: 'cutouts',
        value: cutouts
      });
      
      renderCanvas();
    }
  }
  
  function clearAllCutouts() {
    cutouts = [];
    
    dispatch('update', {
      field: 'cutouts',
      value: cutouts
    });
    
    renderCanvas();
  }
  
  $: if (design.shape) {
    // If the shape changes, re-render the canvas
    renderCanvas();
  }
</script>

<div>
  <h2 class="title is-4">Customize Shape</h2>
  <p class="subtitle is-6 mb-4">Draw to create cutouts from your piece</p>
  
  <div class="box p-4">
    <div class="level mb-3">
      <div class="level-left">
        <p>Draw closed shapes to create cutouts</p>
      </div>
      <div class="level-right">
        <div class="buttons">
          <button class="button is-small" on:click={clearLastCutout}>
            <span>Undo Last Cutout</span>
          </button>
          <button class="button is-small is-danger" on:click={clearAllCutouts}>
            <span>Clear All Cutouts</span>
          </button>
        </div>
      </div>
    </div>
    
    <div class="canvas-container has-background-light">
      <canvas 
        bind:this={canvas} 
        width={canvasWidth} 
        height={canvasHeight}
        on:mousedown={startDrawing}
        on:mousemove={draw}
        on:mouseup={stopDrawing}
        on:mouseleave={stopDrawing}
      ></canvas>
    </div>
    
    <p class="help mt-2">Click and drag to create cutouts. Draw a complete closed shape for each cutout.</p>
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