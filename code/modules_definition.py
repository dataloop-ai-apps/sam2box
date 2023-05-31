import dtlpy as dl
import json

package_name = "segment-anything" # docker built-in
# package_name = "segment-anything-nodocker" # no docker built-in

def generate_package_json(package_name):
    package = {
        "name": package_name,
        "modules": [module.to_json() for module in get_modules()]
    }

    with open('package.json', 'w', encoding='utf-8') as f:
        json.dump(package, f, indent=4)


def get_modules():
    module = dl.PackageModule(
        name=package_name,
        entry_point='main.py',
        init_inputs=[
            dl.FunctionIO(name='sam_checkpoint', type=dl.PackageInputType.STRING)
        ],
        functions=[
            dl.PackageFunction(
                name='return_annotations',
                inputs=[
                    dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM)
                ],
                outputs=[
                    dl.FunctionIO(name='annotations', type=dl.PackageInputType.ANNOTATIONS)
                ],

                description='segments an image with sam'
            ),
            dl.PackageFunction(
                name='segment_item',
                inputs=[
                    dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM)
                ],
                outputs=[
                    dl.FunctionIO(name='item', type=dl.PackageInputType.ITEM)
                ],

                description='segments an image with sam and uploads annotations'
            ),
            dl.PackageFunction(
                name='annotate_dataset',
                inputs=[
                    dl.FunctionIO(name='dataset', type=dl.PackageInputType.DATASET),
                    dl.FunctionIO(name='query', type=dl.PackageInputType.JSON)
                ],

                description='segments images in a dataset with sam and uploads annotations'
            )
        ]
    )
    return [module]




def get_slots():
    slots = [
            # dl.PackageSlot(
            #     function_name='score',
            #     module_name=package_name,
            #     display_name='Segment with sam',
            #     display_icon='fas fa-exchange-alt',
            #     display_scopes=[dl.SlotDisplayScope(resource=dl.SlotDisplayScopeResource.ITEM,filters={})],
            #     post_action=dl.SlotPostAction(dl.SlotPostActionType.DRAW_ANNOTATION)
            # ),

            dl.PackageSlot(
                function_name='annotate_dataset',
                module_name=package_name,
                display_name='Segment with sam',
                display_icon='fas fa-exchange-alt',
                display_scopes=[dl.SlotDisplayScope(resource=dl.SlotDisplayScopeResource.DATASET_QUERY,filters={})]
            )
        ]

    return slots