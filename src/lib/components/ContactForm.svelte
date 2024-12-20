<script>
  let formData = {
    nom: '',
    email: '',
    telephone: '',
    message: '',
    urgence: 'normal'
  };

  async function handleSubmit() {
    try {
      // Logique d'envoi du formulaire
      console.log('Formulaire envoyé:', formData);
    } catch (error) {
      console.error('Erreur lors de l\'envoi du formulaire:', error);
    }
  }
</script>

<form class="box" on:submit|preventDefault={handleSubmit}>
  <div class="field">
    <label class="label">Nom</label>
    <div class="control">
      <input 
        class="input" 
        type="text" 
        bind:value={formData.nom} 
        required
      >
    </div>
  </div>

  <div class="field">
    <label class="label">Email</label>
    <div class="control">
      <input 
        class="input" 
        type="email" 
        bind:value={formData.email} 
        required
      >
    </div>
  </div>

  <div class="field">
    <label class="label">Téléphone</label>
    <div class="control">
      <input 
        class="input" 
        type="tel" 
        bind:value={formData.telephone} 
        required
      >
    </div>
  </div>

  <div class="field">
    <label class="label">Niveau d'Urgence</label>
    <div class="control">
      <div class="select">
        <select bind:value={formData.urgence}>
          <option value="normal">Normal</option>
          <option value="urgent">Urgent</option>
          <option value="emergency">Très Urgent</option>
        </select>
      </div>
    </div>
  </div>

  <div class="field">
    <label class="label">Message</label>
    <div class="control">
      <textarea 
        class="textarea" 
        bind:value={formData.message} 
        required
      ></textarea>
    </div>
  </div>

  <button class="button is-primary" type="submit">Envoyer</button>
</form>
