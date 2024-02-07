# Car Submission Pipeline`

`car-submission-pipeline` is a python utility meant to monitor and process inputs related to objects detection and vehicle status.

## Installation

* A PostgresSQL database needs to be available and properly configured
  * The database specified in the `POSTGRES_DB` variable has to exist
  * The user specified in the `POSTGRES_USER` has to have access to that database
* The following envionment variable must be set: 
  * `POSTGRES_USER`
  * `POSTGRES_PASS`
  * `POSTGRES_HOST`
  * `POSTGRES_PORT`
  * `POSTGRES_DB` 
  * `FILE_DIRECTORY`
* If this is being run in a cloud or containerized environment, the input-files directory can be mounted in and then specified using the environment variables.
* Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `car-submission-pipeline`.

```bash
pip install -r requirements.txt
```

## Usage

```python
python pipeline/run.py 
```

## Interview-related notes:
* I've chosen the postgres backend due it's high-level support for native JSON querying. However, I specifically chose an ORM library which can be moved to cloud support natively by changing environment variables, and can also be easily refactored to cloud-native DBs in case greater scale is needed, or we need to go full noSQL.
* I've set this up to be stateless, to allow deployments such as a Kubernetes `CronJobs` or as a serverless function
* I'm assuming filename timestamps on the files are in unix format 
* Improvements, were there to be more time:
  * Add type annotations
  * Add tests, specifically on validation and parsing
  * Ensure dupilicates don't make it into the database. Probably by enforcing DB-level uniqueness constraints between time and `vehicle_id`.
  * Move old files which are not processed as part of this run to the 'processed' directory
  * Make sure to use filepath types (see typing)
  * Scale - this isn't easily multithreaded. If we're hitting scale issues, split the reading of files into different threads by splitting the file-list in `SubmissionFile.process_files`
  * Exception handling and logging (always need more of that). Specifically, I spent a while dealing with input issues. We need to be more lenient on input, or ensure more sanitized data.
  * Make the file interface more generic to support cloud storage or an FTP server etc...
  * In CI, replace `psycopg2-binary` with `psycopg2` (after installing prerequisites) for production run
