<script>
    export let title;
    export let image;
    export let description;
  </script>
  
  <div class="card">
    <div class="card-image">
      <figure class="image is-4by3">
        <img src={image} alt={title}>
      </figure>
    </div>
    <div class="card-content">
      <h3 class="title is-4">{title}</h3>
      <p class="content">{description}</p>
    </div>
  </div>
  