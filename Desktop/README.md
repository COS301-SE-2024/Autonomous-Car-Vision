# Ensure you have Yarn installed: 
cd Desktop
corepack enable

# If on Linux
sudo npm i --force

# Ensure you have the correct version of yarn:
yarn set version stable

# install dependancies: (Use sudo if on Linux)
yarn install

# to run rollup: 
yarn run rollup -c -w

# To start electron: (in new terminal):
yarn electron .
