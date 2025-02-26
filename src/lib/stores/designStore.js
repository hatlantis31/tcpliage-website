// lib/stores/designStore.js
import { writable } from 'svelte/store';

export const designPieces = writable([]);
export const designState = writable({
  material: '',
  shape: '',
  dimensions: {}
});
