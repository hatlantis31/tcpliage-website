<script>
  const services = [
    {
      titre: 'Fabrication d\'Urgence',
      description: 'Réalisation rapide pour vos besoins urgents',
      image: '/services/emergency.jpg',
      caracteristiques: [
        'Disponibilité 24h/24 et 7j/7',
        'Temps de réponse rapide',
        'Livraison sur site'
      ]
    },
    {
      titre: 'Pièces Métalliques Sur Mesure',
      description: 'Solutions adaptées à vos exigences spécifiques',
      image: '/services/custom.jpg',
      caracteristiques: [
        'Spécifications précises',
        'Matériaux de qualité',
        'Savoir-faire expert'
      ]
    },
    // Ajoutez d'autres services selon vos besoins
  ];
</script>

<section class="hero is-medium is-dark">
  <div class="hero-body">
    <div class="container">
      <h1 class="title is-1">A propos</h1>
      <h2 class="subtitle">Solutions Professionnelles de Fabrication Métallique</h2>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    {#each services as service}
      <div class="box mb-6">
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
            <a href="/contact" class="button is-primary">Demander un Devis</a>
          </div>
        </div>
      </div>
    {/each}
  </div>
</section>
