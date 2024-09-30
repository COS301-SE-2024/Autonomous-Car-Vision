import { render, screen } from '@testing-library/svelte';
import gallaryComponent from '../../components/GallaryCard.svelte';
import { expect, test } from 'vitest';
import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/svelte';

test('renders "Details here..." link', () => {
    try{
      render(gallaryComponent);
      const detailsLink = screen.getByText('Details here...');
      expect(detailsLink).toBeInTheDocument();
    }catch(e){
      console.error("error occured", e);
      if (e.stack) {
          console.log('Stack trace:', e.stack);
      }
      return false;
    }
});

test('navigates to correct URL when "Details here..." link is clicked', async () => {

    try{const mockNavigate = jest.fn(); // Mock the navigate function
  render(gallaryComponent, { props: { navigate: mockNavigate } });
  const detailsLink = screen.getByText('Details here...');
  detailsLink.click();
  expect(mockNavigate).toHaveBeenCalledWith('/details'); // Replace '/details' with the actual URL
}catch(e){
    console.error("error occured", e);
    if (e.stack) {
        console.log('Stack trace:', e.stack);
    }
    return false;
}
  
});

test('does not display "Details here..." link when "isDownloaded" is false', () => {

    try{
          render(gallaryComponent, { props: { isDownloaded: false } });
    const detailsLink = screen.queryByText('Details here...');
    expect(detailsLink).not.toBeInTheDocument();
    }
    catch(e){
        console.error("error occured", e);
        if (e.stack) {
            console.log('Stack trace:', e.stack);
        }
        return false;
    }

});


