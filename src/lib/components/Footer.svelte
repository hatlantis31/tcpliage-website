<script>
  const currentYear = new Date().getFullYear();
</script>

<footer class="footer">
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-4">
        <div class="footer-brand mb-4">
          <img src="/logo.jpg" alt="TCPliage Logo" width="180">
        </div>
        <p class="has-text-grey mb-3">
          TC PLIAGE, votre partenaire métallurgique de confiance depuis 2016. Notre savoir-faire et notre réactivité au service de vos projets.
        </p>
        <div class="social-icons">
          <a href="#" class="icon-link" aria-label="Facebook">
            <span class="icon">
              <i class="fab fa-facebook-f"></i>
            </span>
          </a>
          <a href="#" class="icon-link" aria-label="LinkedIn">
            <span class="icon">
              <i class="fab fa-linkedin-in"></i>
            </span>
          </a>
          <a href="#" class="icon-link" aria-label="Instagram">
            <span class="icon">
              <i class="fab fa-instagram"></i>
            </span>
          </a>
        </div>
      </div>
      
      <div class="column is-2-tablet is-6-mobile">
        <h3 class="footer-title">Navigation</h3>
        <ul class="footer-links">
          <li><a href="/">Accueil</a></li>
          <li><a href="/services">Services</a></li>
          <li><a href="/about">À Propos</a></li>
          <li><a href="/designer">Dessin en ligne</a></li>
          <li><a href="/contact">Contact</a></li>
        </ul>
      </div>
      
      <div class="column is-3-tablet is-6-mobile">
        <h3 class="footer-title">Nos Services</h3>
        <ul class="footer-links">
          <li><a href="/services">Fabrication d'Urgence</a></li>
          <li><a href="/services">Pièces Sur Mesure</a></li>
          <li><a href="/services">Couvertines</a></li>
          <li><a href="/services">Habillages Métalliques</a></li>
          <li><a href="/services">Quincaillerie</a></li>
        </ul>
      </div>
      
      <div class="column is-3-tablet is-12-mobile">
        <h3 class="footer-title">Contact</h3>
        <div class="contact-info">
          <p>
            <span class="icon has-text-danger"><i class="fas fa-map-marker-alt"></i></span>
            3 Avenue du Bois Vert, <br>Portet-Sur-Garonne
          </p>
          <p>
            <span class="icon has-text-danger"><i class="fas fa-phone"></i></span>
            Standard: <a href="tel:standard-phone">01 23 45 67 89</a>
          </p>
          <p>
            <span class="icon has-text-danger"><i class="fas fa-phone-volume"></i></span>
            Urgence: <a href="tel:emergency-phone" class="has-text-danger has-text-weight-bold">01 23 45 67 90</a>
          </p>
          <p>
            <span class="icon has-text-danger"><i class="fas fa-envelope"></i></span>
            <a href="mailto:contact@tcpliage.fr">contact@tcpliage.fr</a>
          </p>
        </div>
      </div>
    </div>
    
    <hr class="footer-divider">
    
    <div class="level is-mobile">
      <div class="level-left">
        <div class="level-item">
          <p class="is-size-7 has-text-grey">
            © {currentYear} TCPliage. Tous droits réservés.
          </p>
        </div>
      </div>
      <div class="level-right">
        <div class="level-item">
          <a href="#" class="is-size-7">Mentions Légales</a>
        </div>
        <div class="level-item">
          <a href="#" class="is-size-7">Politique de confidentialité</a>
        </div>
      </div>
    </div>
  </div>
</footer>

<style>
  .footer {
    background-color: #f5f5f5;
    padding: 3rem 1.5rem 2rem;
    color: #4a4a4a;
  }
  
  .footer-brand {
    display: block;
    margin-bottom: 1rem;
  }
  
  .footer-title {
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1.25rem;
    color: #363636;
    position: relative;
    padding-bottom: 0.75rem;
  }
  
  .footer-title::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    width: 50px;
    height: 2px;
    background-color: #E53935;
  }
  
  .footer-links {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .footer-links li {
    margin-bottom: 0.5rem;
  }
  
  .footer-links a {
    color: #4a4a4a;
    transition: color 0.2s ease;
    display: inline-block;
    position: relative;
    padding-left: 0;
  }
  
  .footer-links a::before {
    content: "→";
    position: absolute;
    left: -15px;
    opacity: 0;
    transition: all 0.2s ease;
  }
  
  .footer-links a:hover {
    color: #E53935;
    padding-left: 15px;
  }
  
  .footer-links a:hover::before {
    opacity: 1;
    left: 0;
  }
  
  .social-icons {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
  }
  
  .icon-link {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background-color: #E0E0E0;
    color: #333;
    transition: all 0.2s ease;
  }
  
  .icon-link:hover {
    background-color: #E53935;
    color: white;
    transform: translateY(-3px);
  }
  
  .contact-info p {
    display: flex;
    align-items: flex-start;
    margin-bottom: 0.75rem;
  }
  
  .contact-info .icon {
    margin-right: 0.75rem;
    width: 16px;
  }
  
  .contact-info a {
    color: #4a4a4a;
    transition: color 0.2s ease;
  }
  
  .contact-info a:hover {
    color: #E53935;
  }
  
  .footer-divider {
    background-color: #e0e0e0;
    height: 1px;
    margin: 2rem 0 1.5rem;
  }
  
  /* Responsive adjustments */
  @media screen and (max-width: 768px) {
    .footer-title {
      margin-top: 1.5rem;
    }
    
    .level-left, .level-right {
      flex-direction: column;
      align-items: center;
    }
    
    .level-item:not(:last-child) {
      margin-bottom: 0.5rem;
    }
  }
</style>