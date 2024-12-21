<!-- src/routes/designer/+page.svelte -->
<script>
    import { onMount } from 'svelte';
    
    let canvas;
    let ctx;
    let points = [];
    let thickness = 2.0;
    let material = 'acier';
    let isDrawing = false;
    let scale = 1; // 1 pixel = 1mm
    let message = '';
    let messageType = 'info';
    
    onMount(() => {
        ctx = canvas.getContext('2d');
        canvas.width = 800;
        canvas.height = 600;
        drawGrid();
    });
    
    function drawGrid() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Dessiner la grille (tous les 10mm)
        ctx.beginPath();
        ctx.strokeStyle = '#ddd';
        
        for (let x = 0; x < canvas.width; x += 10 * scale) {
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvas.height);
        }
        
        for (let y = 0; y < canvas.height; y += 10 * scale) {
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
        }
        
        ctx.stroke();
        
        // Dessiner les points et les lignes
        if (points.length > 0) {
            ctx.beginPath();
            ctx.strokeStyle = '#333';
            ctx.lineWidth = 2;
            
            ctx.moveTo(points[0].x, points[0].y);
            for (let i = 1; i < points.length; i++) {
                ctx.lineTo(points[i].x, points[i].y);
            }
            
            if (points.length > 2) {
                ctx.lineTo(points[0].x, points[0].y);
            }
            
            ctx.stroke();
            
            // Dessiner les points
            points.forEach((point, index) => {
                ctx.beginPath();
                ctx.fillStyle = '#007bff';
                ctx.arc(point.x, point.y, 5, 0, Math.PI * 2);
                ctx.fill();
                
                // Afficher les coordonnées
                ctx.fillStyle = '#333';
                ctx.font = '12px Arial';
                ctx.fillText(`${Math.round(point.x/scale)},${Math.round(point.y/scale)}`, point.x + 10, point.y + 10);
            });
        }
    }
    
    async function validatePiece() {
        if (points.length < 3) {
            message = 'Ajoutez au moins 3 points pour former une pièce';
            messageType = 'error';
            return;
        }
        
        const scaledPoints = points.map(p => ({
            x: p.x / scale,
            y: p.y / scale
        }));
        
        try {
            const response = await fetch('http://localhost:8000/validate-piece', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    points: scaledPoints,
                    thickness,
                    material
                })
            });
            
            const result = await response.json();
            message = result.message;
            messageType = result.valid ? 'success' : 'error';
        } catch (error) {
            message = 'Erreur de connexion au serveur';
            messageType = 'error';
        }
    }
    
    function handleCanvasClick(event) {
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        
        points.push({ x, y });
        points = points; // Force Svelte reactivity
        drawGrid();
    }
    
    function undoLastPoint() {
        points.pop();
        points = points;
        drawGrid();
    }
    
    function clearDrawing() {
        points = [];
        drawGrid();
    }
</script>

<div class="container p-4">
    <h1 class="title">Dessin de pièce métallique</h1>
    
    <div class="columns">
        <div class="column is-8">
            <canvas
                bind:this={canvas}
                on:click={handleCanvasClick}
                class="border"
            ></canvas>
        </div>
        
        <div class="column is-4">
            <div class="field">
                <label class="label">Épaisseur (mm)</label>
                <input
                    type="number"
                    bind:value={thickness}
                    class="input"
                    min="0.5"
                    max="50"
                    step="0.5"
                />
            </div>
            
            <div class="field">
                <label class="label">Matériau</label>
                <div class="select">
                    <select bind:value={material}>
                        <option value="acier">Acier</option>
                        <option value="aluminium">Aluminium</option>
                        <option value="inox">Inox</option>
                    </select>
                </div>
            </div>
            
            <div class="buttons">
                <button class="button is-primary" on:click={validatePiece}>
                    Valider la pièce
                </button>
                <button class="button" on:click={undoLastPoint}>
                    Annuler dernier point
                </button>
                <button class="button is-danger" on:click={clearDrawing}>
                    Effacer tout
                </button>
            </div>
            
            {#if message}
                <div class="notification is-{messageType === 'error' ? 'danger' : 'success'}">
                    {message}
                </div>
            {/if}
        </div>
    </div>
</div>

<style>
    canvas {
        border: 1px solid #ccc;
        cursor: crosshair;
    }
    
    .border {
        border: 1px solid #ccc;
    }
</style>