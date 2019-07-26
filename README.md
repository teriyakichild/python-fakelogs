# fakelogs
This library can be used to generate a high volume of fake logs in multiple formats.  It uses the [Faker](https://faker.readthedocs.io/en/master/) library for generating the data.  It currently only supports logging to stdout with the main goal of running it in a pod.

## Install
```bash
# For development, run from within the cloned directory like this:
pip install -e .
#
python setup.py install
#or 
make install
#or 
pip install fakelogs # This isn't working yet.  Once we have a stable release, it will be pushed to pypi
```

## Configuration
Environment variables are used to configure the output of this program:
1. OUTPUT_FORMAT - This is the format used to output the fake data.  3 options are supported currently:
   * text - This generates a very basic log line with random text (Faker.text). (default)
   * kv - This generates a log with fake user profile data (Faker.profile) using a key/value pair format.
   * json - This generates a log with fake user profile data (Faker.profile) using a json format
2. TIME_TO_SLEEP: This is the time to sleep in seconds between each data generation (default is 1.0 second)
3. RECORDS_PER_ITERATION: This is the number of log records that should be generated before sleeping. (default is 1)
4. POOL_PROCESSES: Number of workers to use when generating logs.  Shouldn't be set higher than number of CPUs. (default is 1)
5. MAX_ITERATIONS: Maximum number of iterations to perform before quitting. (Defaults to 0 which means there is no limit)
6. TRANSACTION_ID: Unique Identifier that allows for easy searching of log messages. (Defaults to random UUID)
7. PRELOAD_DATA: Should data be loaded on startup or should it be generated on the fly. (Defaults to False)
8. PRELOAD_RECORDS: Number of records to preload. (Defaults to 2000)

## Usage
```bash
export OUTPUT_FORMAT=json
export TIME_TO_SLEEP=1
export RECORDS_PER_ITERATION=10
export POOL_PROCESSES=1
export MAX_ITERATIONS=0
fakelogs
```

## Tests
```bash
# Install dependencies
pip install -r requirements-dev.txt
# Run tests
pytests
```
