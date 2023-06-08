from pydantic import BaseModel
from src.utils import calculate_checksum


class IngestLargeDataset:
    def __init__(self, repo, logger):
        self.repo = repo
        self.logger = logger

    class Inputs(BaseModel):
        name: str
        path: str = None
        user: dict

    class Outputs(BaseModel):
        dataset: dict

    def __call__(self, inputs: Inputs) -> Outputs:
        # allow only zip files
        if not inputs.path.endswith(".zip"):
            raise Exception("Only zip files are allowed")
        self.logger("Computing checksum...")
        checksum = calculate_checksum(inputs.path)
        self.logger(checksum)
        self.logger("Ingesting dataset...")
        id_token = inputs.user["id_token"]
        dataset_id, upload_id = self.repo.prepare_large_upload(
            inputs.name, id_token, checksum
        )
        self.repo.ingest_large_dataset(
            inputs.path,
            1024 * 1024 * 10,
            upload_id,
            dataset_id,
            id_token,
        )
        # data, error = self.repo.complete_upload(
        #     inputs.name, id_token, upload_id, dataset_id, checksum
        # )
        # if error:
        #     raise Exception(error)
        # self.logger("Done")
        # return self.Outputs(dataset=data)
        return
