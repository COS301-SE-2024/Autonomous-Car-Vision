# Ensure you have Yarn installed: 
cd Desktop
corepack enable

# Ensure you have the correct version of yarn:
yarn set version stable
yarn install

# install dependancies: 
yarn install

# to run rollup: 
yarn run rollup -c -w

# To start electron: (in new terminal):
yarn electron .