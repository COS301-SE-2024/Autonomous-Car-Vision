import '@testing-library/jest-dom';
import { expect, test } from 'vitest';
import { render } from '@testing-library/svelte';

import Home from '../src/routes/Home.svelte';

test('renders the div with default value', () => {
  const result = render(Home);

  const headerText = result.getByText('Home');

  expect(headerText).toBeInTheDocument();
  // expect(true).toBe(true)
});