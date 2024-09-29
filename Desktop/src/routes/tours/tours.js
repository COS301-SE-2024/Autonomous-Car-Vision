// tours.js
export const tours = {
    viewGalleryTour: [
        {
          target: '.sideBar',
          content: 'Click on the Gallery tab on the sidebar.',
        },
        {
          target: '.screen',
          content: 'The gallery page will open and you can access your videos here.',
        },
      ],
      viewVideoTour: [
        {
          target: '.screen',
          content: 'On the gallery page, click on the video to view it.',
        },
        {
          target: '.notDownloaded',
          content: 'If the video is not downloaded on your local storage, it will be grey.',
        },
        {
          target: '.download-btn',
          content: 'Simply click on the download button, wait for it to download from our servers and you should be able to access the video.',
        },
      ],
      processVideoTour: [
        {
          target: '.process-btn',
          content: 'On the screen, click on the process button.',
        },
        {
          target: '.modal',
          content: 'Choose the model you want to use to process the video.',
        },
        {
        target: '.confirm',
        content: 'confirm the model and wait patiently as the AI does its work.',
        },
        {
        target: '.sideAview-btn',
        content: 'On the top left, click on the arrow button.',
        },
        {
        target: '.sideView',
        content: 'To view the different versions of the video that have been process, click on the model name.',
        },
        {
        target: '.screen',
        content: 'You can now see the process video',
        },
      ],
      viewModelsTour: [
        {
          target: '.sideBar',
          content: 'Click on the Models tab on the sidebar.',
        },
        {
          target: '.screen',
          content: 'You can view all the models on this page.',
        },
        {
          target: '.modelsMore',
          content: 'To view more details of a model, click the model to reveal the extended summary.',
        },
      ],
      accountSettingsTour: [
        {
          target: '.sideBar',
          content: 'Click on your username on the sidebar.',
        },
        {
          target: '.popUp',
          content: 'On the pop-up menu, click on the Account settings option.',
        },
        {
          target: '.screen',
          content: 'You can edit your details here, as well as change your profile picture on this page.',
        }, 
        {
          target: '.save-btn',
          content: 'Click here to save your new details.',
        },
      ],
    changePasswordTour: [
        {
          target: '.password-btn',
          content: 'On the account settings page, click on the change password button.',
        },
      {
        target: '.password-field',
        content: 'This is where you change your password.',
      },
      {
        target: '.submit-btn',
        content: 'Click here to save your new password.',
      },
    ],
    uploadTour: [
      {
        target: '.upload-btn',
        content: 'On the gallery page, click on the upload button on the top left of the screen.',
      },
      {
        target: '.modal',
        content: 'Choose a video from your file directory.',
      },
      {
        target: '.submit-btn',
        content: 'Click here to save your the video.',
      },
    ],
    driveGalleryTour: [
      {
        target: '.sideBar',
        content: 'On the sidebar, click on the Drive Gallery Tab.',
      },
      {
        target: '.screen',
        content: 'You can view all your drives here.',
      },
      {
        target: '.dashboard',
        content: 'Click on a drive to view the dashboard.',
      },
    //   add more for the weaver and the other features...
    ],
    pipesTour: [
      {
        target: '.sideBar',
        content: 'On the sidebar, click on the Pipes tab to open the page.',
      },
      {
        target: '.chooseModel-btn',
        content: 'Choose a model from by clicking this button.',
      },
      {
        target: '.screen',
        content: 'This is where you can edit the layers of your models.',
      },
      {
        target: '.save-btn',
        content: 'You can save your pipe here.',
      },
      {
        target: '.clear-btn',
        content: 'This button clears the pipeline and resets the page for you.',
      },
    ],
    visualizerTour: [
      {
        target: '.sideBar',
        content: 'On the sidebar, access the models visualizer on its tab.',
      },
      {
        target: '.screen',
        content: 'This is where you can upload an onnx file to view the AI model.',
      },
      {
        target: '.screen',
        content: 'Please visit https://netron.app  for more information.',
      },
    ],
    teamViewTour: [
      {
        target: '.sideBar',
        content: 'On the sidebar, open the teams drop down and click on the teams view tab. ',
      }, 
      {
        target: '.screen',
        content: 'Here you can view all the members in your team and their details.',
      },
      {
        target: '.invite-btn',
        content: 'Click here to invite people to join your team.',
      },
      {
        target: '.remove-btn',
        content: 'Click here to remove the member from your team.',
      },
    ],
    teamNetworkTour: [
      {
        target: '.sideBar',
        content: 'On the sidebar, open the teams network page via the teams drop down tab.',
      }, 
      {
        target: '.screen',
        content: 'Here you can view how your team network is set up.',
      },
      //add more here on team network
    ],
    themeTour: [
      {
        target: '.sideBar',
        content: 'Click on the theme toggler on the side bar.',
      },  
      {
        target: '.screen',
        content: 'The theme will update accordingly throughout the app.',
      },
    ],
    logoutTour: [
      {
        target: '.sideBar',
        content: 'Click on your username for more options.',
      },  
      {
        target: '.logout-btn',
        content: 'Click here to log out of the app.',
      },
    ],
    // Add more tours here
  };
  