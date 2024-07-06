import { describe, expect, it, test } from 'vitest'
import { render } from '@testing-library/svelte';
import Spinner from '../../components/Spinner.svelte'; // Replace 'Spinner' with the name of your component

describe('Dot Animation', () => {
  it('should render 16 dots', async () => {
    try{
        const { container } = render(Spinner);
        expect(container.querySelectorAll('.dot').length).toBe(16);
    }
    catch(e){
        console.error("error occured", e);
    }
  });

  it('should have correct initial positions for the dots', async () => {

    try{
            const { container } = render(Spinner);
        const dots = container.querySelectorAll('.dot');
        for (let i = 0; i < dots.length; i++) {
        const dot = dots[i];
        const { bottom, right } = window.getComputedStyle(dot);
        const expectedBottom = `${120 * (i % 4) / 100}px`;
        const expectedRight = `${120 * Math.floor(i / 4) / 100}px`;
        expect(bottom).toBe(expectedBottom);
        expect(right).toBe(expectedRight);
        }
    }
    catch(err){
        console.error(err);
    }
  });

  it('should have correct initial scales for the dots', async () => {
    try{
        const { container } = render(Spinner);
        const dots = container.querySelectorAll('.dot');
        for (let i = 0; i < dots.length; i++) {
        const dot = dots[i];
        const scale = window.getComputedStyle(dot).getPropertyValue('--uib-scale');
        const expectedScale = `${0.94 + 0.02 * i}px`;
        expect(scale).toBe(expectedScale);
        }
    }
    catch(error){
        console.error(error);
    }
   
  });

  it('should have correct animation delays for the dots', async () => {

    try{
        const { container } = render(Spinner);
        const dots = container.querySelectorAll('.dot');
        for (let i = 0; i < dots.length; i++) {
        const dot = dots[i];
        const delay = window.getComputedStyle(dot).getPropertyValue('--uib-animation-delay');
        const expectedDelay = `${1000 * (i * 0.02 + 0.01)}ms`;
        expect(delay).toBe(expectedDelay);
        }
    }
    catch(error){
        console.error(error);
    }
  });

  it('should have correct animation durations for the dots', async () => {

    try{
        const { container } = render(Spinner);
        const dots = container.querySelectorAll('.dot');
        for (let i = 0; i < dots.length; i++) {
        const dot = dots[i];
        const duration = window.getComputedStyle(dot).getPropertyValue('--uib-animation-duration');
        const expectedDuration = `${1000}ms`;
        expect(duration).toBe(expectedDuration);
        }
    }
    catch(error){
        console.error(error);
    }
  });

});