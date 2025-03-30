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
  .footer {
    background: linear-gradient(135deg, var(--secondary-dark), var(--secondary));
    padding: 5rem 1.5rem 2rem;
    position: relative;
    z-index: 2;
    color: var(--text-white);
    box-shadow: 0 -5px 30px rgba(0, 0, 0, 0.15);
  }
  
  .footer::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(to right, var(--primary), var(--primary-light));
  }
  
  .footer-top {
    margin-bottom: 3rem;
  }
  
  .footer-brand img {
    max-width: 150px;
    height: auto;
  }
  
  .footer-title {
    font-family: var(--font-family-heading);
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    color: var(--text-white);
    position: relative;
    padding-bottom: 0.75rem;
    display: inline-block;
  }
  
  .footer-title::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    width: 40px;
    height: 3px;
    background-color: var(--primary);
  }
  
  .footer-links {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .footer-links li {
    margin-bottom: 0.7rem;
  }
  
  .footer-links a {
    color: var(--bg-light);
    transition: all 0.3s ease;
    display: inline-block;
    position: relative;
    padding-left: 0;
  }
  
  .footer-links a::before {
    content: "→";
    position: absolute;
    left: -20px;
    opacity: 0;
    transition: all 0.3s ease;
  }
  
  .footer-links a:hover {
    color: var(--primary);
    padding-left: 20px;
  }
  
  .footer-links a:hover::before {
    opacity: 1;
    left: 0;
  }
  
  .social-links {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
  }
  
  .social-link {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #f1f1f1;
    color: var(--text);
    transition: all 0.3s ease;
  }
  
  .social-link:hover {
    background-color: var(--primary);
    color: white;
    transform: translateY(-3px);
  }
  
  .contact-details {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .contact-details li {
    display: flex;
    align-items: flex-start;
    margin-bottom: 1rem;
    color: var(--bg-light);
  }
  
  .contact-details i {
    color: var(--primary-light);
    margin-right: 1rem;
    margin-top: 0.3rem;
    width: 16px;
  }
  
  .contact-details a {
    color: var(--bg-light);
    transition: color 0.3s ease;
  }
  
  .contact-details a:hover {
    color: var(--primary);
  }
  
  .contact-details a.emergency {
    color: var(--primary);
    font-weight: 700;
  }
  
  .footer-bottom {
    padding-top: 2rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .copyright {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
  }
  
  .legal-links {
    font-size: 0.9rem;
  }
  
  .legal-links a {
    color: rgba(255, 255, 255, 0.7);
    margin: 0 0.5rem;
    transition: color 0.3s ease;
  }
  
  .legal-links a:hover {
    color: var(--primary-light);
  }
  
  .separator {
    color: rgba(255, 255, 255, 0.3);
  }
  
  /* Animation on scroll */
  .is-visible .animate-item {
    animation: fadeInUp 0.6s ease forwards;
    opacity: 0;
  }
  
  .is-visible .animate-item:nth-child(1) {
    animation-delay: 0.1s;
  }
  
  .is-visible .animate-item:nth-child(2) {
    animation-delay: 0.3s;
  }
  
  .is-visible .animate-item:nth-child(3) {
    animation-delay: 0.5s;
  }
  
  .is-visible .animate-item:nth-child(4) {
    animation-delay: 0.7s;
  }
  
  .is-visible .footer-nav {
    animation-delay: 0.3s;
  }
  
  .is-visible .footer-contact {
    animation-delay: 0.5s;
  }
  
  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  /* Responsive adjustments */
  @media screen and (max-width: 768px) {
    .footer {
      padding: 3rem 1.5rem 2rem;
    }
    
    .footer-title {
      margin-top: 1.5rem;
    }
    
    .footer-bottom .columns {
      flex-direction: column;
      text-align: center;
    }
    
    .footer-bottom .has-text-right-tablet {
      text-align: center !important;
      margin-top: 1rem;
    }
    
    .contact-details li {
      display: flex;
      align-items: flex-start;
    }
  }
</style>