<!-- ServiceCard.svelte -->
<script>
  // Accept both old and new prop formats
  export let service = null;
  export let title = null;
  export let image = null;
  export let description = null;

  // Use service object if provided, otherwise use individual props
  $: displayTitle = service ? service.titre : title;
  $: displayImage = service ? service.image : image;
  $: displayDescription = service ? service.description : description;
  $: characteristics = service ? service.caracteristiques : [];
  
  // Format gallery link from title
  $: galleryLink = displayTitle ? `/gallery/${displayTitle.toLowerCase().replace(/\s+/g, '-')}` : '';
  
  // Check if image exists, otherwise use a placeholder
  function handleImageError(event) {
    event.target.src = 'https://via.placeholder.com/600x400?text=TC+PLIAGE';
  }
</script>

{#if service}
  <!-- Full service card with characteristics -->
  <div class="service-card-container">
    <div class="service-card">
      <div class="columns is-vcentered">
        <div class="column is-5">
          <div class="card-image-container">
            <figure class="image is-16by9">
              <img 
                src={displayImage} 
                alt={displayTitle}
                on:error={handleImageError}
                loading="lazy"
              >
            </figure>
            <div class="image-overlay"></div>
          </div>
        </div>
        <div class="column is-7">
          <div class="card-content">
            <h3 class="title is-3 service-title">{displayTitle}</h3>
            <div class="title-underline"></div>
            <p class="subtitle is-5 service-description">{displayDescription}</p>
            
            {#if characteristics && characteristics.length > 0}
              <div class="characteristics-list">
                <h4 class="title is-6 mb-2">Caractéristiques :</h4>
                <ul>
                  {#each characteristics as caracteristique}
                    <li>
                      <span class="icon has-text-danger">
                        <i class="fas fa-check-circle"></i>
                      </span>
                      <span>{typeof caracteristique === 'string' ? caracteristique : caracteristique.description}</span>
                    </li>
                  {/each}
                </ul>
              </div>
            {/if}
            
            <div class="buttons action-buttons">
              <a href="/contact" class="button is-danger">
                <span class="icon">
                  <i class="fas fa-file-alt"></i>
                </span>
                <span>Demander un Devis</span>
              </a>
              <a href={galleryLink} class="button is-outlined is-dark">
                <span class="icon">
                  <i class="fas fa-images"></i>
                </span>
                <span>Voir la Galerie</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
{:else}
  <!-- Compact service card for highlights -->
  <div class="compact-service-card">
    <div class="card-image-container">
      <figure class="image is-16by9">
        <img 
          src={displayImage} 
          alt={displayTitle}
          on:error={handleImageError}
          loading="lazy"
        >
      </figure>
      <div class="image-overlay"></div>
    </div>
    <div class="card-content">
      <h3 class="title is-4">{displayTitle}</h3>
      <div class="title-underline small"></div>
      <p class="content">{displayDescription}</p>
      <a href="/services" class="card-link">
        <span>En savoir plus</span>
        <span class="icon">
          <i class="fas fa-arrow-right"></i>
        </span>
      </a>
    </div>
  </div>
{/if}

<style>
  /* Full Service Card Styles */
  .service-card-container {
    margin-bottom: 2rem;
  }
  
  .service-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    overflow: hidden;
    transition: all 0.3s ease;
  }
  
  .service-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.15);
  }
  
  .card-image-container {
    position: relative;
    overflow: hidden;
    border-radius: 8px;
  }
  
  .card-image-container img {
    transition: transform 0.5s ease;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .service-card:hover .card-image-container img {
    transform: scale(1.05);
  }
  
  .image-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.3));
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  .service-card:hover .image-overlay {
    opacity: 1;
  }
  
  .card-content {
    padding: 1.5rem 1rem 1.5rem 0;
  }
  
  .service-title {
    color: #333;
    position: relative;
    display: inline-block;
    margin-bottom: 0.75rem;
  }
  
  .title-underline {
    width: 50px;
    height: 3px;
    background-color: #E53935;
    margin-bottom: 1.25rem;
  }
  
  .title-underline.small {
    width: 40px;
    height: 2px;
  }
  
  .service-description {
    color: #555;
    margin-bottom: 1.5rem;
  }
  
  .characteristics-list {
    margin-bottom: 1.5rem;
  }
  
  .characteristics-list ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .characteristics-list li {
    display: flex;
    align-items: flex-start;
    margin-bottom: 0.5rem;
    color: #555;
  }
  
  .characteristics-list .icon {
    margin-right: 0.5rem;
    margin-top: 0.25rem;
  }
  
  .action-buttons {
    margin-top: auto;
  }
  
  /* Compact Card Styles */
  .compact-service-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    height: 100%;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    transition: all 0.3s ease;
  }
  
  .compact-service-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 25px rgba(0,0,0,0.15);
  }
  
  .compact-service-card .card-content {
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
  }
  
  .compact-service-card h3 {
    margin-bottom: 0.75rem;
  }
  
  .compact-service-card .content {
    color: #555;
    flex-grow: 1;
    margin-bottom: 1rem;
  }
  
  .card-link {
    display: flex;
    align-items: center;
    color: #E53935;
    font-weight: 600;
    margin-top: auto;
    transition: all 0.2s ease;
  }
  
  .card-link:hover {
    color: #c62828;
  }
  
  .card-link .icon {
    margin-left: 0.5rem;
    transition: transform 0.2s ease;
  }
  
  .card-link:hover .icon {
    transform: translateX(3px);
  }
  
  /* Responsive adjustments */
  @media screen and (max-width: 768px) {
    .service-card .columns {
      display: block;
    }
    
    .service-card .column {
      width: 100%;
    }
    
    .card-content {
      padding: 1.5rem;
    }
  }
</style>