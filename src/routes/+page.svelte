<script>
  import ServiceCard from '$lib/components/ServiceCard.svelte';
</script>

<section class="hero is-medium is-dark">
  <div class="hero-body">
    <div class="container">
      <h1 class="title is-1">
        TCPliage
      </h1>
      <h2 class="subtitle">
        Fabrication de Pièces Métalliques en Urgence pour Chantiers
      </h2>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-one-third">
        <ServiceCard 
          title="Fabrication d'Urgence"
          image="/home/emergency-manufacturing.jpg"
          description="Réalisation rapide pour vos besoins urgents en pièces métalliques"
        />
      </div>
      <div class="column is-one-third">
        <ServiceCard 
          title="Solutions Sur Mesure"
          image="/home/custom-solutions.jpg"
          description="Pièces métalliques adaptées à vos besoins spécifiques"
        />
      </div>
      <div class="column is-one-third">
        <ServiceCard 
          title="Garantie Qualité"
          image="/home/quality-assurance.jpg"
          description="Matériaux de haute qualité et fabrication précise"
        />
      </div>
    </div>
  </div>
</section>
