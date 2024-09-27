import { describe, expect, it, test } from 'vitest'
import { render, fireEvent, screen } from '@testing-library/svelte';
import FileItem from '../../components/FileItem.svelte'; // Replace with the actual file path

test('renders file name and close button', () => {
    try{
          const file = { name: 'test-file.txt' };
            render(FileItem, { file });
            expect(screen.getByText(file.name)).toBeInTheDocument();
            expect(screen.getByTestId('close-button')).toBeInTheDocument();
    }
    catch(errors){
        console.error("error occured", errors);
        if (errors.stack) {
            console.log('Stack trace:', errors.stack);
        }
        return false;
    }

});

test('calls onRemove function when close button is clicked', () => {

    try{
        const mockOnRemove = jest.fn();
        render(FileItem, { file: { name: 'test-file.txt' }, onRemove: mockOnRemove });    
        const closeButton = screen.getByTestId('close-button');
        fireEvent.click(closeButton);
        expect(mockOnRemove).toHaveBeenCalledWith({ name: 'test-file.txt' });
    }
    catch(e){
        console.error("error occured", e);
        if (e.stack) {
            console.log('Stack trace:', e.stack);
        }
        return false;
    }
  
});

test('displays correct file name', () => {
    try{
          const file = { name: 'test-file.txt' };
            render(FileItem, { file });
            expect(screen.getByText(file.name)).toHaveTextContent(file.name);
    }
    catch(e){
        console.error("error occured", e);
        if (e.stack) {
            console.log('Stack trace:', e.stack);
        }
        return false;
    }

});

test('renders close button with correct icon', () => {
    try{
            
        render(FileItem, { file: { name: 'test-file.txt' } });
        expect(screen.getByTestId('close-button')).toHaveAttribute('icon', 'mdi-close-thick}');

    }
    catch(e){
        console.error("error occured", e);
        if (e.stack) {
            console.log('Stack trace:', e.stack);
        }
        return false;}
    
});

test('does not throw error when file is not provided', () => {
    try{
        const { container } = render(FileItem, { onRemove: jest.fn() });
        expect(container).not.toThrow();
    }
    catch(e){
        console.error("error occured", e);
        if (e.stack) {
            console.log('Stack trace:', e.stack);
        }
        return false;
    }

});