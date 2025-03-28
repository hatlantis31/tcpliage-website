<script>
  import ContactForm from '$lib/components/ContactForm.svelte';
  import { onMount } from 'svelte';
  
  let mapLoaded = false;
  let activeTab = 'form';
  
  // Office hours
  const officeHours = [
    { day: 'Lundi', hours: '5h - 19h' },
    { day: 'Mardi', hours: '5h - 19h' },
    { day: 'Mercredi', hours: '5h - 19h' },
    { day: 'Jeudi', hours: '5h - 19h' },
    { day: 'Vendredi', hours: '5h - 19h' },
    { day: 'Samedi', hours: 'Sur rendez-vous' },
    { day: 'Dimanche', hours: 'Fermé (urgences uniquement)' }
  ];
  
  onMount(() => {
    // If you have a Google Maps API key, you can initialize the map here
    setTimeout(() => {
      mapLoaded = true;
    }, 1000);
  });
  
  function setActiveTab(tab) {
    activeTab = tab;
  }
</script>

<section class="section contact-hero">
  <div class="container">
    <div class="content has-text-centered">
      <h1 class="title is-1 has-text-white">Contactez-nous</h1>
      <p class="subtitle is-4 has-text-white">Notre équipe est à votre écoute pour répondre à vos besoins</p>
    </div>
  </div>
</section>

<section class="section contact-options">
  <div class="container">
    <div class="columns is-multiline">
      <!-- Card 1: Emergency Contact -->
      <div class="column is-4-desktop is-6-tablet">
        <div class="contact-card emergency">
          <div class="card-icon">
            <span class="icon is-large">
              <i class="fas fa-phone-alt fa-2x"></i>
            </span>
          </div>
          <h3 class="title is-4">Service d'Urgence</h3>
          <p>Disponible 24h/24 et 7j/7 pour tous vos besoins urgents de fabrication métallique.</p>
          <a href="tel:emergency-number" class="button is-danger is-fullwidth">
            <span class="icon">
              <i class="fas fa-phone"></i>
            </span>
            <span>01 23 45 67 90</span>
          </a>
        </div>
      </div>
      
      <!-- Card 2: Email Contact -->
      <div class="column is-4-desktop is-6-tablet">
        <div class="contact-card email">
          <div class="card-icon">
            <span class="icon is-large">
              <i class="fas fa-envelope fa-2x"></i>
            </span>
          </div>
          <h3 class="title is-4">Email & Devis</h3>
          <p>Pour les demandes de devis et renseignements généraux sur nos services.</p>
          <a href="mailto:contact@tcpliage.fr" class="button is-primary is-fullwidth">
            <span class="icon">
              <i class="fas fa-envelope"></i>
            </span>
            <span>contact@tcpliage.fr</span>
          </a>
        </div>
      </div>
      
      <!-- Card 3: Visit Us -->
      <div class="column is-4-desktop is-6-tablet">
        <div class="contact-card visit">
          <div class="card-icon">
            <span class="icon is-large">
              <i class="fas fa-map-marker-alt fa-2x"></i>
            </span>
          </div>
          <h3 class="title is-4">Visitez Notre Atelier</h3>
          <p>Venez nous rencontrer directement à notre atelier de fabrication à Portet-Sur-Garonne.</p>
          <a 
            href="https://maps.google.com?q=3+Avenue+du+Bois+Vert,+Portet-Sur-Garonne" 
            target="_blank" 
            class="button is-info is-fullwidth"
          >
            <span class="icon">
              <i class="fas fa-directions"></i>
            </span>
            <span>Itinéraire</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section contact-main">
  <div class="container">
    <div class="tabs is-centered is-boxed is-medium">
      <ul>
        <li class={activeTab === 'form' ? 'is-active' : ''}>
          <a on:click|preventDefault={() => setActiveTab('form')}>
            <span class="icon"><i class="fas fa-paper-plane"></i></span>
            <span>Formulaire de Contact</span>
          </a>
        </li>
        <li class={activeTab === 'info' ? 'is-active' : ''}>
          <a on:click|preventDefault={() => setActiveTab('info')}>
            <span class="icon"><i class="fas fa-info-circle"></i></span>
            <span>Informations</span>
          </a>
        </li>
      </ul>
    </div>
    
    <div class="tab-content">
      {#if activeTab === 'form'}
        <div class="columns">
          <div class="column is-8 is-offset-2">
            <div class="box contact-form-container">
              <h2 class="title is-3 has-text-centered mb-5">Envoyez-nous un Message</h2>
              <ContactForm />
            </div>
          </div>
        </div>
      {:else}
        <div class="columns">
          <div class="column is-6">
            <div class="box info-box">
              <h3 class="title is-4">Coordonnées</h3>
              <div class="contact-details">
                <div class="contact-detail">
                  <span class="icon has-text-danger">
                    <i class="fas fa-map-marker-alt"></i>
                  </span>
                  <div>
                    <strong>Adresse:</strong><br>
                    3 Avenue du Bois Vert<br>
                    Portet-Sur-Garonne, France
                  </div>
                </div>
                
                <div class="contact-detail">
                  <span class="icon has-text-danger">
                    <i class="fas fa-phone"></i>
                  </span>
                  <div>
                    <strong>Téléphone:</strong><br>
                    Standard: <a href="tel:standard-number">01 23 45 67 89</a><br>
                    Urgence: <a href="tel:emergency-number">01 23 45 67 90</a>
                  </div>
                </div>
                
                <div class="contact-detail">
                  <span class="icon has-text-danger">
                    <i class="fas fa-envelope"></i>
                  </span>
                  <div>
                    <strong>Email:</strong><br>
                    <a href="mailto:contact@tcpliage.fr">contact@tcpliage.fr</a>
                  </div>
                </div>
              </div>
              
              <h3 class="title is-4 mt-5">Horaires d'Ouverture</h3>
              <table class="table is-fullwidth opening-hours">
                <tbody>
                  {#each officeHours as { day, hours }}
                    <tr>
                      <td>{day}</td>
                      <td class="has-text-right">{hours}</td>
                    </tr>
                  {/each}
                </tbody>
              </table>
              
              <div class="notification is-warning is-light mt-4">
                <p class="has-text-weight-medium">
                  <span class="icon has-text-warning">
                    <i class="fas fa-exclamation-triangle"></i>
                  </span>
                  Notre service d'urgence est disponible 24h/24 et 7j/7 en dehors des heures d'ouverture.
                </p>
              </div>
            </div>
          </div>
          <div class="column is-6">
            <div class="box map-container">
              <h3 class="title is-4">Notre Localisation</h3>
              <div class="map-wrapper">
                {#if mapLoaded}
                  <iframe
                    width="100%"
                    height="400"
                    style="border:0"
                    loading="lazy"
                    allowfullscreen
                    referrerpolicy="no-referrer-when-downgrade"
                    src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2889.9371526429886!2d1.4033!3d43.5356!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x12aebb7baf3310a3%3A0x1d4f860e16ef5296!2s3%20Av.%20du%20Bois%20Vert%2C%2031120%20Portet-sur-Garonne!5e0!3m2!1sfr!2sfr!4v1650000000000!5m2!1sfr!2sfr"
                  >
                  </iframe>
                {:else}
                  <div class="map-loading">
                    <span class="icon is-large">
                      <i class="fas fa-spinner fa-pulse fa-2x"></i>
                    </span>
                    <p>Chargement de la carte...</p>
                  </div>
                {/if}
              </div>
              
              <div class="buttons is-centered mt-4">
                <a 
                  href="https://maps.google.com?q=3+Avenue+du+Bois+Vert,+Portet-Sur-Garonne" 
                  target="_blank" 
                  class="button is-info"
                >
                  <span class="icon">
                    <i class="fas fa-directions"></i>
                  </span>
                  <span>Itinéraire</span>
                </a>
                <a href="tel:standard-number" class="button is-primary">
                  <span class="icon">
                    <i class="fas fa-phone"></i>
                  </span>
                  <span>Appeler</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      {/if}
    </div>
  </div>
</section>

<section class="section faq-section">
  <div class="container">
    <h2 class="title is-2 has-text-centered">Questions Fréquentes</h2>
    <div class="columns is-multiline">
      <div class="column is-6">
        <div class="faq-item">
          <h3 class="title is-5">Quel est votre délai de fabrication en urgence ?</h3>
          <p>Pour les commandes urgentes, nous garantissons une fabrication en 24h. Notre équipe est mobilisée pour traiter les demandes d'urgence en priorité.</p>
        </div>
      </div>
      <div class="column is-6">
        <div class="faq-item">
          <h3 class="title is-5">Quels types de métaux travaillez-vous ?</h3>
          <p>Nous travaillons principalement l'acier, l'aluminium, l'inox et le cuivre. Nos machines sont adaptées pour tous types d'épaisseurs selon vos besoins.</p>
        </div>
      </div>
      <div class="column is-6">
        <div class="faq-item">
          <h3 class="title is-5">Comment obtenir un devis ?</h3>
          <p>Vous pouvez obtenir un devis en nous contactant par téléphone, email ou en utilisant notre formulaire de contact en ligne. Pour les pièces complexes, notre outil de dessin en ligne est disponible.</p>
        </div>
      </div>
      <div class="column is-6">
        <div class="faq-item">
          <h3 class="title is-5">Livrez-vous dans toute la France ?</h3>
          <p>Oui, nous livrons dans toute la France. Pour les commandes urgentes, nous proposons un service de livraison express pour garantir la réception de vos pièces dans les plus brefs délais.</p>
        </div>
      </div>
    </div>
    
    <div class="has-text-centered mt-6">
      <p class="subtitle is-5">Vous avez d'autres questions ?</p>
      <a href="tel:standard-number" class="button is-medium is-danger">
        <span class="icon">
          <i class="fas fa-phone"></i>
        </span>
        <span>Contactez-nous directement</span>
      </a>
    </div>
  </div>
</section>

<style>
  /* Hero Section */
  .contact-hero {
    background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('/contact-hero.jpg');
    background-size: cover;
    background-position: center;
    padding: 6rem 1.5rem;
    margin-bottom: 0;
  }
  
  /* Contact Options Cards */
  .contact-options {
    padding-bottom: 0;
  }
  
  .contact-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
    padding: 2rem;
    text-align: center;
    height: 100%;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  
  .contact-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  }
  
  .contact-card.emergency {
    border-top: 4px solid #E53935;
  }
  
  .contact-card.email {
    border-top: 4px solid #00897B;
  }
  
  .contact-card.visit {
    border-top: 4px solid #1E88E5;
  }
  
  .card-icon {
    margin-bottom: 1.5rem;
    color: #555;
  }
  
  .contact-card h3 {
    margin-bottom: 1rem;
  }
  
  .contact-card p {
    color: #666;
    margin-bottom: 1.5rem;
    flex-grow: 1;
  }
  
  /* Tabs Styling */
  .tabs.is-boxed li.is-active a {
    border-color: #E53935;
    color: #E53935;
  }
  
  .tabs a {
    transition: all 0.2s ease;
  }
  
  .tab-content {
    padding: 2rem 0;
  }
  
  /* Contact Form Container */
  .contact-form-container {
    padding: 2rem;
    border-radius: 8px;
    background-color: white;
  }
  
  /* Contact Information */
  .info-box {
    height: 100%;
  }
  
  .contact-details {
    margin: 2rem 0;
  }
  
  .contact-detail {
    display: flex;
    margin-bottom: 1.5rem;
  }
  
  .contact-detail .icon {
    margin-right: 1rem;
    margin-top: 5px;
  }
  
  .opening-hours tr {
    border-bottom: 1px solid #f0f0f0;
  }
  
  .opening-hours tr:last-child {
    border-bottom: none;
  }
  
  /* Map Container */
  .map-container {
    height: 100%;
  }
  
  .map-wrapper {
    position: relative;
    width: 100%;
    height: 400px;
    border-radius: 6px;
    overflow: hidden;
    margin-bottom: 1.5rem;
  }
  
  .map-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    background-color: #f5f5f5;
  }
  
  /* FAQ Section */
  .faq-section {
    background-color: #f9f9f9;
    padding: 5rem 1.5rem;
  }
  
  .faq-item {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
    height: 100%;
    transition: all 0.3s ease;
  }
  
  .faq-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  }
  
  .faq-item h3 {
    margin-bottom: 1rem;
    color: #333;
  }
  
  .faq-item p {
    color: #666;
  }
  
  /* Responsive adjustments */
  @media screen and (max-width: 768px) {
    .contact-hero {
      padding: 4rem 1.5rem;
    }
    
    .contact-detail {
      flex-direction: column;
    }
    
    .contact-detail .icon {
      margin-bottom: 0.5rem;
    }
    
    .map-wrapper {
      height: 300px;
    }
  }
</style>