<script>
  export let design;
  
  $: scale = 0.25; // 1mm = 0.25px
  $: canvasWidth = 400;
  $: canvasHeight = 300;
  
  function drawPreview(canvas) {
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);
    
    // Draw grid
    ctx.beginPath();
    ctx.strokeStyle = '#ddd';
    for (let x = 0; x < canvasWidth; x += 10) {
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvasHeight);
    }
    for (let y = 0; y < canvasHeight; y += 10) {
      ctx.moveTo(0, y);
      ctx.lineTo(canvasWidth, y);
    }
    ctx.stroke();
    
    if (design.shape && design.dimensions) {
      // Draw shape
      ctx.beginPath();
      ctx.strokeStyle = '#333';
      ctx.fillStyle = '#f5f5f5';
      
      if (design.shape === 'rectangle' && design.dimensions.length && design.dimensions.width) {
        const width = design.dimensions.length * scale;
        const height = design.dimensions.width * scale;
        const x = (canvasWidth - width) / 2;
        const y = (canvasHeight - height) / 2;
        ctx.rect(x, y, width, height);
      }
      
      ctx.fill();
      ctx.stroke();
      
      // Draw dimensions
      ctx.font = '12px Arial';
      ctx.fillStyle = '#333';
      if (design.material) {
        ctx.fillText(design.material.toUpperCase(), canvasWidth - 80, 20);
      }
    }
  }
</script>

<div class="box mt-4">
  <h3 class="title is-5">Aperçu du design</h3>
  <canvas
    bind:this={canvas}
    width={canvasWidth}
    height={canvasHeight}
    use:drawPreview
  ></canvas>
  
  {#if design.material && design.shape && design.dimensions}
    <div class="mt-3">
      <p><strong>Matériau:</strong> {design.material}</p>
      <p><strong>Dimensions:</strong> 
        {#each Object.entries(design.dimensions) as [key, value]}
          {key}: {value}mm 
        {/each}
      </p>
    </div>
  {/if}
</div>

<style>
  canvas {
    border: 1px solid #ccc;
    width: 100%;
    max-width: 400px;
    height: auto;
  }
</style>