# Car Submission Pipeline`

`car-submission-pipeline` is a python utility meant to monitor and process inputs related to objects detection and vehicle status.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `car-submission-pipeline`.

```bash
pip install -r requirements.txt
```

## Usage

```python
#TODO
```

## Interview-related notes:
* I've chosen the postgres backend due it's high-level support for native JSON querying. However, I specifically chose an ORM library which can be moved to cloud support natively by changing environment variables, and can also be easily refactored to cloud-native DBs in case greater scale is needed, or we need to go full noSQL.
* I've set this up to be stateless, to allow deployments such as a Kubernetes `CronJobs` or as a serverless function
* I am assuming the DB schema will not change frequently, as such, db "migrations" will be managed manually. 
* 