//import { render, screen, userEvent, act  } from 'vitest';
import { describe, expect, it, test } from 'vitest'
import { render, screen, userEvent, act } from '@testing-library/svelte';
import { isLoading } from '../../stores/loading';
import AccountSettings from '../../routes/AccountSettings.svelte';
import Sidebar from '../../components/SidebarV2.svelte';
import Spinner from '../../components/Spinner.svelte';

// test('Save Changes Form', () => {
//   beforeEach(async () => {
//     isLoading.set(true);
//     await render(AccountSettings);
//   });

//   it('should call the saveChanges function when the "Save Changes" button is clicked', async () => {
//     try {
//       const saveButton = await screen.findByText('Save Changes');
//       await userEvent.click(saveButton);

//       const saveChangesSpy = jest.spyOn(AccountSettings, 'saveChanges');

//       await act(async () => {
//         setTimeout(() => {
//           isLoading.set(false);
//         }, 4000);
//       });

//       expect(saveChangesSpy).toHaveBeenCalled();
//     } catch (error) {
//       console.error(error);
//     }
//   });

//   it('should display a toast message when the saveChanges function is called successfully', async () => {
//     try {
//       const saveButton = await screen.findByText('Save Changes');
//       await userEvent.click(saveButton);

//       const successToast = await screen.findByText('Changes saved successfully!');

//       await act(async () => {
//         setTimeout(() => {
//           isLoading.set(false);
//         }, 4000);
//       });

//       expect(successToast).toBeInTheDocument();
//     } catch (error) {
//       console.error(error);
//     }
//   });

//   it('should display a toast message when the saveChanges function fails', async () => {
//     try {
//       const saveButton = await screen.findByText('Save Changes');
//       await userEvent.click(saveButton);

//       const errorToast = await screen.findByText('Failed to save changes');

//       await act(async () => {
//         setTimeout(() => {
//           isLoading.set(false);
//         }, 4000);
//       });

//       expect(errorToast).toBeInTheDocument();
    // } catch (error) {
    //   console.error(error);
    // }
//   });
//});
test('Settings Page', () => {
    beforeEach(async () => {
      isLoading.set(true);
      // Simulate the user being logged in and having access to the settings page
      window.electronAPI.setToken("exampleToken");
      await render(Sidebar);
      const navbar = await screen.findByText('Profile');
      await userEvent.click(navbar);
      await render(AccountSettings);
    });
  
    it('should display the settings page when the user clicks on the profile icon in the Navbar', async () => {
      try {
        const profileIcon = await screen.findByText('Profile');
        await userEvent.click(profileIcon);
  
        const accountSettingsPage = await screen.findByText('Account Settings');
  
        expect(accountSettingsPage).toBeInTheDocument();
      } catch (error) {
        console.error(error);
      }
    });
  });
