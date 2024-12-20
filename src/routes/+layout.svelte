<script>
    import 'bulma/css/bulma.min.css';
    import Header from '$lib/components/Header.svelte';
    import Footer from '$lib/components/Footer.svelte';
  </script>
  
  <Header />
  
  <main>
    <slot />
  </main>
  
  <Footer />
  
  <style>
    main {
      min-height: calc(100vh - 14rem);
    }
  </style>
  