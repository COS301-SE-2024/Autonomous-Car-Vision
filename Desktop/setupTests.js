// setupTests.js
import '@testing-library/jest-dom/vitest';
import { vi } from 'vitest';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';

// Mock axios for tests
const mock = new MockAdapter(axios);
mock.onGet("http://localhost:8000/devLogin/").reply(200, {
  token: 'mock-token',
  uid: 'mock-uid',
  uname: 'mock-uname',
  uemail: 'mock-uemail'
});

global.window = {
  electronAPI: {
    storeToken: vi.fn(),
    getToken: vi.fn(() => 'mock-token'),  // Mock return value if needed
    clearToken: vi.fn(),
    storeUname: vi.fn(),
    getUname: vi.fn(() => 'mock-uname'),  // Mock return value if needed
    clearUname: vi.fn(),
    storeUid: vi.fn(),
    getUid: vi.fn(() => 'mock-uid'),  // Mock return value if needed
    clearUid: vi.fn(),
    storeUemail: vi.fn(),
    getUemail: vi.fn(() => 'mock-uemail'),  // Mock return value if needed
    clearUemail: vi.fn(),
    hashPassword: vi.fn(),
    hashPasswordSalt: vi.fn(),
    insertData: vi.fn(),
    selectData: vi.fn(),
    updateData: vi.fn(),
    uploadFile: vi.fn(),
    openFileDialog: vi.fn(),
    fetchVideos: vi.fn(),
  },
  location: {
    href: 'http://localhost',
    origin: 'http://localhost',
  },
};
