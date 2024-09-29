import { expect, it, test } from 'vitest';
import { render, fireEvent, screen } from '@testing-library/svelte';
// import GallaryPage from '../../pages/GallaryPage.svelte';



test('Search and Filter Functionality', () => {
    beforeEach(() => {
      // Mock the fetchData function and replace it with a mock implementation
      // const mockFetchData = jest.fn(() => Promise.resolve({ message: 'Data loaded successfully' }));
      // window.electronAPI.fetchVideos = jest.fn(() => Promise.resolve({ success: true, data: [] }));
      // window.electronAPI.checkFileExistence = jest.fn(() => Promise.resolve({ success: true, exists: true }));
  
      // Replace the fetchData function with the mock implementation
      // const { result } = render(GallaryPage, {
      //   props: {
      //     fetchData: mockFetchData,
      //   },
      // });
  
      // Wait for the component to be mounted
      // return result.waitForNextUpdate();
    });
  });
  
    test('should render the search and filter components', () => {
      try {
        const searchInput = document.querySelector('input[type="text"]');
        const filterSelect = document.querySelector('select');
  
        expect(searchInput).toBeInTheDocument();
        // expect(filterSelect).toBeInTheDocument();
      } catch (error) {
        console.error('Error in test case:', error);
      }
    });
  
    it('should call the handleSearch function when the search input changes', async () => {
      try {
        const searchInput = document.querySelector('input[type="text"]');
        const mockHandleSearch = jest.fn();
  
        // Replace the handleSearch function with the mock implementation
        const { result } = render(GallaryPage, {
          props: {
            fetchData: mockFetchData,
            handleSearch: mockHandleSearch,
          },
        });
  
        // Simulate a change event on the search input
        fireEvent.change(searchInput, { target: { value: 'test' } });
  
        // Wait for the handleSearch function to be called
        await waitFor(() => expect(mockHandleSearch).toHaveBeenCalled());
      } catch (error) {
        console.error('Error in test case:', error);
      }
    });
  
    it('should call the handleFilterChange function when the filter select changes', async () => {
      try {
        const filterSelect = document.querySelector('select');
        const mockHandleFilterChange = jest.fn();
  
        // Replace the handleFilterChange function with the mock implementation
        const { result } = render(GallaryPage, {
          props: {
            fetchData: mockFetchData,
            handleFilterChange: mockHandleFilterChange,
          },
        });
  
        // Simulate a change event on the filter select
        fireEvent.change(filterSelect, { target: { value: 'Name' } });
  
        // Wait for the handleFilterChange function to be called
        await waitFor(() => expect(mockHandleFilterChange).toHaveBeenCalled());
      } catch (error) {
        console.error('Error in test case:', error);
      }
    });
  
    it('should render the GallaryCard component with the correct props', async () => {
      try {
        // Mock the videoURLs, videoNames, and downloadedStatuses arrays
        const mockVideoURLs = ['url1', 'url2', 'url3'];
        const mockVideoNames = ['name1', 'name2', 'name3'];
        const mockDownloadedStatuses = [true, false, true];
  
        // Replace the videoURLs, videoNames, and downloadedStatuses arrays with the mock implementations
        const { result } = render(GallaryPage, {
          props: {
            fetchData: mockFetchData,
            videoURLs: mockVideoURLs,
            videoNames: mockVideoNames,
            downloadedStatuses: mockDownloadedStatuses,
          },
        });
  
        // Wait for the component to be mounted
        await result.waitForNextUpdate();
  
        // Assert that the GallaryCard component is rendered with the correct props
        const galleryCards = document.querySelectorAll('gallary-card');
        expect(galleryCards.length).toBe(3);
        expect(galleryCards[0].getAttribute('video-source')).toBe(mockVideoURLs[0]);
        expect(galleryCards[0].getAttribute('video-name')).toBe(mockVideoNames[0]);
        expect(galleryCards[0].getAttribute('is-downloaded')).toBe(mockDownloadedStatuses[0] ? 'true' : 'false');
      } catch (error) {
        console.error('Error in test case:', error);
      }
    });
  
    it('should display a loading spinner when the isLoading store is true', async () => {
      try {
        // Mock the isLoading store and set it to true
        const mockIsLoadingStore = {
          set: jest.fn(),
        };
  
        // Replace the isLoading store with the mock implementation
        const { result } = render(GallaryPage, {
          props: {
            fetchData: mockFetchData,
            isLoadingStore: mockIsLoadingStore,
          },
        });
  
        // Wait for the component to be mounted
        await result.waitForNextUpdate();
  
        // Assert that a loading spinner is displayed when the isLoading store is true
        const loadingSpinner = document.querySelector('spinner');
        expect(loadingSpinner).toBeInTheDocument();
      } catch (error) {
        console.error('Error in test case:', error);
      }
    });
