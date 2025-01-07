<!-- +page.svelte (in services directory) -->
<script>
  import { onMount } from 'svelte';
  import ServiceCard from '$lib/components/ServiceCard.svelte';

  let services = [];
  let loading = true;
  let error = null;

  onMount(async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/services/');
      if (!response.ok) throw new Error('Failed to fetch services');
      services = await response.json();
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  });
</script>

<section class="hero is-medium is-dark">
  <div class="hero-body">
    <div class="container">
      <h1 class="title is-1">Nos Services</h1>
      <h2 class="subtitle">Solutions Professionnelles de Fabrication Métallique</h2>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    {#if loading}
      <div class="has-text-centered">
        <p>Chargement des services...</p>
      </div>
    {:else if error}
      <div class="notification is-danger">
        <p>{error}</p>
      </div>
    {:else}
      {#each services as service}
        <ServiceCard {service} />
      {/each}
    {/if}
  </div>
</section>