from ...models import Dataset, STACDataset
from ...errors import DatasetDoesNotExistError, UserUnauthorizedError
from ...repos import DatasetsDBRepo


def retrieve(data):
    if data is None:
        raise DatasetDoesNotExistError()
    return Dataset(**data) if data["quality"] == 0 else STACDataset(**data)


def retrieve_dataset(dataset_id):
    repo = DatasetsDBRepo()
    data = repo.retrieve_dataset(dataset_id)
    return retrieve(data)


def retrieve_dataset_by_name(name):
    repo = DatasetsDBRepo()
    data = repo.find_one_dataset_by_name(name)
    return retrieve(data)


def retrieve_file(files_id, file_id):
    repo = DatasetsDBRepo()
    data = repo.retrieve_file(files_id, file_id)
    return data


def retrieve_owned_dataset(dataset_id, uid):
    dataset = retrieve_dataset(dataset_id)
    if dataset.uid != uid:
        raise UserUnauthorizedError()
    return dataset
