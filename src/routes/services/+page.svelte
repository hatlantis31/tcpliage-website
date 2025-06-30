<script>
  import { onMount } from 'svelte';
  import ServiceCard from '$lib/components/ServiceCard.svelte';
  
  let services = [];
  let loading = true;
  let error = null;
  
  onMount(async () => {
  try {
    const response = await fetch('/api/services/');
    if (!response.ok) throw new Error('Failed to load services');
    const data = await response.json();
    
    // Extract the results array from the paginated response
    services = data.results || [];
    
    console.log("Services loaded:", services); // Add this for debugging
    loading = false;
  } catch (e) {
    error = e.message;
    loading = false;
    console.error('Error loading services:', e);
  }
});
</script>

<section class="hero is-medium is-dark">
  <div class="hero-body">
    <div class="container">
      <h1 class="title is-1">Nos Services</h1>
      <h2 class="subtitle">Solutions métalliques sur mesure pour tous vos projets</h2>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="content mb-6">
      <h2 class="title is-2 has-text-centered">Expertise Métallique à Votre Service</h2>
      <p class="subtitle has-text-centered">
        Découvrez notre gamme complète de services de fabrication métallique
      </p>
    </div>
    
    {#if loading}
      <div class="has-text-centered py-6">
        <p>Chargement des services...</p>
        <progress class="progress is-danger" max="100"></progress>
      </div>
    {:else if error}
      <div class="notification is-danger">
        <p>Erreur lors du chargement des services: {error}</p>
        <p>Veuillez réessayer ultérieurement ou nous contacter directement.</p>
      </div>
    {:else if services.length === 0}
      <div class="notification is-warning">
        <p>Aucun service disponible pour le moment.</p>
      </div>
    {:else}
      {#each services as service}
        <ServiceCard {service} />
      {/each}
    {/if}
    
    <div class="has-text-centered mt-6">
      <a href="/contact" class="button is-danger is-large">
        <span>Demander un Devis</span>
        <span class="icon">
          <i class="fas fa-arrow-right"></i>
        </span>
      </a>
    </div>
  </div>
</section>

<style>
  .hero {
    background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('/services-hero.jpg');
    background-size: cover;
    background-position: center;
  }
</style>