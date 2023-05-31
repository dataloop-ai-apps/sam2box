import os
from multiprocessing.pool import ThreadPool
import dtlpy as dl
import logging
import tqdm
from segment_anything import build_sam, SamAutomaticMaskGenerator
import cv2
import requests

logger = logging.getLogger(name=__name__)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

building_with_model_included_in_docker = True

if dl.token_expired():
    dl.login()

class ServiceRunner(dl.BaseServiceRunner):
    """
    Service runner class

    """

    def __init__(self, sam_checkpoint):
        """
        Load the model
        """
        logger.info('set up model')

        if building_with_model_included_in_docker:
            logger.debug(f'Trying to get model snapshot from {sam_checkpoint}')
            logger.debug(f'These files are present: {os.listdir(os.path.dirname(sam_checkpoint))}')
            self.checkpoint = sam_checkpoint
        else:
            params = {'stream':True}
            response = requests.get(sam_checkpoint, params=params)

            self.checkpoint = sam_checkpoint.split('/')[-1]
            totalbits = 0
            if response.status_code == 200:
                with open(self.checkpoint, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            totalbits += 1024
                            logger.debug(f"Downloaded {totalbits*1025}KB")
                            f.write(chunk)
            else:
                logger.error(f'Error message while downlading: {response.status_code}')
                raise ValueError('requests failed to download model')
        
        self.mask_generator = SamAutomaticMaskGenerator(
        model=build_sam(checkpoint=self.checkpoint),
        points_per_side=16,
        pred_iou_thresh=0.9,
        stability_score_thresh=0.92,
        crop_n_layers=1,
        crop_n_points_downscale_factor=2,
        min_mask_region_area=100,  # Requires open-cv to run post-processing
        )
        self.mask_generator = SamAutomaticMaskGenerator(build_sam(checkpoint=self.checkpoint))
        # self.max_masks = 500

        logger.info('model set up')


    def segment_item(self, item: dl.Item):
        annotations = self.return_annotations(item=item)

        item.annotations.upload(annotations=annotations)
        item = item.update()

        logger.info(f'uploaded {len(annotations)} annotations for item {item.name}')

        return item


    def return_annotations(self, item: dl.Item):
        file = cv2.imread(item.download())

        masks = self.mask_generator.generate(file)

        # add annotations
        builder = item.annotations.builder()
        for idx, mask in enumerate(masks):
            # if idx == self.max_masks:
            #     break
            logger.debug(f'add segmantic mask {idx} with confidence {mask["predicted_iou"]}')

            label = "mask.{:03d}".format(idx)
            
            box = mask['bbox']
            print(box)
            # mask = (ann_arr==idc).astype(np.uint8)
            builder.add(annotation_definition=dl.Box(left=box[0], top=box[1], right = box[0]+box[2], 
                                                     bottom = box[1]+box[3],label=label) ,
                        # (geo=mask['segmentation'], label=label),
                model_info={'name': self.checkpoint, 'confidence': mask["predicted_iou"]})

        
        # return builder.to_json()['annotations'], overall_conf
        return builder.to_json()['annotations']
        
    def annotate_dataset(self, dataset: dl.Dataset, query=None):

        try:
            filters = dl.Filters(resource=dl.FiltersResource.ITEM, custom_filter=query)
            pages = dataset.items.list(filters=filters)
            if pages.items_count == 0:
                logger.info("No item has been found")

            pool = ThreadPool(processes=32)
            pbar = tqdm.tqdm(total=pages.items_count)

            for i_item, item in enumerate(pages.all()):
                pool.apply_async(
                    self.score_and_upload(item))
            pool.close()
            pool.join()
            pool.terminate()
        except Exception as r:
            logging.exception('ERROR: dataset id: {}: {}'.format(dataset.id, r))
        finally:
            logging.info('done')
