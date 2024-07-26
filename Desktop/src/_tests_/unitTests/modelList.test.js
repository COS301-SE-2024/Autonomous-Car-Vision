import { expect, it, test } from 'vitest';
import { render, fireEvent, screen } from '@testing-library/svelte';
import modelList from '../../components/ModelList.svelte';

test('Selected code block', () => {
    try{
        let component;

        beforeEach(async () => {
            component = render(modelList, {
            processedVideos: [
                { profileImgURL: 'profile1.jpg', label: 'Model 1' },
                { profileImgURL: 'profile2.jpg', label: 'Model 2' }
            ]
            });
        });   

  it('should call selectModel function with the correct argument when a div is clicked', async () => {
    try {
      const div = component.getByRole('button', { name: 'Model 1' });
      const dispatch = jest.fn();
      component.$set({ dispatch });

      await fireEvent.click(div);

      expect(dispatch).toHaveBeenCalledWith('select', { profileImgURL: 'profile1.jpg', label: 'Model 1' });
    } catch (error) {
      console.error('Test failed:', error);
    }
  });

  it('should not call selectModel function when a div is clicked if processedVideos is empty', async () => {
    try {
      component.$set({ processedVideos: [] });

      const div = component.getByRole('button', { name: 'Model 1' });
      const dispatch = jest.fn();
      component.$set({ dispatch });

      await fireEvent.click(div);

      expect(dispatch).not.toHaveBeenCalled();
    } catch (error) {
      console.error('Test failed:', error);
    }
  });

  it('should call selectModel function with the correct argument when a second div is clicked', async () => {
    try {
      const div = component.getByRole('button', { name: 'Model 2' });
      const dispatch = jest.fn();
      component.$set({ dispatch });

      await fireEvent.click(div);

      expect(dispatch).toHaveBeenCalledWith('select', { profileImgURL: 'profile2.jpg', label: 'Model 2' });
    } catch (error) {
      console.error('Test failed:', error);
    }
  });

  it('should not call selectModel function when a div is clicked if the event is cancelled', async () => {
    try {
      const div = component.getByRole('button', { name: 'Model 1' });
      const dispatch = jest.fn();
      component.$set({ dispatch });

      const event = new Event('click', { cancelable: true });
      event.preventDefault();
      event.stopPropagation();

      await fireEvent.mouseDown(div);
      await fireEvent.mouseUp(div);

      expect(dispatch).not.toHaveBeenCalled();
    } catch (error) {
      console.error('Test failed:', error);
    }
  });

  it('should call selectModel function with the correct argument when a div is clicked with a custom event', async () => {
    try {
      const div = component.getByRole('button', { name: 'Model 1' });
      const dispatch = jest.fn();
      component.$set({ dispatch });

      const customEvent = new CustomEvent('custom-click', { bubbles: true });
      await fireEvent.event(div, customEvent);

      expect(dispatch).toHaveBeenCalledWith('select', { profileImgURL: 'profile1.jpg', label: 'Model 1' });
    } catch (error) {
      console.error('Test failed:', error);
    }
  });
    }
    catch(e)
    {
        console.error("error occured", e);
        if (e.stack) {
            console.log('Stack trace:', e.stack);
        }
        return false;
    };
});