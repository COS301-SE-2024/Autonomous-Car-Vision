// import { render, screen } from '@testing-library/svelte';
// import gallaryComponent from '../../components/GallaryCard.svelte';
// import { expect, test } from 'vitest';
// import '@testing-library/jest-dom';
// import { render, screen } from '@testing-library/svelte';

// test('renders "Details here..." link', () => {
//     try{
//       render(gallaryComponent);
//       const detailsLink = screen.getByText('Details here...');
//       expect(detailsLink).toBeInTheDocument();
//     }catch(e){
//       console.error("error occured", e);
//       if (e.stack) {
//           console.log('Stack trace:', e.stack);
//       }
//       return false;
//     }
// });

// test('navigates to correct URL when "Details here..." link is clicked', async () => {

//     try{const mockNavigate = jest.fn(); // Mock the navigate function
//   render(gallaryComponent, { props: { navigate: mockNavigate } });
//   const detailsLink = screen.getByText('Details here...');
//   detailsLink.click();
//   expect(mockNavigate).toHaveBeenCalledWith('/details'); // Replace '/details' with the actual URL
// }catch(e){
//     console.error("error occured", e);
//     if (e.stack) {
//         console.log('Stack trace:', e.stack);
//     }
//     return false;
// }
  
// });

// test('does not display "Details here..." link when "isDownloaded" is false', () => {

//     try{
//           render(gallaryComponent, { props: { isDownloaded: false } });
//   const detailsLink = screen.queryByText('Details here...');
//   expect(detailsLink).not.toBeInTheDocument();
//     }
//     catch(e){
//         console.error("error occured", e);
//         if (e.stack) {
//             console.log('Stack trace:', e.stack);
//         }
//         return false;
//     }

// });

import { describe, expect, it, test } from 'vitest'

test("testing something", () => {
    expect(1 + 2).toBe(3)
})

describe("TESTING MULTIPLE", () => {
    it("1 + 1", () => {
        expect(1+1).toBe(2)
    })

    it("2 * 2", () => {
        expect(2 * 2).toBe(4)
    })
})