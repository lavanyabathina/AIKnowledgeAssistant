from loaders.webdocument_generator import create_dataset_from_web
from loaders.localdocument_generator import create_dataset_from_local

async def generate_dataset(dataset_config):
    datasets = dataset_config["datasets"]
    for dataset in datasets:
        if dataset["type"] == "web":
            print("Source is from web");
            print("Source name:" , dataset["name"])
            await create_dataset_from_web (dataset["name"],dataset["path"])
        elif dataset["type"] == "local":
            print("Source is from local");
            print("Dataset is present in local source by default")
            await create_dataset_from_local (dataset["path"])
