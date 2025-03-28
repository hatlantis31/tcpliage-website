<script>
  import { onMount } from 'svelte';
  
  let isActive = false;
  let isScrolled = false;
  
  onMount(() => {
    const handleScroll = () => {
      isScrolled = window.scrollY > 50;
    };
    
    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  });
</script>

<nav class="navbar {isScrolled ? 'is-fixed-top is-scrolled' : ''}" role="navigation" aria-label="menu principal">
  <div class="container">
    <div class="navbar-brand">
      <a class="navbar-item" href="/">
        <img class="logo" src="/logo.jpg" alt="Logo TCPliage">
      </a>

      <!-- CTA Button for Mobile -->
      <a href="tel:your-emergency-number" class="navbar-item is-hidden-desktop emergency-call">
        <span class="icon has-text-danger">
          <i class="fas fa-phone-alt"></i>
        </span>
        <span>Urgence</span>
      </a>

      <a role="button" 
         class="navbar-burger {isActive ? 'is-active' : ''}" 
         aria-label="menu" 
         aria-expanded="false"
         on:click={() => isActive = !isActive}>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>

    <div class="navbar-menu {isActive ? 'is-active' : ''}">
      <div class="navbar-end">
        <a class="navbar-item" href="/">Accueil</a>
        <a class="navbar-item" href="/services">Services</a>
        <a class="navbar-item" href="/about">À Propos</a>
        <a class="navbar-item" href="/designer">Dessin en ligne</a>
        <a class="navbar-item" href="/contact">Contact</a>
        
        <!-- Emergency Call Button -->
        <div class="navbar-item is-hidden-touch">
          <a href="tel:your-emergency-number" class="button is-danger is-outlined">
            <span class="icon">
              <i class="fas fa-phone-alt"></i>
            </span>
            <span>Service d'Urgence</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</nav>

<style>
  .navbar {
    background-color: rgba(255, 255, 255, 0.95) !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
  }
  
  .is-scrolled {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }

  .navbar-item {
    color: #333 !important;
    font-weight: 500;
    transition: color 0.2s ease;
    position: relative;
  }

  .navbar-item:hover {
    color: #E53935 !important;
    background-color: transparent !important;
  }
  
  /* Create an underline effect for nav items */
  .navbar-item::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 50%;
    width: 0;
    height: 2px;
    background-color: #E53935;
    transition: all 0.3s ease;
  }
  
  .navbar-item:hover::after {
    width: 80%;
    left: 10%;
  }

  /* Logo styles */
  .navbar-item img.logo {
    max-height: none !important;
    width: 10rem !important;
    height: 3rem !important;
    object-fit: contain !important;
  }

  /* Burger menu color */
  .navbar-burger span {
    background-color: #333 !important;
    height: 2px;
  }
  
  .navbar-burger:hover {
    background-color: transparent;
  }

  /* Mobile menu styling */
  .navbar-menu.is-active {
    background-color: #fff !important;
    box-shadow: 0 8px 16px rgba(10, 10, 10, 0.1);
    border-radius: 0 0 4px 4px;
    animation: slideDown 0.3s ease;
  }
  
  @keyframes slideDown {
    0% {
      opacity: 0;
      transform: translateY(-10px);
    }
    100% {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  /* Emergency call button styling */
  .emergency-call {
    color: #E53935 !important;
    font-weight: bold;
    display: flex;
    align-items: center;
    margin-right: 10px;
  }
  
  .emergency-call .icon {
    margin-right: 5px;
  }
  
  /* Make navbar fixed on mobile by default */
  @media screen and (max-width: 1023px) {
    .navbar {
      position: fixed;
      top: 0;
      width: 100%;
      z-index: 30;
    }
    
    /* Add padding to allow space for fixed navbar */
    :global(body) {
      padding-top: 3.25rem;
    }
  }
  
  /* Container to limit width on large screens */
  @media screen and (min-width: 1408px) {
    .container {
      max-width: 1344px !important;
    }
  }
</style>