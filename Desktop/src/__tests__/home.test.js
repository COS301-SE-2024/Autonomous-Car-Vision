// home.test.js
import { describe, expect, it } from 'vitest';
import '@testing-library/jest-dom';
import { render } from '@testing-library/svelte';
import HomePage from '../routes/Home.svelte';

describe('Home route - Landing page', () => {
  it('renders without crashing', () => {
    const { container } = render(HomePage);
    expect(container).toBeInTheDocument();
  });

  it('renders heading', () => {
    const { getByText } = render(HomePage);
    const heading = getByText('Welcome to High-Viz');
    expect(heading).toBeInTheDocument();
  });

  it('renders Log In button', () => {
    const { getByText } = render(HomePage);
    const buttonText = getByText('Log In');
    expect(buttonText).toBeInTheDocument();
  });

  it('renders Sign Up button', () => {
    const { getByText } = render(HomePage);
    const buttonText = getByText('Sign Up');
    expect(buttonText).toBeInTheDocument();
  });
});
