<script>
  import { onMount } from 'svelte';
  
  let isActive = false;
  let isScrolled = false;
  let lastScrollY = 0;
  let isNavHidden = false;
  
  onMount(() => {
    const handleScroll = () => {
      // Detect scroll direction for hiding/showing navbar
      const currentScrollY = window.scrollY;
      isNavHidden = currentScrollY > lastScrollY && currentScrollY > 200;
      lastScrollY = currentScrollY;
      
      // Apply style change on scroll
      isScrolled = window.scrollY > 50;
    };
    
    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  });
  
  function toggleMenu() {
    isActive = !isActive;
    // Prevent scrolling when menu is open on mobile
    if (isActive) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
  }
</script>

<header class="site-header {isScrolled ? 'is-scrolled' : ''} {isNavHidden ? 'is-hidden' : ''}">
  <div class="container">
    <nav class="navbar" role="navigation" aria-label="Menu principal">
      <div class="navbar-brand">
        <a class="navbar-item logo-container" href="/">
          <img class="logo" src="/logo.jpg" alt="TCPliage - Fabrication métallique d'urgence">
        </a>

        <!-- Emergency button for mobile -->
        <a href="tel:your-emergency-number" class="navbar-item is-hidden-desktop emergency-call">
          <span class="icon has-text-danger">
            <i class="fas fa-phone-alt"></i>
          </span>
          <span>Urgence</span>
        </a>

        <button
          class="navbar-burger {isActive ? 'is-active' : ''}"
          aria-label="menu"
          aria-expanded="{isActive}"
          on:click={toggleMenu}
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </button>
      </div>

      <div class="navbar-menu {isActive ? 'is-active' : ''}">
        <div class="navbar-end">
          <a class="navbar-item" href="/" on:click={() => isActive = false}>Accueil</a>
          <a class="navbar-item" href="/services" on:click={() => isActive = false}>Services</a>
          <a class="navbar-item" href="/about" on:click={() => isActive = false}>À Propos</a>
          <a class="navbar-item" href="/designer" on:click={() => isActive = false}>Dessin en ligne</a>
          <a class="navbar-item" href="/contact" on:click={() => isActive = false}>Contact</a>
          
          <!-- Emergency Call Button -->
          <div class="navbar-item is-hidden-touch">
            <a href="tel:your-emergency-number" class="button is-danger">
              <span class="icon">
                <i class="fas fa-phone-alt"></i>
              </span>
              <span>Service d'Urgence 24/7</span>
            </a>
          </div>
        </div>
      </div>
    </nav>
  </div>
</header>

<style>
  .site-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    transition: all 0.3s ease;
    background: linear-gradient(to right, var(--bg-white), var(--bg-light));
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    border-bottom: 3px solid var(--primary);
  }
  
  .site-header.is-scrolled {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    background-color: var(--bg-white);
  }
  
  .site-header.is-hidden {
    transform: translateY(-100%);
  }
  
  .navbar {
    background-color: transparent;
    min-height: 4.5rem;
    padding: 0.5rem 0;
  }
  
  .logo-container {
    padding: 0.25rem 0.75rem;
  }
  
  .logo {
    height: 3rem;
    width: auto;
    max-height: none !important;
    object-fit: contain;
    transition: all 0.3s ease;
  }
  
  .is-scrolled .logo {
    height: 2.5rem;
  }
  
  .navbar-item {
    font-weight: 600;
    font-family: var(--font-family-heading);
    color: var(--text) !important;
    padding: 0.5rem 1rem;
    margin: 0 0.25rem;
    transition: all 0.3s ease;
    position: relative;
  }
  
  .navbar-item::after {
    content: "";
    position: absolute;
    width: 0;
    height: 3px;
    bottom: 0;
    left: 50%;
    background-color: var(--primary);
    transition: all 0.3s ease;
    transform: translateX(-50%);
  }
  
  .navbar-item:hover {
    color: var(--primary) !important;
    background-color: transparent !important;
  }
  
  .navbar-item:hover::after {
    width: 70%;
  }
  
  /* Current page indicator - add class 'is-active' to current page nav item */
  .navbar-item.is-active::after {
    width: 70%;
  }
  
  .navbar-burger {
    height: 4.5rem;
    width: 4.5rem;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    color: var(--text);
  }
  
  .navbar-burger span {
    height: 2px;
    width: 30px;
    left: calc(50% - 15px);
    background-color: var(--text);
    transition: all 0.3s ease;
  }
  
  .navbar-burger:hover span {
    background-color: var(--primary);
  }
  
  .navbar-burger.is-active span:nth-child(1) {
    transform: translateY(7px) rotate(45deg);
  }
  
  .navbar-burger.is-active span:nth-child(2) {
    opacity: 0;
  }
  
  .navbar-burger.is-active span:nth-child(3) {
    transform: translateY(-7px) rotate(-45deg);
  }
  
  .emergency-call {
    background-color: rgba(229, 57, 53, 0.1);
    color: var(--primary) !important;
    border-radius: 4px;
    font-weight: 700;
    margin-right: 0.5rem;
  }
  
  /* Mobile menu styles */
  @media screen and (max-width: 1023px) {
    :global(body) {
      padding-top: 4.5rem;
    }
    
    .navbar-menu {
      position: fixed;
      top: 4.5rem;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: white;
      padding: 1rem;
      display: flex;
      flex-direction: column;
      align-items: stretch;
      opacity: 0;
      pointer-events: none;
      transform: translateY(-10px);
      transition: all 0.3s ease;
      box-shadow: none;
      overflow-y: auto;
    }
    
    .navbar-menu.is-active {
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0);
      box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    
    .navbar-end {
      flex-direction: column;
      margin-top: 1rem;
    }
    
    .navbar-item {
      padding: 1rem;
      margin: 0.25rem 0;
      text-align: center;
      font-size: 1.25rem;
      border-radius: 8px;
    }
    
    .navbar-item:hover {
      background-color: rgba(229, 57, 53, 0.1) !important;
    }
    
    .navbar-item::after {
      display: none;
    }
  }
  
  /* Larger screens */
  @media screen and (min-width: 1024px) {
    :global(body) {
      padding-top: 4.5rem;
    }
    
    .navbar-menu {
      display: flex !important;
      background-color: transparent;
    }
    
    .navbar-end {
      align-items: center;
    }
  }
</style>