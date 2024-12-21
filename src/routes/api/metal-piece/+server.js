import { json } from "@sveltejs/kit";

export async function POST({ request }) {
  const data = await request.json();
  // Envoyez les données au serveur Python
  // Retournez le résultat
  return json({ success: true, piece: data });
}
