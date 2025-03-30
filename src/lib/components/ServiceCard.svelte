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
  
  // For animation on scroll visibility
  import { onMount } from 'svelte';
  let isVisible = false;
  
  onMount(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          isVisible = true;
          observer.disconnect();
        }
      });
    }, { threshold: 0.1 });
    
    const serviceCard = document.querySelector('.service-card');
    if (serviceCard) {
      observer.observe(serviceCard);
    }
    
    return () => {
      observer.disconnect();
    };
  });
</script>

{#if service}
  <div class="service-card" class:is-visible={isVisible}>
    <div class="columns is-vcentered">
      <div class="column is-5 image-column">
        <div class="service-image-container">
          {#if displayImage}
            <img src={displayImage} alt={displayTitle} class="service-image">
          {:else}
            <!-- Placeholder image if no image is provided -->
            <img src="/images/services/default.jpg" alt={displayTitle} class="service-image">
          {/if}
          <div class="service-overlay"></div>
        </div>
      </div>
      
      <div class="column is-7 content-column">
        <div class="service-content">
          <h3 class="service-title">{displayTitle}</h3>
          <div class="title-underline"></div>
          <p class="service-description">{displayDescription}</p>
          
          {#if characteristics && characteristics.length > 0}
            <ul class="service-features">
              {#each characteristics as characteristic}
                <li>
                  <span class="icon"><i class="fas fa-check-circle"></i></span>
                  <span>{typeof characteristic === 'string' ? characteristic : characteristic.description}</span>
                </li>
              {/each}
            </ul>
          {/if}
          
          <div class="service-actions">
            <a href="/contact?service={encodeURIComponent(displayTitle)}" class="button is-primary">Demander un Devis</a>
            <a href="/services/{displayTitle.toLowerCase().replace(/\s+/g, '-')}" class="button is-light">En savoir plus</a>
          </div>
        </div>
      </div>
    </div>
  </div>
{:else}
  <!-- Simple card version -->
  <div class="card simple-service-card" class:is-visible={isVisible}>
    <div class="card-image">
      {#if displayImage}
        <img src={displayImage} alt={displayTitle}>
      {:else}
        <img src="/images/services/default.jpg" alt={displayTitle}>
      {/if}
      <div class="card-overlay"></div>
    </div>
    <div class="card-content">
      <h3 class="card-title">{displayTitle}</h3>
      <div class="title-underline small"></div>
      <p class="card-description">{displayDescription}</p>
      <a href="/services/{displayTitle.toLowerCase().replace(/\s+/g, '-')}" class="card-link">
        <span>En savoir plus</span>
        <span class="icon"><i class="fas fa-arrow-right"></i></span>
      </a>
    </div>
  </div>
{/if}

<style>
  /* Main service card */
  .service-card {
    background: linear-gradient(135deg, var(--bg-white), var(--bg-light));
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-md);
    margin-bottom: 3rem;
    transform: translateY(30px);
    opacity: 0;
    transition: all 0.5s ease;
    border-left: 4px solid var(--primary);
  }
  
  .service-card.is-visible {
    transform: translateY(0);
    opacity: 1;
  }
  
  .service-card:hover {
    box-shadow: var(--shadow-lg);
  }
  
  .service-image-container {
    position: relative;
    height: 100%;
    min-height: 300px;
    overflow: hidden;
    border-radius: var(--radius-md);
  }
  
  .service-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
  }
  
  .service-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to right, rgba(46, 64, 87, 0.7), rgba(171, 0, 13, 0.4));
    opacity: 0.3;
    transition: opacity 0.3s ease;
  }
  
  .service-image-container:hover .service-image {
    transform: scale(1.05);
  }
  
  .service-image-container:hover .service-overlay {
    opacity: 0.3;
  }
  
  .service-content {
    padding: 2rem;
  }
  
  .service-title {
    font-size: 2rem;
    font-weight: 700;
    color: var(--dark);
    margin-bottom: 1rem;
  }
  
  .title-underline {
    height: 4px;
    width: 60px;
    background-color: var(--primary);
    margin-bottom: 1.5rem;
  }
  
  .title-underline.small {
    width: 40px;
    height: 3px;
  }
  
  .service-description {
    color: var(--text-light);
    margin-bottom: 1.5rem;
    font-size: 1.1rem;
    line-height: 1.6;
  }
  
  .service-features {
    list-style: none;
    padding: 0;
    margin: 0 0 2rem;
  }
  
  .service-features li {
    display: flex;
    align-items: flex-start;
    margin-bottom: 0.75rem;
    font-weight: 500;
    background-color: rgba(229, 57, 53, 0.08);
    padding: 0.5rem 1rem;
    border-radius: var(--radius-md);
    margin-bottom: 0.5rem;
  }
  
  .service-features li .icon {
    color: var(--primary);
    margin-right: 0.75rem;
    flex-shrink: 0;
  }
  
  .service-actions {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
  }
  
  .service-actions .button {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
  
  /* Simple card version */
  .simple-service-card {
    height: 100%;
    transform: translateY(30px);
    opacity: 0;
    transition: all 0.5s ease;
    background: linear-gradient(to bottom, var(--bg-white) 70%, var(--bg-primary-subtle) 100%);
    border-top: 3px solid var(--primary);
  }
  
  .simple-service-card.is-visible {
    transform: translateY(0);
    opacity: 1;
  }
  
  .simple-service-card .card-image {
    position: relative;
    overflow: hidden;
    height: 200px;
  }
  
  .simple-service-card .card-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
  }
  
  .simple-service-card:hover .card-image img {
    transform: scale(1.08);
  }
  
  .card-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to top, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0) 60%);
  }
  
  .simple-service-card .card-content {
    padding: 1.5rem;
    position: relative;
  }
  
  .simple-service-card .card-title {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    color: var(--dark);
  }
  
  .simple-service-card .card-description {
    color: var(--text-light);
    margin-bottom: 1.5rem;
    line-height: 1.5;
  }
  
  .card-link {
    display: inline-flex;
    align-items: center;
    color: var(--primary);
    font-weight: 600;
    transition: all 0.3s ease;
  }
  
  .card-link .icon {
    margin-left: 0.5rem;
    transition: transform 0.3s ease;
  }
  
  .card-link:hover {
    color: var(--primary-dark);
  }
  
  .card-link:hover .icon {
    transform: translateX(3px);
  }
  
  /* Responsive Adjustments */
  @media screen and (max-width: 768px) {
    .service-card .columns {
      flex-direction: column;
    }
    
    .service-image-container {
      min-height: 200px;
    }
    
    .service-title {
      font-size: 1.75rem;
    }
    
    .service-content {
      padding: 1.5rem;
    }
    
    .image-column {
      order: 1;
    }
    
    .content-column {
      order: 2;
    }
  }
</style>