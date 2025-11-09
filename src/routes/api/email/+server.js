import { json } from '@sveltejs/kit';

export async function POST({ request }) {
  try {
    const data = await request.json();

    // Format email content
    const emailHtml = `
      <h2>Nouvelle Conception de Pièce Métallique</h2>
      <p><strong>Référence:</strong> ${data.referenceNumber}</p>
      <p><strong>Coût Estimé:</strong> €${data.estimatedCost.toFixed(2)}</p>
      <p><strong>Délai de Production:</strong> ${data.productionDays} jours</p>
      <p><strong>Date de Soumission:</strong> ${new Date(data.submittedAt).toLocaleString('fr-FR')}</p>

      <h3>Détails de la Conception:</h3>
      <pre>${data.designData}</pre>

      ${data.screenshot ? `<h3>Aperçu:</h3><img src="${data.screenshot}" alt="Design Preview" style="max-width: 600px;">` : ''}
    `;

    // Use a service like SendGrid, Mailgun, or Resend
    // Example with fetch to an email service:
    const emailResponse = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.RESEND_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        from: 'noreply@tcpliage.fr',
        to: data.to,
        subject: data.subject,
        html: emailHtml,
        attachments: data.screenshot ? [{
          filename: `design-${data.referenceNumber}.svg`,
          content: data.screenshot
        }] : []
      })
    });

    if (!emailResponse.ok) {
      throw new Error('Failed to send email via service');
    }

    return json({ success: true });
  } catch (error) {
    console.error('Email error:', error);
    return json({ success: false, error: error.message }, { status: 500 });
  }
}