import { writable } from 'svelte/store';

const storedTheme = localStorage.getItem('theme') || 'highVizLight';
export const theme = writable(storedTheme);

theme.subscribe(value => {
  localStorage.setItem('theme', value);
});