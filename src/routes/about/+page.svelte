<script>
  import { onMount } from 'svelte';
  
  // Company timeline
  const timelineEvents = [
    {
      year: 1988,
      title: "Débuts dans l'Industrie Métallique",
      description: "Notre fondateur commence sa carrière dans l'industrie de la métallurgie, acquérant une solide expérience technique."
    },
    {
      year: 2016,
      title: "Création de TC PLIAGE",
      description: "Fondation de notre entreprise familiale spécialisée dans la fabrication de pièces métalliques à Portet-Sur-Garonne."
    },
    {
      year: 2018,
      title: "Développement du Service d'Urgence",
      description: "Mise en place de notre service de fabrication express 24h/24 pour répondre aux besoins urgents des chantiers."
    },
    {
      year: 2020,
      title: "Acquisition d'Équipements Dernière Génération",
      description: "Investissement dans des machines à commande numérique pour augmenter notre précision et notre capacité de production."
    },
    {
      year: 2023,
      title: "Extension de l'Atelier",
      description: "Agrandissement de nos installations pour mieux répondre à la demande croissante et améliorer nos délais de production."
    }
  ];
  
  // Team members
  const teamMembers = [
    {
      name: "Thomas Durand",
      position: "Fondateur & Directeur",
      bio: "Fort de plus de 30 ans d'expérience dans l'industrie métallique, Thomas a fondé TC PLIAGE avec la vision d'offrir un service réactif et de qualité.",
      image: "/team/director.jpg"
    },
    {
      name: "Sophie Martin",
      position: "Responsable Production",
      bio: "Sophie supervise tous les aspects de la production, garantissant la qualité et le respect des délais pour chaque commande.",
      image: "/team/production.jpg"
    },
    {
      name: "Jean Leclerc",
      position: "Expert Technique",
      bio: "Jean apporte son expertise technique pour résoudre les défis les plus complexes et assurer la faisabilité de chaque projet.",
      image: "/team/technical.jpg"
    },
    {
      name: "Marie Dubois",
      position: "Service Client",
      bio: "Marie est le premier point de contact pour nos clients, coordonnant les demandes et assurant un suivi personnalisé.",
      image: "/team/customer-service.jpg"
    }
  ];
  
  // Values
  const values = [
    {
      title: "Réactivité",
      description: "Nous nous engageons à répondre rapidement à vos besoins, particulièrement dans les situations d'urgence.",
      icon: "bolt"
    },
    {
      title: "Excellence",
      description: "La qualité et la précision sont au cœur de notre travail, dans chaque pièce que nous fabriquons.",
      icon: "award"
    },
    {
      title: "Innovation",
      description: "Nous investissons continuellement dans les technologies et techniques les plus récentes.",
      icon: "lightbulb"
    },
    {
      title: "Proximité",
      description: "Nous cultivons des relations de confiance avec nos clients pour mieux comprendre et satisfaire leurs besoins.",
      icon: "handshake"
    }
  ];
  
  // Gallery images
  const galleryImages = [
    "/gallery/workshop1.jpg",
    "/gallery/production1.jpg",
    "/gallery/machine1.jpg",
    "/gallery/team1.jpg",
    "/gallery/product1.jpg",
    "/gallery/workshop2.jpg"
  ];
  
  // Counter for animation
  let counters = {
    years: 0,
    clients: 0,
    projects: 0,
    team: 0
  };
  
  // Target values for counters
  const targetCounters = {
    years: 7,
    clients: 500,
    projects: 2000,
    team: 12
  };
  
  onMount(() => {
    // Animate counters
    const duration = 2000;
    const step = 20;
    
    for (const key in targetCounters) {
      const target = targetCounters[key];
      const increment = target / (duration / step);
      
      let current = 0;
      const interval = setInterval(() => {
        current += increment;
        if (current >= target) {
          current = target;
          clearInterval(interval);
        }
        counters[key] = Math.floor(current);
      }, step);
    }
  });
</script>

<!-- Hero Section -->
<section class="hero is-medium">
  <div class="hero-body">
    <div class="container">
      <div class="columns is-vcentered">
        <div class="column is-6">
          <h1 class="title is-1 hero-title">
            À Propos de<br>
            <span class="company-name">TC<span class="has-text-danger">PLIAGE</span></span>
          </h1>
          <div class="subtitle-line"></div>
          <p class="hero-description mb-5">
            Votre partenaire de confiance pour la fabrication métallique d'urgence. 
            Depuis 2016, notre équipe met son expertise au service de vos projets 
            les plus exigeants, avec une réactivité et une qualité constantes.
          </p>
          <div class="buttons">
            <a href="#our-story" class="button is-danger is-medium">
              <span>Notre Histoire</span>
              <span class="icon">
                <i class="fas fa-chevron-down"></i>
              </span>
            </a>
            <a href="/contact" class="button is-outlined is-medium">
              <span>Nous Contacter</span>
            </a>
          </div>
        </div>
        <div class="column is-6">
          <figure class="image about-image-container">
            <img src="/about/company-photo.jpg" alt="TC PLIAGE atelier" class="about-image">
          </figure>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Stats Banner -->
<section class="section stats-banner">
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-3-desktop is-6-tablet">
        <div class="stat-item">
          <div class="stat-number">+<span class="counter">{counters.years}</span></div>
          <div class="stat-label">Années d'Expérience</div>
        </div>
      </div>
      <div class="column is-3-desktop is-6-tablet">
        <div class="stat-item">
          <div class="stat-number">+<span class="counter">{counters.clients}</span></div>
          <div class="stat-label">Clients Satisfaits</div>
        </div>
      </div>
      <div class="column is-3-desktop is-6-tablet">
        <div class="stat-item">
          <div class="stat-number">+<span class="counter">{counters.projects}</span></div>
          <div class="stat-label">Projets Réalisés</div>
        </div>
      </div>
      <div class="column is-3-desktop is-6-tablet">
        <div class="stat-item">
          <div class="stat-number"><span class="counter">{counters.team}</span></div>
          <div class="stat-label">Membres d'Équipe</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Our Story Section -->
<section class="section our-story" id="our-story">
  <div class="container">
    <div class="columns">
      <div class="column is-10 is-offset-1">
        <h2 class="title is-2 has-text-centered section-title">Notre Histoire</h2>
        <div class="subtitle-line centered"></div>
        <p class="section-subtitle has-text-centered">
          Un parcours marqué par la passion du métal et l'excellence technique
        </p>
        
        <div class="timeline mt-6">
          {#each timelineEvents as event, index}
            <div class="timeline-item">
              <div class="timeline-year">
                <span>{event.year}</span>
              </div>
              <div class="timeline-content">
                <h3 class="title is-4">{event.title}</h3>
                <p>{event.description}</p>
              </div>
            </div>
          {/each}
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Values Section -->
<section class="section values-section">
  <div class="container">
    <h2 class="title is-2 has-text-centered section-title">Nos Valeurs</h2>
    <div class="subtitle-line centered"></div>
    <p class="section-subtitle has-text-centered">
      Les principes qui guident nos actions au quotidien
    </p>
    
    <div class="columns is-multiline mt-6">
      {#each values as value}
        <div class="column is-3-desktop is-6-tablet">
          <div class="value-card">
            <div class="value-icon">
              <span class="icon">
                <i class="fas fa-{value.icon}"></i>
              </span>
            </div>
            <h3 class="title is-4">{value.title}</h3>
            <p>{value.description}</p>
          </div>
        </div>
      {/each}
    </div>
  </div>
</section>

<!-- Mission Section -->
<section class="section mission-section">
  <div class="container">
    <div class="columns is-vcentered">
      <div class="column is-6">
        <h2 class="title is-2 section-title">Notre Mission</h2>
        <div class="subtitle-line"></div>
        <p class="section-subtitle">
          Conjuguer réactivité et qualité pour vos projets métalliques
        </p>
        
        <div class="content mission-content">
          <p>
            La mission de TC PLIAGE est d'offrir des solutions de fabrication métallique 
            réactives et de haute qualité, répondant aux besoins urgents des professionnels 
            du bâtiment et de l'industrie.
          </p>
          <p>
            Nous nous engageons à:
          </p>
          <ul>
            <li><strong>Répondre aux urgences</strong> avec un service disponible 24h/24 et 7j/7</li>
            <li><strong>Garantir la qualité</strong> de chaque pièce sortant de notre atelier</li>
            <li><strong>Adapter nos services</strong> aux exigences spécifiques de chaque projet</li>
            <li><strong>Innover constamment</strong> pour améliorer nos processus et nos produits</li>
          </ul>
          <p>
            Cette mission guide chacune de nos actions et nous pousse à constamment élever 
            nos standards pour satisfaire et dépasser les attentes de nos clients.
          </p>
        </div>
      </div>
      <div class="column is-6">
        <figure class="image mission-image-container">
          <img src="/about/mission-image.jpg" alt="Notre mission" class="mission-image">
        </figure>
      </div>
    </div>
  </div>
</section>

<!-- Team Section -->
<section class="section team-section">
  <div class="container">
    <h2 class="title is-2 has-text-centered section-title">Notre Équipe</h2>
    <div class="subtitle-line centered"></div>
    <p class="section-subtitle has-text-centered">
      Des professionnels passionnés à votre service
    </p>
    
    <div class="columns is-multiline mt-6">
      {#each teamMembers as member}
        <div class="column is-3-desktop is-6-tablet">
          <div class="team-card">
            <div class="team-photo-container">
              <img src={member.image} alt={member.name} class="team-photo">
              <div class="team-overlay"></div>
            </div>
            <div class="team-info">
              <h3 class="title is-4">{member.name}</h3>
              <p class="team-position">{member.position}</p>
              <p class="team-bio">{member.bio}</p>
            </div>
          </div>
        </div>
      {/each}
    </div>
  </div>
</section>

<!-- Workshop Gallery -->
<section class="section gallery-section">
  <div class="container">
    <h2 class="title is-2 has-text-centered section-title">Notre Atelier</h2>
    <div class="subtitle-line centered"></div>
    <p class="section-subtitle has-text-centered">
      Découvrez notre environnement de travail et nos équipements
    </p>
    
    <div class="columns is-multiline mt-6">
      {#each galleryImages as image, index}
        <div class="column is-4-desktop is-6-tablet">
          <div class="gallery-item">
            <a href={image} target="_blank" class="gallery-link">
              <img src={image} alt="Atelier TC PLIAGE" loading="lazy">
              <div class="gallery-overlay">
                <span class="icon">
                  <i class="fas fa-search-plus"></i>
                </span>
              </div>
            </a>
          </div>
        </div>
      {/each}
    </div>
  </div>
</section>

<!-- CTA Section -->
<section class="section cta-section">
  <div class="container">
    <div class="cta-content">
      <h2 class="title is-2 has-text-white">Prêt à Collaborer avec Nous ?</h2>
      <p class="subtitle is-4 has-text-white">
        Confiez-nous vos projets de fabrication métallique et bénéficiez de notre expertise
      </p>
      <div class="buttons is-centered mt-6">
        <a href="/contact" class="button is-danger is-large">
          <span>Contactez-nous</span>
          <span class="icon">
            <i class="fas fa-arrow-right"></i>
          </span>
        </a>
        <a href="/services" class="button is-white is-outlined is-large">
          <span>Découvrir nos Services</span>
        </a>
      </div>
    </div>
  </div>
</section>

<style>
  /* Hero Section */
 
</style>