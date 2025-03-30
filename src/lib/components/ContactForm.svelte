<script>
  import { onMount } from 'svelte';
  
  let formData = {
    nom: '',
    email: '',
    telephone: '',
    entreprise: '',
    sujet: '',
    message: '',
    urgence: 'normal',
    fichier: null
  };
  
  let submitStatus = null; // null, 'sending', 'success', 'error'
  let errorMessage = '';
  let formValid = false;
  let formFields = {};
  let fileLabel = 'Choisir un fichier';
  
  // Form field validation
  let validation = {
    nom: { valid: false, message: 'Veuillez entrer votre nom' },
    email: { valid: false, message: 'Veuillez entrer un email valide' },
    telephone: { valid: false, message: 'Veuillez entrer un numéro de téléphone valide' },
    message: { valid: false, message: 'Veuillez entrer un message' }
  };
  
  // Urgency levels
  const urgencyLevels = [
    { value: 'normal', label: 'Normal (3-5 jours)', icon: 'clock', color: 'is-info' },
    { value: 'urgent', label: 'Urgent (24-48h)', icon: 'exclamation', color: 'is-warning' },
    { value: 'emergency', label: 'Très urgent (24h)', icon: 'exclamation-triangle', color: 'is-danger' }
  ];
  
  // Contact subjects
  const subjects = [
    'Demande de devis',
    'Fabrication d\'urgence',
    'Informations sur nos services',
    'Service après-vente',
    'Autre demande'
  ];
  
  onMount(() => {
    // Initialize form fields references
    Object.keys(validation).forEach(key => {
      formFields[key] = document.getElementById(key);
    });
    
    // Check if there's a service parameter in the URL
    const urlParams = new URLSearchParams(window.location.search);
    const serviceParam = urlParams.get('service');
    
    if (serviceParam) {
      formData.sujet = `Demande de devis - ${serviceParam}`;
    }
  });
  
  // Validate email format
  function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  }
  
  // Validate phone format (10 digits, can have spaces, dots or dashes)
  function isValidPhone(phone) {
    const re = /^(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4})$/;
    return re.test(phone);
  }
  
  // Validate individual field
  function validateField(field) {
    if (field === 'email') {
      validation.email.valid = isValidEmail(formData.email);
    } else if (field === 'telephone') {
      validation.telephone.valid = isValidPhone(formData.telephone);
    } else if (field === 'nom') {
      validation.nom.valid = formData.nom.trim().length >= 2;
    } else if (field === 'message') {
      validation.message.valid = formData.message.trim().length >= 10;
    }
    
    updateFormValidity();
    return validation[field].valid;
  }
  
  // Update overall form validity
  function updateFormValidity() {
    formValid = Object.values(validation).every(field => field.valid);
  }
  
  // Handle input change
  function handleInput(field) {
    validateField(field);
  }
  
  // Handle input blur
  function handleBlur(field) {
    if (formFields[field] && !validation[field].valid) {
      formFields[field].classList.add('is-danger');
    }
  }
  
  // Handle input focus
  function handleFocus(field) {
    if (formFields[field]) {
      formFields[field].classList.remove('is-danger');
    }
  }
  
  // Handle file selection
  function handleFileChange(event) {
    const file = event.target.files[0];
    if (file) {
      formData.fichier = file;
      fileLabel = file.name;
    } else {
      fileLabel = 'Choisir un fichier';
    }
  }
  
  // Handle form submission
  async function handleSubmit() {
    // Validate all fields
    Object.keys(validation).forEach(validateField);
    
    if (!formValid) {
      Object.keys(validation).forEach(field => {
        if (!validation[field].valid && formFields[field]) {
          formFields[field].classList.add('is-danger');
        }
      });
      return;
    }
    
    submitStatus = 'sending';
    
    try {
      // Simulate form submission for demo purposes
      // In a real app, you'd send data to your backend
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      console.log('Form submitted:', formData);
      submitStatus = 'success';
      
      // Reset form after success
      setTimeout(() => {
        formData = {
          nom: '',
          email: '',
          telephone: '',
          entreprise: '',
          sujet: '',
          message: '',
          urgence: 'normal',
          fichier: null
        };
        
        // Reset validation
        Object.keys(validation).forEach(key => {
          validation[key].valid = false;
          if (formFields[key]) {
            formFields[key].classList.remove('is-danger');
          }
        });
        
        fileLabel = 'Choisir un fichier';
        formValid = false;
        submitStatus = null;
      }, 3000);
      
    } catch (error) {
      console.error('Error submitting form:', error);
      submitStatus = 'error';
      errorMessage = "Une erreur s'est produite. Veuillez réessayer ou nous contacter par téléphone.";
    }
  }
</script>

<div class="contact-form-container">
  {#if submitStatus === 'success'}
    <div class="form-success">
      <div class="success-icon">
        <i class="fas fa-check-circle"></i>
      </div>
      <h3>Message Envoyé!</h3>
      <p>Votre message a été envoyé avec succès. Nous vous répondrons dans les plus brefs délais.</p>
    </div>
  {:else}
    <form class="contact-form" on:submit|preventDefault={handleSubmit}>
      <!-- Form Status Messages -->
      {#if submitStatus === 'error'}
        <div class="notification is-danger">
          <button class="delete" on:click={() => submitStatus = null}></button>
          <p>
            <span class="icon"><i class="fas fa-exclamation-triangle"></i></span>
            <span>{errorMessage}</span>
          </p>
        </div>
      {/if}
      
      <div class="columns is-multiline">
        <!-- Left Column -->
        <div class="column is-6">
          <!-- Name Field -->
          <div class="field">
            <label class="label" for="nom">Nom <span class="required">*</span></label>
            <div class="control has-icons-left">
              <input 
                id="nom"
                class="input" 
                type="text" 
                placeholder="Votre nom et prénom"
                bind:value={formData.nom}
                on:input={() => handleInput('nom')}
                on:focus={() => handleFocus('nom')}
                on:blur={() => handleBlur('nom')}
                required
              >
              <span class="icon is-small is-left">
                <i class="fas fa-user"></i>
              </span>
            </div>
            {#if !validation.nom.valid && formData.nom !== ''}
              <p class="help is-danger">{validation.nom.message}</p>
            {/if}
          </div>
          
          <!-- Email Field -->
          <div class="field">
            <label class="label" for="email">Email <span class="required">*</span></label>
            <div class="control has-icons-left">
              <input 
                id="email"
                class="input" 
                type="email" 
                placeholder="Votre adresse email"
                bind:value={formData.email}
                on:input={() => handleInput('email')}
                on:focus={() => handleFocus('email')}
                on:blur={() => handleBlur('email')}
                required
              >
              <span class="icon is-small is-left">
                <i class="fas fa-envelope"></i>
              </span>
            </div>
            {#if !validation.email.valid && formData.email !== ''}
              <p class="help is-danger">{validation.email.message}</p>
            {/if}
          </div>
          
          <!-- Phone Field -->
          <div class="field">
            <label class="label" for="telephone">Téléphone <span class="required">*</span></label>
            <div class="control has-icons-left">
              <input 
                id="telephone"
                class="input" 
                type="tel" 
                placeholder="Votre numéro de téléphone"
                bind:value={formData.telephone}
                on:input={() => handleInput('telephone')}
                on:focus={() => handleFocus('telephone')}
                on:blur={() => handleBlur('telephone')}
                required
              >
              <span class="icon is-small is-left">
                <i class="fas fa-phone"></i>
              </span>
            </div>
            {#if !validation.telephone.valid && formData.telephone !== ''}
              <p class="help is-danger">{validation.telephone.message}</p>
            {/if}
          </div>
          
          <!-- Company Field -->
          <div class="field">
            <label class="label" for="entreprise">Entreprise</label>
            <div class="control has-icons-left">
              <input 
                id="entreprise"
                class="input" 
                type="text" 
                placeholder="Nom de votre entreprise (optionnel)"
                bind:value={formData.entreprise}
              >
              <span class="icon is-small is-left">
                <i class="fas fa-building"></i>
              </span>
            </div>
          </div>
        </div>
        
        <!-- Right Column -->
        <div class="column is-6">
          <!-- Subject Field -->
          <div class="field">
            <label class="label" for="sujet">Sujet</label>
            <div class="control has-icons-left">
              <div class="select is-fullwidth">
                <select id="sujet" bind:value={formData.sujet}>
                  <option value="" disabled selected>Sélectionnez un sujet</option>
                  {#each subjects as subject}
                    <option value={subject}>{subject}</option>
                  {/each}
                </select>
              </div>
              <span class="icon is-small is-left">
                <i class="fas fa-tag"></i>
              </span>
            </div>
          </div>
          
          <!-- Urgency Level Field -->
          <div class="field">
            <label class="label">Niveau d'Urgence</label>
            <div class="control">
              <div class="urgency-selector">
                {#each urgencyLevels as level}
                  <label class="urgency-option">
                    <input 
                      type="radio" 
                      name="urgence"
                      bind:group={formData.urgence} 
                      value={level.value}
                    >
                    <div class={`urgency-label ${level.color}`}>
                      <span class="icon">
                        <i class={`fas fa-${level.icon}`}></i>
                      </span>
                      <span>{level.label}</span>
                    </div>
                  </label>
                {/each}
              </div>
            </div>
          </div>
          
          <!-- File Upload Field -->
          <div class="field">
            <label class="label">Joindre un fichier</label>
            <div class="file has-name is-fullwidth">
              <label class="file-label">
                <input 
                  class="file-input" 
                  type="file" 
                  name="fichier"
                  on:change={handleFileChange}
                  accept=".pdf,.jpg,.jpeg,.png,.dwg,.dxf"
                >
                <span class="file-cta">
                  <span class="file-icon">
                    <i class="fas fa-upload"></i>
                  </span>
                  <span class="file-label">Choisir</span>
                </span>
                <span class="file-name">
                  {fileLabel}
                </span>
              </label>
            </div>
            <p class="help">Maximum 10 Mo (PDF, JPG, PNG, DWG, DXF)</p>
          </div>
        </div>
        
        <!-- Message Field (Full Width) -->
        <div class="column is-12">
          <div class="field">
            <label class="label" for="message">Message <span class="required">*</span></label>
            <div class="control">
              <textarea 
                id="message"
                class="textarea" 
                placeholder="Détaillez votre demande..."
                rows="5"
                bind:value={formData.message}
                on:input={() => handleInput('message')}
                on:focus={() => handleFocus('message')}
                on:blur={() => handleBlur('message')}
                required
              ></textarea>
            </div>
            {#if !validation.message.valid && formData.message !== ''}
              <p class="help is-danger">{validation.message.message}</p>
            {/if}
          </div>
        </div>
      </div>
      
      <div class="field">
        <div class="control">
          <label class="checkbox">
            <input type="checkbox" required>
            J'accepte que mes données soient traitées pour traiter ma demande conformément à la <a href="#">politique de confidentialité</a>.
          </label>
        </div>
      </div>
      
      <div class="field is-grouped is-grouped-right">
        <div class="control">
          <button 
            type="submit" 
            class="button is-primary is-medium submit-button"
            class:is-loading={submitStatus === 'sending'}
            disabled={submitStatus === 'sending'}
          >
            <span class="icon">
              <i class="fas fa-paper-plane"></i>
            </span>
            <span>Envoyer</span>
          </button>
        </div>
      </div>
    </form>
  {/if}
</div>

<style>
  .contact-form-container {
    position: relative;
    background: linear-gradient(135deg, var(--bg-white), var(--bg-light));
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--border);
  }
  
  .contact-form {
    padding: 2rem;
  }
  
  .contact-form::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(to right, var(--primary), var(--primary-light));
  }
  
  .form-success {
    padding: 4rem 2rem;
    text-align: center;
    animation: fadeSlideUp 0.5s ease forwards;
  }
  
  .success-icon {
    font-size: 4rem;
    color: var(--success);
    margin-bottom: 1.5rem;
    display: inline-block;
    animation: scaleUp 0.5s ease forwards 0.2s;
    transform: scale(0);
  }
  
  .form-success h3 {
    font-size: 1.75rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--dark);
  }
  
  .form-success p {
    color: var(--text-light);
    font-size: 1.1rem;
    max-width: 500px;
    margin: 0 auto;
  }
  
  .required {
    color: var(--primary);
  }
  
  .label {
    font-weight: 600;
    color: var(--dark);
    margin-bottom: 0.5rem;
  }
  
  .input, .textarea, .select select {
    background-color: white;
    border: 2px solid var(--border);
    transition: all 0.3s ease;
  }
  
  .input:focus, .textarea:focus, .select select:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(229, 57, 53, 0.1);
  }
  
  .input.is-danger, .textarea.is-danger {
    border-color: var(--danger);
    animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
  }
  
  .urgency-selector {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .urgency-option {
    display: flex;
    align-items: center;
    cursor: pointer;
  }
  
  .urgency-option input {
    position: absolute;
    opacity: 0;
    width: 0;
    height: 0;
  }
  
  .urgency-label {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    border-radius: var(--radius-md);
    border: 2px solid var(--border);
    width: 100%;
    transition: all 0.3s ease;
  }
  
  .urgency-label .icon {
    margin-right: 0.75rem;
  }
  
  .urgency-label.is-info {
    color: var(--info);
    background-color: rgba(33, 150, 243, 0.05);
  }
  
  .urgency-label.is-warning {
    color: var(--warning);
    background-color: rgba(255, 193, 7, 0.05);
  }
  
  .urgency-label.is-danger {
    color: var(--danger);
    background-color: rgba(255, 61, 0, 0.05);
  }
  
  .urgency-option input:checked + .urgency-label {
    border-color: currentColor;
    background-color: rgba(229, 57, 53, 0.05);
    font-weight: 600;
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
  }
  
  .urgency-option input:checked + .urgency-label.is-info {
    background-color: rgba(33, 150, 243, 0.15);
  }
  
  .urgency-option input:checked + .urgency-label.is-warning {
    background-color: rgba(255, 193, 7, 0.15);
  }
  
  .urgency-option input:checked + .urgency-label.is-danger {
    background-color: rgba(255, 61, 0, 0.15);
  }
  
  .urgency-option:hover .urgency-label {
    transform: translateY(-2px);
  }
  
  .file-cta {
    background-color: var(--primary);
    color: white;
    border: none;
    font-weight: 600;
  }
  
  .file-name {
    border-color: var(--border);
    border-width: 2px;
    font-size: 0.9rem;
  }
  
  .file-input:focus + .file-cta {
    box-shadow: 0 0 0 2px rgba(229, 57, 53, 0.2);
  }
  
  .submit-button {
    min-width: 160px;
    height: 3rem;
    font-weight: 600;
  }
  
  .checkbox {
    display: flex;
    align-items: center;
    font-size: 0.9rem;
    color: var(--text-light);
  }
  
  .checkbox input {
    margin-right: 0.5rem;
  }
  
  .notification {
    margin-bottom: 2rem;
    animation: fadeSlideDown 0.5s ease;
  }
  
  .help {
    font-size: 0.8rem;
    transition: all 0.3s ease;
  }
  
  .help.is-danger {
    color: var(--danger);
  }
  
  @keyframes shake {
    10%, 90% {
      transform: translateX(-1px);
    }
    
    20%, 80% {
      transform: translateX(2px);
    }
    
    30%, 50%, 70% {
      transform: translateX(-3px);
    }
    
    40%, 60% {
      transform: translateX(3px);
    }
  }
  
  @keyframes fadeSlideDown {
    from {
      opacity: 0;
      transform: translateY(-20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  @keyframes fadeSlideUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  @keyframes scaleUp {
    from {
      transform: scale(0);
    }
    to {
      transform: scale(1);
    }
  }
  
  /* Responsive Adjustments */
  @media screen and (max-width: 768px) {
    .contact-form {
      padding: 1.5rem;
    }
    
    .urgency-selector {
      gap: 0.5rem;
    }
    
    .submit-button {
      width: 100%;
    }
  }
</style>