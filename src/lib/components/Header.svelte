<script>
    let isActive = false;
  </script>
  
  <nav class="navbar is-dark" role="navigation" aria-label="menu principal">
    <div class="navbar-brand">
      <a class="navbar-item" href="/">
        <img class="logo" src="/logo.jpg" alt="Logo TCPliage" height="28">
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
        <a class="navbar-item" href="/contact">Contact</a>
      </div>
    </div>
  </nav>
  
  <style>
    .logo {
      margin-right: 1rem;
      /* size */
      width: 10rem;
  /* importan height */
      height: 3rem;
    }
  </style>