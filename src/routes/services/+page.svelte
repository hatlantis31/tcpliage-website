<script>
  const services = [
    {
      titre: 'Couvertine',
      description: 'Fabrication de couvertines sur mesure pour la protection et finition des acrotères',
      image: '/couvertine/example.jpg',
      caracteristiques: [
        'Couvertines aluminium',
        'Protection des murs et toitures',
        'Finitions soignées',
        'Sur mesure selon vos dimensions'
      ]
    },
    {
      titre: 'Habillage',
      description: 'Solutions d\'habillage métallique pour vos façades et structures',
      image: '/habillage/example.jpg',
      caracteristiques: [
        'Habillage de façades',
        'Bardage métallique',
        'Revêtements personnalisés',
        'Différentes finitions disponibles'
      ]
    },
    {
      titre: 'Matière',
      description: 'Large gamme de matériaux disponibles pour vos projets',
      image: '/matiere/example.jpg',
      caracteristiques: [
        'Aluminium',
        'Acier galvanisé',
        'Acier laqué',
        'Zinc'
      ]
    },
    {
      titre: 'Quincaillerie',
      description: 'Fabrication de pièces de quincaillerie sur mesure',
      image: '/quincaillerie/example.jpg',
      caracteristiques: [
        'Fixations spéciales',
        'Supports métalliques',
        'Pièces techniques',
        'Accessoires sur mesure'
      ]
    },
    {
      titre: 'Réalisation',
      description: 'Réalisation de projets métalliques complexes et sur mesure',
      image: '/realisation/example.jpg',
      caracteristiques: [
        'Projets personnalisés',
        'Fabrication précise',
        'Installation possible',
        'Suivi de chantier'
      ]
    },
    {
      titre: 'Formes Spéciales',
      description: 'Création de formes métalliques spécifiques selon vos besoins',
      image: '/shape/example.jpg',
      caracteristiques: [
        'Pliage complexe',
        'Formes sur mesure',
        'Découpe précise',
        'Solutions adaptées'
      ]
    }
  ];
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
    {#each services as service}
      <div class="box mb-6 service-box">
        <div class="columns is-vcentered">
          <div class="column is-5">
            <figure class="image is-4by3">
              <img src={service.image} alt={service.titre}>
            </figure>
          </div>
          <div class="column is-7">
            <h3 class="title is-3">{service.titre}</h3>
            <p class="subtitle is-5">{service.description}</p>
            <div class="content">
              <ul>
                {#each service.caracteristiques as caracteristique}
                  <li>{caracteristique}</li>
                {/each}
              </ul>
            </div>
            <div class="buttons">
              <a href="/contact" class="button is-primary">Demander un Devis</a>
              <a href="/gallery/{service.titre.toLowerCase()}" class="button is-light">Voir la Galerie</a>
            </div>
          </div>
        </div>
      </div>
    {/each}
  </div>
</section>

<style>
  .service-box {
    transition: transform 0.3s ease;
    border-radius: 8px;
    overflow: hidden;
  }

  .service-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  }

  .image {
    border-radius: 4px;
    overflow: hidden;
  }

  .buttons {
    margin-top: 1.5rem;
  }
</style>
