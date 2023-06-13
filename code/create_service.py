from modules_definition import get_modules, get_slots
import dtlpy as dl
import pathlib

project_name = '' # INSERT PROJECT NAME 
package_name = " " # INSERT PACKAGE NAME

if dl.token_expired():
    dl.login()

new_package_deployment = True  # True if new package need to be deployed

project = dl.projects.get(project_name=project_name)


###############
#   package   #
###############


def deploy_service():
    src_path = str(pathlib.Path('.').resolve())

    if new_package_deployment:
        package = project.packages.push(package_name=package_name,
                                        modules=get_modules(),
                                        src_path=src_path,
                                        slots=get_slots())
        print('New Package has been deployed')
    else:
        package = project.packages.get(package_name=package_name)
        print('Got last package')

    ###############
    #     bot     #
    ###############

    try:
        bot = project.bots.get(bot_name=package.name)
        print("Package {} Bot {} {} has been gotten".format(package.name, bot.name, bot.email))
    except dl.exceptions.NotFound:
        bot = project.bots.create(name=package.name)
        print("New bot has been created: {} email: {}".format(bot.name, bot.email))

    ###########
    # service #
    ###########

    try:
        service = package.services.get(service_name=package_name)
        print("Service has been gotten: ", service.name)
    except dl.exceptions.NotFound as e:
        runtime = dl.KubernetesRuntime(num_replicas=1,
                                            concurrency=10,
                                            runner_image = 'dataloopai/sam2box:gpu.cuda.11.8.py3.8.pytorch2', # model built-in
                                            pod_type=dl.InstanceCatalog.GPU_K80_M,
                                            autoscaler=dl.KubernetesRabbitmqAutoscaler(
                                                minReplicas=1,
                                                max_replicas=1,
                                                queue_length=10))
        init_input=[
            dl.FunctionIO(name='sam_checkpoint',
                            type=dl.PackageInputType.STRING,
                            value="/tmp/models/sam_vit_h_4b8939.pth") # model built-in
        ]

        service = package.services.deploy(service_name=package_name,
                                          module_name=package_name,
                                          init_input=init_input,
                                          runtime=runtime)


        print("New service has been created: ", service.name)

    print("package.version: ", package.version)
    print("service.package_revision: ", service.package_revision)
    print("service.runtime.concurrency: ", service.runtime.concurrency)
    service.runtime.autoscaler.print()

    if package.version != service.package_revision:
        service.package_revision = package.version
        service.update()
        print("service.package_revision has been updated: ", service.package_revision)

    else:
        print('No need to update service.package_revision')


if __name__ == "__main__":
    deploy_service()
