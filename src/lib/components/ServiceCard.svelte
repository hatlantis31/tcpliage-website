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
</script>

{#if service}
  <div class="box mb-6 service-box">
    <div class="columns is-vcentered">
      <div class="column is-5">
        <figure class="image is-4by3">
          <img src={displayImage} alt={displayTitle}>
        </figure>
      </div>
      <div class="column is-7">
        <h3 class="title is-3">{displayTitle}</h3>
        <p class="subtitle is-5">{displayDescription}</p>
        <div class="content">
          <ul>
            {#each characteristics as caracteristique}
              <li>{typeof caracteristique === 'string' ? caracteristique : caracteristique.description}</li>
            {/each}
          </ul>
        </div>
        <div class="buttons">
          <a href="/contact" class="button is-primary">Demander un Devis</a>
          <a href="/gallery/{displayTitle.toLowerCase()}" class="button is-light">Voir la Galerie</a>
        </div>
      </div>
    </div>
  </div>
{:else}
  <div class="card light-theme-card">
    <div class="card-image">
      <figure class="image is-4by3">
        <img src={displayImage} alt={displayTitle}>
      </figure>
    </div>
    <div class="card-content">
      <h3 class="title is-4">{displayTitle}</h3>
      <p class="content">{displayDescription}</p>
    </div>
  </div>
{/if}

<style>
  .service-box {
    transition: transform 0.3s ease;
    border-radius: 8px;
    overflow: hidden;
    background-color: #ffffff !important;
    color: #4a4a4a !important;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  }

  .service-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  }
  
  .light-theme-card {
    background-color: #ffffff !important;
    color: #4a4a4a !important;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  }

  .image {
    border-radius: 4px;
    overflow: hidden;
  }

  .buttons {
    margin-top: 1.5rem;
  }
  
  /* Ensure text is readable */
  :global(.service-box h3, .service-box p, .service-box li) {
    color: #4a4a4a !important;
  }
  
  /* Ensure light theme for card content */
  :global(.card-content) {
    background-color: #ffffff !important;
    color: #4a4a4a !important;
  }
</style>