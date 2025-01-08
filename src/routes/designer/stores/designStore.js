// designStore.js
import { writable } from "svelte/store";

export const designState = writable({
  step: 1,
  material: "",
  shape: "",
  dimensions: {},
});
