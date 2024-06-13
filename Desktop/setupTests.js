// setupTests.js
// import '@testing-library/jest-dom';
// import { vi } from 'vitest';

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

// global.document = {
//   createElement: () => ({
//     setAttribute: vi.fn(),
//     getAttribute: vi.fn(),
//   }),
// };
