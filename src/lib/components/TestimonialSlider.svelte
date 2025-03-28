<!-- TestimonialSlider.svelte -->
<script>
    import { onMount, onDestroy } from 'svelte';
    
    export let testimonials = [];
    export let autoplaySpeed = 5000; // in milliseconds
    export let showControls = true;
    export let columns = 3; // Number of columns in desktop view
    
    let currentIndex = 0;
    let intervalId;
    let testimonialContainer;
    let isTransitioning = false;
    
    // Calculate number of slides to show based on columns
    $: slidesToShow = Math.min(testimonials.length, columns);
    $: totalSlides = Math.ceil(testimonials.length / slidesToShow);
    
    // Adjust currentIndex to stay within bounds
    $: if (testimonials.length && currentIndex >= totalSlides) {
      currentIndex = 0;
    }
    
    // Get visible testimonials based on current index and slides to show
    $: visibleTestimonials = getVisibleTestimonials(currentIndex, slidesToShow);
    
    function getVisibleTestimonials(index, count) {
      const startIndex = index * count;
      return testimonials.slice(startIndex, startIndex + count);
    }
    
    function nextSlide() {
      if (isTransitioning) return;
      isTransitioning = true;
      
      // Add transition-out class to current items
      if (testimonialContainer) {
        const items = testimonialContainer.querySelectorAll('.testimonial-card');
        items.forEach(item => {
          item.classList.add('transition-out');
        });
        
        // Wait for transition to complete
        setTimeout(() => {
          currentIndex = (currentIndex + 1) % totalSlides;
          
          // Remove transition classes after a brief delay to allow new items to render
          setTimeout(() => {
            const newItems = testimonialContainer.querySelectorAll('.testimonial-card');
            newItems.forEach(item => {
              item.classList.remove('transition-out');
              item.classList.add('transition-in');
            });
            
            // Remove transition-in class after animation completes
            setTimeout(() => {
              newItems.forEach(item => {
                item.classList.remove('transition-in');
              });
              isTransitioning = false;
            }, 500);
          }, 50);
        }, 300);
      }
    }
    
    function prevSlide() {
      if (isTransitioning) return;
      isTransitioning = true;
      
      // Add transition-out class to current items
      if (testimonialContainer) {
        const items = testimonialContainer.querySelectorAll('.testimonial-card');
        items.forEach(item => {
          item.classList.add('transition-out-reverse');
        });
        
        // Wait for transition to complete
        setTimeout(() => {
          currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
          
          // Remove transition classes after a brief delay to allow new items to render
          setTimeout(() => {
            const newItems = testimonialContainer.querySelectorAll('.testimonial-card');
            newItems.forEach(item => {
              item.classList.remove('transition-out-reverse');
              item.classList.add('transition-in-reverse');
            });
            
            // Remove transition-in class after animation completes
            setTimeout(() => {
              newItems.forEach(item => {
                item.classList.remove('transition-in-reverse');
              });
              isTransitioning = false;
            }, 500);
          }, 50);
        }, 300);
      }
    }
    
    function goToSlide(index) {
      if (isTransitioning || index === currentIndex) return;
      
      const direction = index > currentIndex ? 'next' : 'prev';
      
      // Add appropriate transition class
      if (testimonialContainer) {
        const items = testimonialContainer.querySelectorAll('.testimonial-card');
        items.forEach(item => {
          item.classList.add(direction === 'next' ? 'transition-out' : 'transition-out-reverse');
        });
        
        // Wait for transition to complete
        setTimeout(() => {
          currentIndex = index;
          
          // Remove transition classes after a brief delay
          setTimeout(() => {
            const newItems = testimonialContainer.querySelectorAll('.testimonial-card');
            newItems.forEach(item => {
              item.classList.remove('transition-out', 'transition-out-reverse');
              item.classList.add(direction === 'next' ? 'transition-in' : 'transition-in-reverse');
            });
            
            // Remove transition-in class after animation completes
            setTimeout(() => {
              newItems.forEach(item => {
                item.classList.remove('transition-in', 'transition-in-reverse');
              });
              isTransitioning = false;
            }, 500);
          }, 50);
        }, 300);
      }
    }
    
    function startAutoplay() {
      if (testimonials.length <= slidesToShow) return;
      
      intervalId = setInterval(() => {
        nextSlide();
      }, autoplaySpeed);
    }
    
    function pauseAutoplay() {
      if (intervalId) {
        clearInterval(intervalId);
      }
    }
    
    function resumeAutoplay() {
      pauseAutoplay();
      startAutoplay();
    }
    
    onMount(() => {
      if (testimonials.length > slidesToShow) {
        startAutoplay();
      }
    });
    
    onDestroy(() => {
      pauseAutoplay();
    });
  </script>
  
  <div 
    class="testimonial-slider"
    on:mouseenter={pauseAutoplay}
    on:mouseleave={resumeAutoplay}
  >
    {#if showControls && testimonials.length > slidesToShow}
      <button 
        class="slider-control prev-control" 
        on:click={prevSlide}
        aria-label="Témoignage précédent"
      >
        <span class="icon">
          <i class="fas fa-chevron-left"></i>
        </span>
      </button>
      
      <button 
        class="slider-control next-control" 
        on:click={nextSlide}
        aria-label="Témoignage suivant"
      >
        <span class="icon">
          <i class="fas fa-chevron-right"></i>
        </span>
      </button>
    {/if}
    
    <div bind:this={testimonialContainer} class="testimonial-container">
      {#if visibleTestimonials.length === 0}
        <div class="empty-state">
          <p>Aucun témoignage disponible pour le moment.</p>
        </div>
      {:else}
        <div class="columns is-multiline">
          {#each visibleTestimonials as testimonial (testimonial.id || testimonial.name)}
            <div class="column is-{12/slidesToShow}">
              <div class="testimonial-card">
                <div class="testimonial-content">
                  <div class="quote-mark">"</div>
                  <p class="testimonial-text">{testimonial.quote || testimonial.text}</p>
                  <div class="rating">
                    {#each Array(5) as _, i}
                      <span class="icon is-small">
                        <i class={`fas fa-star ${i < (testimonial.rating || 5) ? 'filled' : 'empty'}`}></i>
                      </span>
                    {/each}
                  </div>
                </div>
                <div class="testimonial-author">
                  {#if testimonial.image}
                    <div class="author-image">
                      <img src={testimonial.image} alt={testimonial.name} class="is-rounded">
                    </div>
                  {:else}
                    <div class="author-initials">
                      {testimonial.name.split(' ').map(n => n[0]).join('')}
                    </div>
                  {/if}
                  <div class="author-info">
                    <p class="author-name">{testimonial.name}</p>
                    {#if testimonial.company}
                      <p class="author-title">{testimonial.company}</p>
                    {/if}
                  </div>
                </div>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
    
    {#if showControls && testimonials.length > slidesToShow}
      <div class="slider-indicators">
        {#each Array(totalSlides) as _, i}
          <button 
            class="slider-indicator {i === currentIndex ? 'is-active' : ''}" 
            on:click={() => goToSlide(i)}
            aria-label={`Aller au témoignage ${i + 1}`}
          ></button>
        {/each}
      </div>
    {/if}
  </div>
  
  <style>
    .testimonial-slider {
      position: relative;
      padding: 2rem 0;
    }
    
    .testimonial-container {
      overflow: hidden;
    }
    
    .testimonial-card {
      height: 100%;
      background-color: white;
      border-radius: 8px;
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
      padding: 2rem;
      display: flex;
      flex-direction: column;
      transition: all 0.3s ease;
    }
    
    .testimonial-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
    }
    
    .testimonial-content {
      flex-grow: 1;
      position: relative;
      margin-bottom: 1.5rem;
    }
    
    .quote-mark {
      position: absolute;
      top: -20px;
      left: -10px;
      font-size: 4rem;
      color: #E53935;
      opacity: 0.1;
      font-family: serif;
      font-weight: 700;
    }
    
    .testimonial-text {
      color: #555;
      font-style: italic;
      margin-bottom: 1.5rem;
      line-height: 1.6;
    }
    
    .rating {
      display: flex;
      margin-bottom: 0.5rem;
    }
    
    .rating .icon {
      color: #FFD700;
      margin-right: 0.25rem;
    }
    
    .rating .icon .empty {
      color: #E0E0E0;
    }
    
    .testimonial-author {
      display: flex;
      align-items: center;
      border-top: 1px solid #f0f0f0;
      padding-top: 1rem;
    }
    
    .author-image {
      width: 50px;
      height: 50px;
      overflow: hidden;
      margin-right: 1rem;
      flex-shrink: 0;
    }
    
    .author-image img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      border-radius: 50%;
    }
    
    .author-initials {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background-color: #E53935;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 600;
      margin-right: 1rem;
      flex-shrink: 0;
    }
    
    .author-info {
      flex-grow: 1;
    }
    
    .author-name {
      font-weight: 600;
      color: #333;
      margin: 0;
    }
    
    .author-title {
      font-size: 0.85rem;
      color: #777;
      margin: 0;
    }
    
    .slider-control {
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background-color: white;
      border: none;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #555;
      cursor: pointer;
      z-index: 10;
      transition: all 0.2s ease;
    }
    
    .slider-control:hover {
      background-color: #E53935;
      color: white;
      box-shadow: 0 5px 15px rgba(229, 57, 53, 0.2);
    }
    
    .prev-control {
      left: -20px;
    }
    
    .next-control {
      right: -20px;
    }
    
    .slider-indicators {
      display: flex;
      justify-content: center;
      margin-top: 2rem;
    }
    
    .slider-indicator {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background-color: #E0E0E0;
      border: none;
      margin: 0 5px;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    
    .slider-indicator.is-active {
      background-color: #E53935;
      transform: scale(1.2);
    }
    
    .empty-state {
      text-align: center;
      padding: 3rem;
      color: #777;
    }
    
    /* Animation classes */
    .transition-out {
      animation: fadeOutLeft 0.3s ease forwards;
    }
    
    .transition-in {
      animation: fadeInRight 0.3s ease forwards;
    }
    
    .transition-out-reverse {
      animation: fadeOutRight 0.3s ease forwards;
    }
    
    .transition-in-reverse {
      animation: fadeInLeft 0.3s ease forwards;
    }
    
    @keyframes fadeOutLeft {
      from {
        opacity: 1;
        transform: translateX(0);
      }
      to {
        opacity: 0;
        transform: translateX(-20px);
      }
    }
    
    @keyframes fadeInRight {
      from {
        opacity: 0;
        transform: translateX(20px);
      }
      to {
        opacity: 1;
        transform: translateX(0);
      }
    }
    
    @keyframes fadeOutRight {
      from {
        opacity: 1;
        transform: translateX(0);
      }
      to {
        opacity: 0;
        transform: translateX(20px);
      }
    }
    
    @keyframes fadeInLeft {
      from {
        opacity: 0;
        transform: translateX(-20px);
      }
      to {
        opacity: 1;
        transform: translateX(0);
      }
    }
    
    /* Responsive adjustments */
    @media screen and (max-width: 768px) {
      .prev-control, .next-control {
        width: 35px;
        height: 35px;
      }
      
      .prev-control {
        left: -10px;
      }
      
      .next-control {
        right: -10px;
      }
      
      .testimonial-card {
        padding: 1.5rem;
      }
    }
  </style>