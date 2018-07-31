CUDA installation on Ubuntu 18.04
=================================
```
wget https://developer.nvidia.com/compute/cuda/9.0/Prod/local_installers/cuda_9.0.176_384.81_linux-run

sudo sh cuda_9.0.176_384.81_linux-run --override --silent --toolkit

wget http://developer.download.nvidia.com/compute/redist/cudnn/v7.1.4/cudnn-9.0-linux-x64-v7.1.tgz

tar zxfv cudnn-9.0-linux-x64-v7.1.tgz
sudo cp cuda/include/cudnn.h /usr/local/cuda/include
sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*


sudo gedit ~/.bashrc
```
> Add this to end and save
```
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64"
export CUDA_HOME=/usr/local/cuda
```
```
source ~/.bashrc
sudo ldconfig
echo $CUDA_HOME
sudo apt-get install
```

please restart terminals & prompt
