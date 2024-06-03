import { describe, it, expect } from 'vitest';
import '@testing-library/jest-dom';
import { render } from '@testing-library/svelte';

import Home from '../src/routes/Home.svelte';

describe('Home route', () => {
  it('renders the div with default value', () => {
    const result = render(Home);
    
    const headerText = result.getByText('Home');

    expect(headerText).toBeInTheDocument();
  });
});