<!-- DesignPreview.svelte -->
<script>
  import { onMount } from 'svelte';
  import { designPieces } from '../stores/designStore';
  import { v4 as uuidv4 } from 'uuid'; // You'll need to install uuid package

  export let design;
  
  let canvas;
  let isDragging = false;
  let draggedPieceId = null;
  let dragOffset = { x: 0, y: 0 };
  
  $: scale = 0.25;
  $: canvasWidth = 400;
  $: canvasHeight = 300;

  // Add new piece to the canvas
  function addPiece() {
    const newPiece = {
      id: uuidv4(),
      type: design.shape,
      material: design.material,
      dimensions: { ...design.dimensions },
      position: { x: 50, y: 50 } // Default position
    };
    
    designPieces.update(pieces => [...pieces, newPiece]);
  }

  function handleMouseDown(event) {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    
    // Check which piece was clicked
    const clickedPiece = findClickedPiece(x, y);
    if (clickedPiece) {
      isDragging = true;
      draggedPieceId = clickedPiece.id;
      dragOffset.x = x - clickedPiece.position.x;
      dragOffset.y = y - clickedPiece.position.y;
    }
  }
  
  function handleMouseMove(event) {
    if (!isDragging) return;
    
    const rect = canvas.getBoundingClientRect();
    const newX = event.clientX - rect.left - dragOffset.x;
    const newY = event.clientY - rect.top - dragOffset.y;
    
    designPieces.update(pieces =>
      pieces.map(piece =>
        piece.id === draggedPieceId
          ? {
              ...piece,
              position: {
                x: Math.max(0, Math.min(newX, canvasWidth - getPieceWidth(piece))),
                y: Math.max(0, Math.min(newY, canvasHeight - getPieceHeight(piece)))
              }
            }
          : piece
      )
    );
    
    drawPreview();
  }
  
  function handleMouseUp() {
    isDragging = false;
    draggedPieceId = null;
  }
  
  function findClickedPiece(x, y) {
    return $designPieces.find(piece => isInsidePiece(x, y, piece));
  }
  
  function isInsidePiece(x, y, piece) {
    const width = getPieceWidth(piece);
    const height = getPieceHeight(piece);
    
    return x >= piece.position.x &&
           x <= piece.position.x + width &&
           y >= piece.position.y &&
           y <= piece.position.y + height;
  }
  
  function getPieceWidth(piece) {
    if (piece.type === 'rectangle') {
      return piece.dimensions.length * scale;
    } else if (piece.type === 'circle') {
      return piece.dimensions.diameter * scale;
    }
    return 0;
  }
  
  function getPieceHeight(piece) {
    if (piece.type === 'rectangle') {
      return piece.dimensions.width * scale;
    } else if (piece.type === 'circle') {
      return piece.dimensions.diameter * scale;
    }
    return 0;
  }
  
  function drawPreview() {
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);
    
    // Draw grid
    drawGrid(ctx);
    
    // Draw all pieces
    $designPieces.forEach(piece => {
      drawPiece(ctx, piece);
    });
  }

  function drawGrid(ctx) {
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
  }

  function drawPiece(ctx, piece) {
    ctx.beginPath();
    ctx.strokeStyle = '#333';
    ctx.fillStyle = '#f5f5f5';
    
    if (piece.type === 'rectangle') {
      const width = piece.dimensions.length * scale;
      const height = piece.dimensions.width * scale;
      ctx.rect(piece.position.x, piece.position.y, width, height);
    } else if (piece.type === 'circle') {
      const radius = (piece.dimensions.diameter * scale) / 2;
      ctx.arc(
        piece.position.x + radius,
        piece.position.y + radius,
        radius,
        0,
        Math.PI * 2
      );
    }
    
    ctx.fill();
    ctx.stroke();
    
    // Draw piece ID and material
    ctx.font = '10px Arial';
    ctx.fillStyle = '#333';
    ctx.fillText(`ID: ${piece.id.slice(0, 8)}`, piece.position.x + 5, piece.position.y + 15);
    ctx.fillText(piece.material.toUpperCase(), piece.position.x + 5, piece.position.y + 30);
  }

  onMount(() => {
    drawPreview();
  });
</script>

<div class="box mt-4">
  <h3 class="title is-5">Aperçu du design</h3>
  
  <div class="buttons">
    <button class="button is-primary" on:click={addPiece}>
      Ajouter une pièce
    </button>
  </div>

  <canvas
    bind:this={canvas}
    width={canvasWidth}
    height={canvasHeight}
    on:mousedown={handleMouseDown}
    on:mousemove={handleMouseMove}
    on:mouseup={handleMouseUp}
    on:mouseleave={handleMouseUp}
    use:drawPreview
  ></canvas>
  
  <div class="mt-3">
    <h4 class="title is-6">Pièces dans le design:</h4>
    {#each $designPieces as piece}
      <div class="box">
        <p><strong>ID:</strong> {piece.id}</p>
        <p><strong>Type:</strong> {piece.type}</p>
        <p><strong>Matériau:</strong> {piece.material}</p>
        <p><strong>Dimensions:</strong> 
          {#each Object.entries(piece.dimensions) as [key, value]}
            {key}: {value}mm 
          {/each}
        </p>
      </div>
    {/each}
  </div>
</div>

<style>
  canvas {
    border: 1px solid #ccc;
    width: 100%;
    max-width: 400px;
    height: auto;
    cursor: move;
  }
</style>
