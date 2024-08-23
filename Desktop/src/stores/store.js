import { writable } from 'svelte/store';

export const sidebarWidth = writable(150);
export const canvas = writable();
export const warp_pipe = writable();
export const outputPipe = writable([]);