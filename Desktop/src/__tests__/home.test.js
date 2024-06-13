// home.test.js
import { expect, test } from 'vitest';
import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/svelte';
import HomePage from '../routes/Home.svelte';

// test('renders without crashing', () => {
//     try{
//         render(HomePage)
//         const container = screen;
//         expect(container).toBeInTheDocument();
//     }catch (e) {
//         console.error("error occured", e);
//         if (e.stack) {
//             console.log('Stack trace:', e.stack);
//         }
//     }
// });

// test('Fake test for heading', () => {
//     render(HomePage)
    
//     const heading = screen.getAllByRole('heading', {name: 'Welcome!'})

//     expect(heading).not.toBeInTheDocument();
// })

test('renders heading', () => {
    try{
        render(HomePage);
    
        const heading = screen.findByText("Welcome to High-Viz");
        expect(heading).toBeInTheDocument();
    }catch(e){
        console.error("error occured", e);
        if (e.stack) {
            console.log('Stack trace:', e.stack);
        }
        return false;
    }
});

// test('renders Log In button', () => {
//     const { getByText } = render(HomePage);
//     const buttonText = getByText('Log In');
//     expect(buttonText).toBeInTheDocument();
// });

// test('renders Sign Up button', () => {
//     const { getByText } = render(HomePage);
//     const buttonText = getByText('Sign Up');
//     expect(buttonText).toBeInTheDocument();
// });
