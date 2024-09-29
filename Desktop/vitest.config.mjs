import { defineConfig } from 'vitest/config'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import { svelteTesting } from '@testing-library/svelte/vite'

export default defineConfig({
    
    plugins: [svelte(), svelteTesting()],
    test: {
        globals: true,
        environment: 'jsdom',
        reporters: ['basic'],
        setupFiles: ['./setupTests.js'],
        exclude: ['./src/_tests_/e2eTests/**'],
        testDir: './src/_tests_/',
    }
})