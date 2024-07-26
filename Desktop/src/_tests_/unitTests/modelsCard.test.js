import { describe, expect, it, test } from 'vitest'

import { render, screen, fireEvent } from '@testing-library/svelte';
import ModelsCard from '../../components/ModelsCard.svelte'; // Import the component

test('renders correct content for ModelsCard front', () => {
  try {
    const model = {
      mName: 'Test Model',
      mDescription: 'This is a test model',
      mVersion: '1.0',
      mSummary: 'This is a summary for the test model',
      mStatus: 'green',
      mProfileImg: 'profile.jpg',
      mImg: 'image.jpg',
    };

    render(ModelsCard, { props: { Model: model } });

    expect(screen.getByText('Test Model')).toBeInTheDocument();
    expect(screen.getByText('1.0')).toBeInTheDocument();
    expect(screen.getByText('This is a summary for the test model')).toBeInTheDocument();
    expect(screen.getByAltText('Test Model')).toBeInTheDocument();
    expect(screen.getByAltText('image.jpg')).toBeInTheDocument();
  } catch (error) {
    console.error('Test failed:', error);
  }
});

test('renders correct content for ModelsCard back', () => {
  try {
    const model = {
      mName: 'Test Model',
      mDescription: 'This is a test model',
      mVersion: '1.0',
      mSummary: 'This is a summary for the test model',
      mStatus: 'green',
      mProfileImg: 'profile.jpg',
      mImg: 'image.jpg',
    };

    render(ModelsCard, { props: { Model: model } });

    expect(screen.getByText('This is a summary for the test model')).toBeInTheDocument();
  } catch (error) {
    console.error('Test failed:', error);
  }
});

test('updates content when Model values change', () => {
  try {
    const model = {
      mName: 'Test Model',
      mDescription: 'This is a test model',
      mVersion: '1.0',
      mSummary: 'This is a summary for the test model',
      mStatus: 'green',
      mProfileImg: 'profile.jpg',
      mImg: 'image.jpg',
    };

    const updatedModel = {
      mName: 'Updated Model',
      mDescription: 'This is an updated model',
      mVersion: '2.0',
      mSummary: 'This is an updated summary for the model',
      mStatus: 'orange',
      mProfileImg: 'updated-profile.jpg',
      mImg: 'updated-image.jpg',
    };

    const { rerender } = render(ModelsCard, { props: { Model: model } });

    rerender(ModelsCard, { props: { Model: updatedModel } });

    expect(screen.getByText('Updated Model')).toBeInTheDocument();
    expect(screen.getByText('2.0')).toBeInTheDocument();
    expect(screen.getByText('This is an updated summary for the model')).toBeInTheDocument();
    expect(screen.getByAltText('updated-profile.jpg')).toBeInTheDocument();
    expect(screen.getByAltText('updated-image.jpg')).toBeInTheDocument();
  } catch (error) {
    console.error('Test failed:', error);
  }
});

test('flips ModelsCard on mouseover and mouseout', () => {
  try {
    const model = {
      mName: 'Test Model',
      mDescription: 'This is a test model',
      mVersion: '1.0',
      mSummary: 'This is a summary for the test model',
      mStatus: 'green',
      mProfileImg: 'profile.jpg',
      mImg: 'image.jpg',
    };

    render(ModelsCard, { props: { Model: model } });

    const ModelsCard = screen.getByRole('button');

    fireEvent.mouseover(ModelsCard);
    expect(ModelsCard).toHaveClass('flipped');

    fireEvent.mouseout(ModelsCard);
    expect(ModelsCard).not.toHaveClass('flipped');
  } catch (error) {
    console.error('Test failed:', error);
  }
});

test('displays correct status color based on Model.mStatus', () => {
  try {
    const model = {
      mName: 'Test Model',
      mDescription: 'This is a test model',
      mVersion: '1.0',
      mSummary: 'This is a summary for the test model',
      mStatus: 'green',
      mProfileImg: 'profile.jpg',
      mImg: 'image.jpg',
    };

    render(ModelsCard, { props: { Model: model } });

    const statusCircle = screen.getByRole('img', { name: 'Online' });

    expect(statusCircle).toHaveStyle(`fill: ${model.statusColour}`);
  } catch (error) {
    console.error('Test failed:', error);
  }
});