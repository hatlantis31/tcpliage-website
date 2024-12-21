<script>
  let isActive = false;
</script>

<nav class="navbar" role="navigation" aria-label="menu principal">
  <div class="navbar-brand">
    <a class="navbar-item" href="/">
      <img class="logo" src="/logo.jpg" alt="Logo TCPliage">
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
    </div>
  </div>
</nav>

<style>
  /* Custom navbar background color */
  .navbar {
    background-color: #e0e0e0 !important;
  }

  /* Optional: adjust text color for better contrast */
  .navbar-item {
    color: #333 !important;
  }

  .navbar-item:hover {
    color: #000 !important;
    background-color: #d0d0d0 !important;
  }

  /* Logo styles */
  .navbar-item img.logo {
    max-height: none !important;
    width: 10rem !important;
    height: 3rem !important;
    object-fit: contain !important;
  }

  /* Ensure logo container doesn't restrict logo size */
  .navbar-brand a.navbar-item {
    padding: 0.5rem 0.75rem !important;
  }

  /* Burger menu color */
  .navbar-burger span {
    background-color: #333 !important;
  }

  /* Mobile menu background */
  .navbar-menu.is-active {
    background-color: #e0e0e0 !important;
  }
</style>