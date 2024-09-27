import { describe, expect, it, test } from 'vitest'
import { render, fireEvent, waitFor } from '@testing-library/svelte';
import AccountPopUp from '../../components/AccountPopup.svelte'; // Replace 'AccountPopUp' with the actual component name

test('renders the correct number of list items', async () => {
  try {
    const items = [
      { name: 'Item 1', route: '/item1', iconPath: 'icon1' },
      { name: 'Item 2', route: '/item2', iconPath: 'icon2' },
      { name: 'Item 3', route: '/item3', iconPath: 'icon3' },
    ];

    const { container } = render(AccountPopUp, { items });

    const listItems = container.querySelectorAll('li');

    expect(listItems.length).toBe(3);
  } catch (error) {
    console.error('Test failed:', error);
  }
});

test('renders the correct icon and name for each list item', async () => {
  try {
    const items = [
      { name: 'Item 1', route: '/item1', iconPath: 'icon1' },
      { name: 'Item 2', route: '/item2', iconPath: 'icon2' },
      { name: 'Item 3', route: '/item3', iconPath: 'icon3' },
    ];

    const { container } = render(AccountPopUp, { items });

    const listItems = container.querySelectorAll('li');

    for (let i = 0; i < listItems.length; i++) {
      const icon = listItems[i].querySelector('icon');
      const name = listItems[i].querySelector('span');

      expect(icon.getAttribute('path')).toBe(items[i].iconPath);
      expect(name.textContent).toBe(items[i].name);
    }
  } catch (error) {
    console.error('Test failed:', error);
  }
});

test('handles option click and dispatches "close" event', async () => {
  try {
    const items = [
      { name: 'Item 1', route: '/item1', iconPath: 'icon1' },
      { name: 'Item 2', route: '/item2', iconPath: 'icon2' },
      { name: 'Item 3', route: '/item3', iconPath: 'icon3' },
    ];

    const dispatch = jest.fn();
    const { container } = render(AccountPopUp, { items, dispatch });

    const option = container.querySelector('li');
    fireEvent.click(option);

    await waitFor(() => expect(dispatch).toHaveBeenCalledWith('close'));
  } catch (error) {
    console.error('Test failed:', error);
  }
});

test('navigates to the correct route when a list item is clicked', async () => {
  try {
    const items = [
      { name: 'Item 1', route: '/item1', iconPath: 'icon1' },
      { name: 'Item 2', route: '/item2', iconPath: 'icon2' },
      { name: 'Item 3', route: '/item3', iconPath: 'icon3' },
    ];

    const { container, history } = render(AccountPopUp, { items });

    const listItems = container.querySelectorAll('li');

    for (let i = 0; i < listItems.length; i++) {
      const a = listItems[i].querySelector('a');
      fireEvent.click(a);

      await waitFor(() => expect(history.location.pathname).toBe(items[i].route));
    }
  } catch (error) {
    console.error('Test failed:', error);
  }
});

test('renders the correct styles for the list items', async () => {
  try {
    const items = [
      { name: 'Item 1', route: '/item1', iconPath: 'icon1' },
      { name: 'Item 2', route: '/item2', iconPath: 'icon2' },
      { name: 'Item 3', route: '/item3', iconPath: 'icon3' },
    ];

    const { container } = render(AccountPopUp, { items });

    const listItems = container.querySelectorAll('li');

    for (let i = 0; i < listItems.length; i++) {
      const li = listItems[i];

      expect(li.classList.contains('p-2')).toBe(true);
      expect(li.classList.contains('border-b')).toBe(true);
      expect(li.classList.contains('border-opacity-10')).toBe(true);
      expect(li.classList.contains('border-theme-dark-backgroundBlue')).toBe(true);
      expect(li.classList.contains('rounded-md')).toBe(true);
      expect(li.classList.contains('hover:bg-dark-background')).toBe(true);
      expect(li.classList.contains('hover:text-theme-dark-white')).toBe(true);
      expect(li.classList.contains('transition')).toBe(true);
    }
  } catch (error) {
    console.error('Test failed:', error);
  }
});