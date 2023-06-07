# Segment Anything (SAM2BOX) Faas
In this repository, you will be creating a FAAS that utilizes Meta's Segment Anything Model (SAM) to automatically generate masks for a given image and return contained bounding boxes. The original SAM repository can be found in the following link: https://github.com/facebookresearch/segment-anything


Audience: This example is meant for people with a working knowledge of Python and a use-case where auto-segmentation would streamline their processes.

## Installation & Instructions:
The code requires python>=3.8, as well as pytorch>=1.7 and torchvision>=0.8, installing both PyTorch and TorchVision with CUDA support is strongly recommended. Please ensure DTLPY - the Dataloop SDK - is installed as well as the Segment Anything library. All required packages are detailed in the 'requirements.txt' located in the 'code' folder. The 'code' folder also includes the necessary Python files to deploy the SAM-2-BOX Faas within your Dataloop project. Below are the steps needed to deploy SAM2Box faas:

1. Download the code folder
2. Install all dependancies by running the following command: pip install -r requirements.txt
3. Include a package name and specify the project where the service will be deployed in the "create_service" file
5. Add the same package name in the "modules_definition" file
6. Deploy the faas by running the "create_service" file


## Video Demonstration:

<a href="https://app.guidde.com/playbooks/playlist/qNS8Jye28AJFMe3faHoTkD?origin=5t6jUg49oKbdkAHbb3uDjMR9MDr2&active=0" rel="noreferrer noopener">![Video Demonstrations](https://github.com/dataloop-ai-apps/sam2box/blob/main/images/StartOfVideo.png)</a>

The video demonstrations will walk you through the following 4-step process:

1. Deploying the Sam2Box Faas on your particular project
2. Creating a 2-node pipleine: Dataset and the Sam2Box faas 
3. Running an instance: once an item is uploaded in your specified dataset, it is fed into the faas where SAM will automatically generate the semantic masks and return their respective bounding boxes
4. Final BB outputs are uploaded to the original image and can be viewed in the dataset.


## References:
```sh
  @article{kirillov2023segany,
  title={Segment Anything},
  author={Kirillov, Alexander and Mintun, Eric and Ravi, Nikhila and Mao, Hanzi and Rolland, Chloe and Gustafson, Laura and Xiao, Tete and Whitehead, Spencer and Berg, Alexander C. and Lo, Wan-Yen and Doll{\'a}r, Piotr and Girshick, Ross},
  journal={arXiv:2304.02643},
  year={2023}
}
  ```

