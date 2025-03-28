<script>
  import ContactForm from '$lib/components/ContactForm.svelte';
</script>

<section class="hero is-medium is-dark">
  <div class="hero-body">
    <div class="container">
      <h1 class="title is-1">Contactez-nous</h1>
      <h2 class="subtitle">Pour vos Besoins en Fabrication Métallique d'Urgence</h2>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="columns">
      <div class="column is-6">
        <div class="content">
          <h2 class="title is-3">Informations de Contact</h2>
          <p>
            <strong>Adresse:</strong><br>
            Votre Adresse Ici
          </p>
          <p>
            <strong>Téléphone:</strong><br>
            Standard: 01 23 45 67 89<br>
            Urgence: 01 23 45 67 90
          </p>
          <p>
            <strong>Email:</strong><br>
            contact@tcpliage.fr
          </p>
          <p>
            <strong>Horaires:</strong><br>
            Service d'Urgence Disponible 24h/24 et 7j/7
          </p>
        </div>
        
        <div class="mt-6">
          <h3 class="title is-4">Localisation</h3>
          <div class="box">
            <!-- Ajoutez votre code d'intégration Google Maps ici -->
            <iframe 
              width="100%" 
              height="300" 
              frameborder="0" 
              style="border:0" 
              src="https://www.google.com/maps/place/Tc+Pliage/@43.5589011,1.411853,17z/data=!3m1!4b1!4m6!3m5!1s0x12aeb9bf92ebcdd5:0x70377b05ec5c3a5b!8m2!3d43.5589011!4d1.411853!16s%2Fg%2F11flt355hb?entry=ttu&g_ep=EgoyMDI1MDMyNC4wIKXMDSoASAFQAw%3D%3D" 
              allowfullscreen>
            </iframe>
          </div>
        </div>
      </div>
      
      <div class="column is-6">
        <h2 class="title is-3">Envoyez-nous un Message</h2>
        <ContactForm />
      </div>
    </div>
  </div>
</section>
