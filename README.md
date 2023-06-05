# SAM2BOX: 
In this repository, you will be creating a FAAS that utilizes Meta's Segment Anything Model (SAM) to automatically generate masks for a given image and return contained bounding boxes. The original SAM repository can be found in the following link: https://github.com/facebookresearch/segment-anything


Audience: This example is meant for people with a working knowledge of Python and a use-case where auto-segmentation would streamline their processes.

## Installation & Instructions:
The code requires python>=3.8, as well as pytorch>=1.7 and torchvision>=0.8, installing both PyTorch and TorchVision with CUDA support is strongly recommended. Please ensure DTLPY - the Dataloop SDK - is installed as well as the Segment Anything library. All packages needed are detailed in the "requirements.txt" file located in the "code" folder.

The code folder includes the necessary Python files to deploy the SAM-2-BOX Faas within your Dataloop project. Please ensure to include specific project and package names in order to load the function correctly.


## Video Demonstration:

<video src='https://app.guidde.com/playbooks/playlist/a1wWTznUYk3Lz2XfNr7CnV?origin=5t6jUg49oKbdkAHbb3uDjMR9MDr2&active=0' width=100/>

https://app.guidde.com/playbooks/playlist/a1wWTznUYk3Lz2XfNr7CnV?origin=5t6jUg49oKbdkAHbb3uDjMR9MDr2&active=0 




## References:
```sh
  @article{kirillov2023segany,
  title={Segment Anything},
  author={Kirillov, Alexander and Mintun, Eric and Ravi, Nikhila and Mao, Hanzi and Rolland, Chloe and Gustafson, Laura and Xiao, Tete and Whitehead, Spencer and Berg, Alexander C. and Lo, Wan-Yen and Doll{\'a}r, Piotr and Girshick, Ross},
  journal={arXiv:2304.02643},
  year={2023}
}
  ```

