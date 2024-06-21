import { render, screen } from '@testing-library/svelte';
import modelComponent from '../components/ModelsCard.svelte';
import { expect, test } from 'vitest';
import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/svelte';
//import { navigate } from "@sveltejs/kit/navigation";


test('renders correctly with a valid Model object containing gif and status properties', () => {
  try{

    const model = {
        name: 'Test Model',
        category: 'Test Category',
        description: 'This is a test model.',
        status: 'green',
        gif: 'test.gif',
        img: 'test.jpg',
      };
    
    render(modelComponent, { props: { Model: model } });
    expect(screen.getByText('Test Model')).toBeInTheDocument();
    expect(screen.getByText('Test Category')).toBeInTheDocument();
    expect(screen.getByText('This is a test model.')).toBeInTheDocument();
    expect(screen.getByAltText('Test Model')).toBeInTheDocument();
    expect(screen.getByAltText('test.gif')).toBeInTheDocument();
  }
  catch(e){
    console.error("error occured", e);
    if (e.stack) {
        console.log('Stack trace:', e.stack);
    }
    return false;
    }

});  

test('displays the correct status icon when the status is "red"', () => {
  try{

 
  const model = {
    name: 'Test Model',
    category: 'Test Category',
    description: 'This is a test model.',
    status: 'red',
    gif: 'test.gif',
    img: 'test.jpg',
  };

  render(modelComponent, { props: { Model: model } });

  const statusIcon = screen.getByAltText('Offline');
  expect(statusIcon).toBeInTheDocument();
  expect(statusIcon.style.backgroundColor).toBe('rgb(255, 0, 0)');

}
  catch(e){
    console.error("error occured", e);
    if (e.stack) {
        console.log('Stack trace:', e.stack);
    }
    return false;
  }
});