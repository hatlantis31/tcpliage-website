<script>
  const currentYear = new Date().getFullYear();
  
  // Animate footer elements on scroll
  import { onMount } from 'svelte';
  
  let footerVisible = false;
  
  onMount(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          footerVisible = true;
          observer.disconnect();
        }
      });
    }, { threshold: 0.2 });
    
    const footerElement = document.querySelector('.footer');
    if (footerElement) {
      observer.observe(footerElement);
    }
    
    return () => {
      observer.disconnect();
    };
  });
</script>

<footer class="footer" class:is-visible={footerVisible}>
  <div class="container">
    <div class="footer-top">
      <div class="columns is-multiline">
        <div class="column is-5">
          <div class="footer-brand animate-item">
            <img src="/logo.jpg" alt="TCPliage Logo" width="180">
            <p class="mt-4">
              TC PLIAGE, votre partenaire métallurgique de confiance depuis 2016. Notre savoir-faire et notre réactivité au service de vos projets.
            </p>
            <div class="social-links">
              <a href="#" class="social-link" aria-label="Facebook">
                <i class="fab fa-facebook-f"></i>
              </a>
              <a href="#" class="social-link" aria-label="LinkedIn">
                <i class="fab fa-linkedin-in"></i>
              </a>
              <a href="#" class="social-link" aria-label="Instagram">
                <i class="fab fa-instagram"></i>
              </a>
            </div>
          </div>
        </div>
        
        <div class="column is-2-tablet is-6-mobile">
          <div class="footer-nav animate-item">
            <h3 class="footer-title">Navigation</h3>
            <ul class="footer-links">
              <li><a href="/">Accueil</a></li>
              <li><a href="/services">Services</a></li>
              <li><a href="/about">À Propos</a></li>
              <li><a href="/designer">Dessin en ligne</a></li>
              <li><a href="/contact">Contact</a></li>
            </ul>
          </div>
        </div>
        
        <div class="column is-2-tablet is-6-mobile">
          <div class="footer-nav animate-item">
            <h3 class="footer-title">Nos Services</h3>
            <ul class="footer-links">
              <li><a href="/services">Fabrication d'Urgence</a></li>
              <li><a href="/services">Pièces Sur Mesure</a></li>
              <li><a href="/services">Couvertines</a></li>
              <li><a href="/services">Habillages Métalliques</a></li>
              <li><a href="/services">Quincaillerie</a></li>
            </ul>
          </div>
        </div>
        
        <div class="column is-3-tablet is-12-mobile">
          <div class="footer-contact animate-item">
            <h3 class="footer-title">Contact</h3>
            <ul class="contact-details">
              <li>
                <i class="fas fa-map-marker-alt"></i>
                <span>3 Avenue du Bois Vert, <br>Portet-Sur-Garonne</span>
              </li>
              <li>
                <i class="fas fa-phone"></i>
                <span>Standard: <a href="tel:standard-phone">01 23 45 67 89</a></span>
              </li>
              <li>
                <i class="fas fa-phone-volume"></i>
                <span>Urgence: <a href="tel:emergency-phone" class="emergency">01 23 45 67 90</a></span>
              </li>
              <li>
                <i class="fas fa-envelope"></i>
                <span><a href="mailto:contact@tcpliage.fr">contact@tcpliage.fr</a></span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    
    <div class="footer-bottom">
      <div class="columns is-vcentered">
        <div class="column">
          <p class="copyright">
            © {currentYear} TCPliage. Tous droits réservés.
          </p>
        </div>
        <div class="column has-text-right-tablet">
          <div class="legal-links">
            <a href="#">Mentions Légales</a>
            <span class="separator">|</span>
            <a href="#">Politique de confidentialité</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</footer>

<style>

</style>