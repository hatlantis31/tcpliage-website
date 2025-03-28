<!-- ProjectGallery.svelte -->
<script>
    import { onMount } from 'svelte';
    
    export let projects = [];
    export let columns = 3; // Number of columns on desktop
    export let showFilters = true;
    export let categories = ['Tous', 'Urgence', 'Couvertines', 'Habillages', 'Quincaillerie', 'Sur Mesure'];
    
    let selectedCategory = 'Tous';
    let galleryElement;
    let lightboxActive = false;
    let currentProject = null;
    let touchStartX = 0;
    let touchEndX = 0;
    
    // Filter projects by selected category
    $: filteredProjects = selectedCategory === 'Tous'
      ? projects
      : projects.filter(project => project.category === selectedCategory);
    
    // Responsive columns
    $: columnClass = {
      desktop: `is-${12 / columns}`,
      tablet: `is-${columns <= 2 ? 12 / columns : 6}`
    };
    
    // Apply masonry layout when projects change
    $: if (filteredProjects && galleryElement) {
      setTimeout(applyMasonryLayout, 100);
    }
    
    function applyMasonryLayout() {
      if (!galleryElement) return;
      
      const items = galleryElement.querySelectorAll('.gallery-item');
      if (items.length === 0) return;
      
      // Reset heights
      items.forEach(item => {
        item.style.height = 'auto';
      });
      
      // Apply masonry only on desktop
      if (window.innerWidth >= 1024) {
        // Get items per row based on columns
        const itemsPerRow = columns;
        
        for (let i = 0; i < items.length; i += itemsPerRow) {
          // Get max height for this row
          let maxHeight = 0;
          for (let j = i; j < i + itemsPerRow && j < items.length; j++) {
            const height = items[j].offsetHeight;
            if (height > maxHeight) {
              maxHeight = height;
            }
          }
          
          // Set all items in this row to max height
          for (let j = i; j < i + itemsPerRow && j < items.length; j++) {
            items[j].style.height = `${maxHeight}px`;
          }
        }
      }
    }
    
    function setCategory(category) {
      selectedCategory = category;
    }
    
    function openLightbox(project) {
      currentProject = project;
      lightboxActive = true;
      document.body.style.overflow = 'hidden';
    }
    
    function closeLightbox() {
      lightboxActive = false;
      document.body.style.overflow = '';
    }
    
    function nextProject() {
      if (!currentProject) return;
      
      const currentIndex = filteredProjects.findIndex(p => p.id === currentProject.id);
      if (currentIndex >= 0 && currentIndex < filteredProjects.length - 1) {
        currentProject = filteredProjects[currentIndex + 1];
      } else {
        currentProject = filteredProjects[0];
      }
    }
    
    function prevProject() {
      if (!currentProject) return;
      
      const currentIndex = filteredProjects.findIndex(p => p.id === currentProject.id);
      if (currentIndex > 0) {
        currentProject = filteredProjects[currentIndex - 1];
      } else {
        currentProject = filteredProjects[filteredProjects.length - 1];
      }
    }
    
    function handleKeydown(event) {
      if (!lightboxActive) return;
      
      if (event.key === 'Escape') {
        closeLightbox();
      } else if (event.key === 'ArrowRight') {
        nextProject();
      } else if (event.key === 'ArrowLeft') {
        prevProject();
      }
    }
    
    function handleTouchStart(event) {
      touchStartX = event.touches[0].clientX;
    }
    
    function handleTouchMove(event) {
      touchEndX = event.touches[0].clientX;
    }
    
    function handleTouchEnd() {
      if (!lightboxActive) return;
      
      const threshold = 50;
      const deltaX = touchEndX - touchStartX;
      
      if (deltaX > threshold) {
        prevProject();
      } else if (deltaX < -threshold) {
        nextProject();
      }
    }
    
    onMount(() => {
      window.addEventListener('keydown', handleKeydown);
      window.addEventListener('resize', applyMasonryLayout);
      
      // Apply initial masonry layout
      setTimeout(applyMasonryLayout, 300);
      
      return () => {
        window.removeEventListener('keydown', handleKeydown);
        window.removeEventListener('resize', applyMasonryLayout);
      };
    });
  </script>
  
  <svelte:window 
    on:touchstart={handleTouchStart}
    on:touchmove={handleTouchMove}
    on:touchend={handleTouchEnd}
  />
  
  <div class="project-gallery">
    {#if showFilters && categories.length > 0}
      <div class="filter-container">
        <div class="tabs">
          <ul>
            {#each categories as category}
              <li class={category === selectedCategory ? 'is-active' : ''}>
                <a 
                  href="#{category.toLowerCase()}" 
                  on:click|preventDefault={() => setCategory(category)}
                >
                  {category}
                </a>
              </li>
            {/each}
          </ul>
        </div>
      </div>
    {/if}
    
    <div class="gallery-container" bind:this={galleryElement}>
      {#if filteredProjects.length === 0}
        <div class="empty-gallery">
          <p>Aucun projet trouvé dans cette catégorie.</p>
          {#if selectedCategory !== 'Tous'}
            <button class="button is-primary mt-3" on:click={() => setCategory('Tous')}>
              Voir tous les projets
            </button>
          {/if}
        </div>
      {:else}
        <div class="columns is-multiline">
          {#each filteredProjects as project (project.id)}
            <div class="column {columnClass.desktop}-desktop is-6-tablet">
              <div class="gallery-item">
                <div 
                  class="project-card" 
                  on:click={() => openLightbox(project)}
                  on:keypress={(e) => e.key === 'Enter' && openLightbox(project)}
                  role="button"
                  tabindex="0"
                >
                  <div class="project-image-container">
                    <img 
                      src={project.image} 
                      alt={project.title} 
                      loading="lazy"
                      onError={(e) => e.target.src = 'https://via.placeholder.com/600x400?text=TC+PLIAGE'}
                    >
                    <div class="project-overlay">
                      <span class="view-project">
                        <span class="icon">
                          <i class="fas fa-search-plus"></i>
                        </span>
                        <span>Voir le projet</span>
                      </span>
                    </div>
                  </div>
                  <div class="project-info">
                    <h3 class="project-title">{project.title}</h3>
                    {#if project.category}
                      <span class="project-category">{project.category}</span>
                    {/if}
                  </div>
                </div>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  </div>
  
  <!-- Lightbox -->
  {#if lightboxActive && currentProject}
    <div class="lightbox" on:click|self={closeLightbox}>
      <button class="lightbox-close" on:click={closeLightbox}>
        <span class="icon">
          <i class="fas fa-times"></i>
        </span>
      </button>
      
      <div class="lightbox-content">
        <div class="lightbox-image-container">
          <img 
            src={currentProject.largeImage || currentProject.image} 
            alt={currentProject.title}
            on:click|stopPropagation
          >
        </div>
        
        <div class="lightbox-info" on:click|stopPropagation>
          <h3 class="lightbox-title">{currentProject.title}</h3>
          {#if currentProject.category}
            <span class="lightbox-category">{currentProject.category}</span>
          {/if}
          {#if currentProject.description}
            <p class="lightbox-description">{currentProject.description}</p>
          {/if}
          {#if currentProject.client}
            <p class="lightbox-client">
              <strong>Client:</strong> {currentProject.client}
            </p>
          {/if}
          {#if currentProject.date}
            <p class="lightbox-date">
              <strong>Date:</strong> {currentProject.date}
            </p>
          {/if}
        </div>
      </div>
      
      <div class="lightbox-controls">
        <button class="lightbox-control prev-control" on:click|stopPropagation={prevProject}>
          <span class="icon">
            <i class="fas fa-chevron-left"></i>
          </span>
        </button>
        <button class="lightbox-control next-control" on:click|stopPropagation={nextProject}>
          <span class="icon">
            <i class="fas fa-chevron-right"></i>
          </span>
        </button>
      </div>
    </div>
  {/if}
  
  <style>
    .project-gallery {
      margin-bottom: 2rem;
    }
    
    .filter-container {
      margin-bottom: 2rem;
      overflow-x: auto;
    }
    
    .tabs ul {
      flex-wrap: nowrap;
      min-width: max-content;
    }
    
    .tabs li.is-active a {
      border-color: #E53935;
      color: #E53935;
    }
    
    .gallery-container {
      position: relative;
    }
    
    .empty-gallery {
      text-align: center;
      padding: 4rem 2rem;
      color: #777;
      background-color: #f9f9f9;
      border-radius: 8px;
    }
    
    .gallery-item {
      margin-bottom: 1.5rem;
      transition: all 0.3s ease;
    }
    
    .project-card {
      background-color: white;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
      height: 100%;
      cursor: pointer;
      transition: all 0.3s ease;
    }
    
    .project-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 12px 25px rgba(0, 0, 0, 0.1);
    }
    
    .project-image-container {
      position: relative;
      overflow: hidden;
      height: 250px;
    }
    
    .project-image-container img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.5s ease;
    }
    
    .project-card:hover .project-image-container img {
      transform: scale(1.1);
    }
    
    .project-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 0;
      transition: opacity 0.3s ease;
    }
    
    .project-card:hover .project-overlay {
      opacity: 1;
    }
    
    .view-project {
      color: white;
      font-weight: 600;
      display: flex;
      align-items: center;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      background-color: rgba(229, 57, 53, 0.9);
      transition: all 0.2s ease;
    }
    
    .view-project:hover {
      background-color: #E53935;
      transform: scale(1.05);
    }
    
    .view-project .icon {
      margin-right: 0.5rem;
    }
    
    .project-info {
      padding: 1.25rem;
    }
    
    .project-title {
      font-size: 1.25rem;
      font-weight: 600;
      margin-bottom: 0.5rem;
      color: #333;
    }
    
    .project-category {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: 20px;
      background-color: #f5f5f5;
      color: #555;
      font-size: 0.85rem;
      font-weight: 500;
    }
    
    /* Lightbox styles */
    .lightbox {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.9);
      z-index: 1000;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }
    
    .lightbox-close {
      position: absolute;
      top: 1rem;
      right: 1rem;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background-color: rgba(255, 255, 255, 0.2);
      border: none;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s ease;
      z-index: 1001;
    }
    
    .lightbox-close:hover {
      background-color: rgba(255, 255, 255, 0.3);
      transform: scale(1.1);
    }
    
    .lightbox-content {
      display: flex;
      flex-direction: column;
      max-width: 1200px;
      max-height: 90vh;
      background-color: white;
      border-radius: 8px;
      overflow: hidden;
      position: relative;
    }
    
    .lightbox-image-container {
      flex-grow: 1;
      max-height: 70vh;
      overflow: hidden;
    }
    
    .lightbox-image-container img {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }
    
    .lightbox-info {
      padding: 1.5rem;
      background-color: white;
    }
    
    .lightbox-title {
      font-size: 1.5rem;
      font-weight: 600;
      margin-bottom: 0.5rem;
      color: #333;
    }
    
    .lightbox-category {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: 20px;
      background-color: #f5f5f5;
      color: #555;
      font-size: 0.85rem;
      font-weight: 500;
      margin-bottom: 1rem;
    }
    
    .lightbox-description {
      color: #555;
      margin-bottom: 1rem;
      line-height: 1.6;
    }
    
    .lightbox-client, .lightbox-date {
      color: #777;
      font-size: 0.9rem;
      margin-bottom: 0.5rem;
    }
    
    .lightbox-controls {
      position: absolute;
      top: 50%;
      left: 0;
      right: 0;
      transform: translateY(-50%);
      display: flex;
      justify-content: space-between;
      padding: 0 1rem;
      pointer-events: none;
    }
    
    .lightbox-control {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background-color: rgba(255, 255, 255, 0.2);
      border: none;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s ease;
      pointer-events: auto;
    }
    
    .lightbox-control:hover {
      background-color: rgba(229, 57, 53, 0.8);
      transform: scale(1.1);
    }
    
    /* Responsive styles */
    @media screen and (min-width: 769px) {
      .lightbox-content {
        flex-direction: row;
        max-height: 80vh;
      }
      
      .lightbox-image-container {
        width: 60%;
        max-height: 80vh;
      }
      
      .lightbox-info {
        width: 40%;
        overflow-y: auto;
        max-height: 80vh;
      }
    }
    
    @media screen and (max-width: 768px) {
      .project-image-container {
        height: 200px;
      }
      
      .lightbox-controls {
        padding: 0 0.5rem;
      }
      
      .lightbox-control {
        width: 40px;
        height: 40px;
      }
    }
  </style>