<script>
  import ServiceCard from '$lib/components/ServiceCard.svelte';
  import { onMount } from 'svelte';

  let currentSlide = 0;
  const slides = [
    '/home/slider/bandeau1.jpeg',
    '/home/slider/bandeau2.jpeg',
    '/home/slider/bandeau3.jpeg',
    '/home/slider/bandeau4.jpeg'
  ];

  function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
  }

  onMount(() => {
    const interval = setInterval(nextSlide, 5000); // Change slide every 5 seconds
    return () => clearInterval(interval);
  });
</script>

<!-- Hero Section avec Diaporama -->
<section class="hero is-medium">
  <div class="hero-background">
    {#each slides as slide, i}
      <div 
        class="hero-background-image" 
        style="background-image: url({slide}); 
               opacity: {currentSlide === i ? 1 : 0};
               transition: opacity 1s ease-in-out;"
      ></div>
    {/each}
    <div class="hero-overlay"></div>
  </div>
  <div class="hero-body">
    <div class="container">
      <h1 class="title is-1 has-text-white">
        TCPliage
      </h1>
      <h2 class="subtitle has-text-white">
        Fabrication de Pièces Métalliques en Urgence pour Chantiers
      </h2>
    </div>
  </div>
</section>

<!-- Présentation Section -->
<section class="section has-background-light">
  <div class="container">
    <div class="columns is-vcentered">
      <div class="column is-7 content">
        <h2 class="title is-2">Notre Expertise à Votre Service</h2>
        <p class="is-size-5">
          <strong>TC PLIAGE</strong>, votre partenaire métallurgique de confiance à Portet-Sur-Garonne, 
          met son savoir-faire à votre disposition. Installés au 3 Avenue du Bois Vert, nous concrétisons 
          vos projets métalliques avec passion et précision.
        </p>
        <p>
          Fort d'une expertise forgée depuis 1988 dans l'industrie métallique, notre PME familiale, 
          créée en 2016, s'appuie sur des décennies d'expérience pour vous offrir un service personnalisé 
          et des solutions adaptées.
        </p>
        <p>
          Que vous soyez professionnel ou particulier, nous vous accueillons dans notre atelier pour 
          étudier ensemble votre projet et définir la meilleure approche pour sa réalisation.
        </p>
      </div>
      <div class="column is-5">
        <div class="has-ratio" style="position: relative; padding-top: 56.25%;">
          <iframe
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
            src="https://www.youtube.com/embed/NkkO462toNs"
            title="Présentation TC PLIAGE"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          ></iframe>
        </div>
      </div>
    </div>
  </div>
</section>


<!-- Prestations Section -->
<section class="section">
  <div class="container">
    <h2 class="title is-2 has-text-centered mb-6">Nos Prestations</h2>
    
    <div class="columns is-multiline">
      <!-- Fabrication 24h -->
      <div class="column is-3">
        <div class="has-text-centered">
          <div class="mb-4">
            <figure class="image is-96x96 is-inline-block">
              <div class="has-background-danger-light is-flex is-justify-content-center is-align-items-center" style="border-radius: 50%; width: 100%; height: 100%;">
                <span class="is-size-3 has-text-danger has-text-weight-bold">24H</span>
              </div>
            </figure>
          </div>
          <h3 class="title is-4">Fabrication Express</h3>
          <p>
            Notre priorité est votre satisfaction. Délais imposés ou urgence de chantier, 
            nous réalisons vos pliages en 24 heures.
          </p>
        </div>
      </div>

      <!-- Horaires -->
      <div class="column is-3">
        <div class="has-text-centered">
          <div class="mb-4">
            <figure class="image is-96x96 is-inline-block">
              <div class="has-background-info-light is-flex is-justify-content-center is-align-items-center" style="border-radius: 50%; width: 100%; height: 100%;">
                <span class="is-size-4 has-text-info has-text-weight-bold">5H-19H</span>
              </div>
            </figure>
          </div>
          <h3 class="title is-4">Production Continue</h3>
          <p>
            Production en 2 postes, du lundi au vendredi de 5H à 19H en continu 
            pour répondre à tous vos besoins.
          </p>
        </div>
      </div>

      <!-- Service Client -->
      <div class="column is-3">
        <div class="has-text-centered">
          <div class="mb-4">
            <figure class="image is-96x96 is-inline-block">
              <div class="has-background-primary-light is-flex is-justify-content-center is-align-items-center" style="border-radius: 50%; width: 100%; height: 100%;">
                <span class="is-size-3 has-text-primary has-text-weight-bold">★</span>
              </div>
            </figure>
          </div>
          <h3 class="title is-4">Expertise & Conseil</h3>
          <p>
            Notre équipe professionnelle vous accompagne avec les meilleurs conseils 
            pour la réussite de votre projet.
          </p>
        </div>
      </div>

      <!-- Livraison -->
      <div class="column is-3">
        <div class="has-text-centered">
          <div class="mb-4">
            <figure class="image is-96x96 is-inline-block">
              <div class="has-background-warning-light is-flex is-justify-content-center is-align-items-center" style="border-radius: 50%; width: 100%; height: 100%;">
                <span class="is-size-3 has-text-warning-dark has-text-weight-bold">🚚</span>
              </div>
            </figure>
          </div>
          <h3 class="title is-4">Livraison France</h3>
          <p>
            Service de livraison disponible pour vos pliages partout en France.
          </p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Services Cards Section -->
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


<style>
  .hero {
    position: relative;
    overflow: hidden;
    min-height: 400px;
  }

  .hero-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }

  .hero-background-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
  }

  .hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5); /* Assombrit légèrement l'image */
  }

  .hero-body {
    position: relative;
    z-index: 1;
  }

  .title, .subtitle {
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); /* Améliore la lisibilité */
  }
</style>