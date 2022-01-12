import json
import logging
from multiprocessing import Pool, cpu_count
from math import ceil
import os
import random
import sys
import time
import uuid
import re

BYTES = 1
KBYTES = 1024 * BYTES
MBYTES = 1024 * KBYTES
GBYTES = 1024 * MBYTES
DATE_FORMAT="%d-%b-%y %H:%M:%S"
from fakelogs.log import generate_text_log, generate_kv_log, generate_json_log

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt=DATE_FORMAT,
)


def read_from_environment():
    config = {}
    config["OUTPUT_FORMAT"] = os.getenv("OUTPUT_FORMAT", "text")
    config["TIME_TO_SLEEP"] = float(os.getenv("TIME_TO_SLEEP", 1))
    config["RECORDS_PER_ITERATION"] = int(
        os.getenv("RECORDS_PER_ITERATION", 1)
    )
    config["MAX_DATA_PER_ITERATION"] = os.getenv(
        "MAX_DATA_PER_ITERATION", None
    )
    config["POOL_PROCESSES"] = int(os.getenv("POOL_PROCESSES", cpu_count()))
    config["MAX_ITERATIONS"] = int(os.getenv("MAX_ITERATIONS", False))
    config["TRANSACTION_ID"] = str(os.getenv("TRANSACTION_ID", uuid.uuid4()))
    config["PRELOAD_RECORDS"] = min(
        int(os.getenv("PRELOAD_RECORDS", 2000)),
        config["RECORDS_PER_ITERATION"] * 10,
    )
    if config["MAX_DATA_PER_ITERATION"]:
        config["PRELOAD_RECORDS"] = 5000

    config["TEXT_WORD_COUNT"] = int(os.getenv("TEXT_WORD_COUNT", 15))
    return config


def generators():
    return {
        "text": generate_text_log,
        "kv": generate_kv_log,
        "json": generate_json_log,
    }


def preload(pool, num_records, format, config):
    logging.info(f"Generating dataset of {num_records} rows..")
    dataset = []

    def callback(result):
        dataset.append(result)

    generator = generators()[format]

    # Generate the dataset
    asyncs = []
    for i in range(num_records):
        # random.randint uses the current time to generate the return.  When POOL_PROCESSES
        # is set greater than 1, the log_generator function is called multiple times
        # concurrently. This results in outputting sets of identical log records.
        # To avoid this, we add the iteration index to the random number.
        seed = random.randint(1, 10000) + i
        asyncs.append(
            pool.apply_async(
                generator,
                (seed, config, True),
                callback=callback,
                error_callback=lambda x: logging.exception(x),
            )
        )

    # wait until all the queued logs are generated
    while not all(map(lambda ar: ar.ready(), asyncs)):
        time.sleep(0.1)
    logging.info("Generation complete.")

    return dataset


def format_bytes(size):
    if size > GBYTES:
        return f"{round(size / GBYTES, 2)}GB"
    elif size > MBYTES:
        return f"{round(size / MBYTES, 2)}MB"
    elif size > KBYTES:
        return f"{round(size / KBYTES, 2)}KB"
    else:
        return f"{round(size, 2)} bytes"


def max_data_per_iteration(max_data_str):
    if not max_data_str:
        return None

    match = re.search(r"([0-9\.]+)([a-zA-Z]+)", max_data_str)
    if match:
        if len(match.groups()) == 1:
            # Just units, assume bytes
            return int(match.groups()[0])
        else:
            amount, units = match.groups()
            amount = float(amount)
            unit = units.lower()[0]
            if unit == "g":
                return amount * GBYTES
            elif unit == "m":
                return amount * MBYTES
            elif unit == "k":
                return amount * KBYTES
            elif unit == "b":
                return amount
            else:
                raise ValueError(f"Unable to parse units for {max_data_str}")


def size_of_line(line):
    return len(line.encode("utf-8"))


def run(config):
    data = None
    with Pool(processes=config["POOL_PROCESSES"]) as pool:
        data = preload(
            pool, config["PRELOAD_RECORDS"], config["OUTPUT_FORMAT"], config
        )

    data_per = max_data_per_iteration(config["MAX_DATA_PER_ITERATION"])
    records_per = config["RECORDS_PER_ITERATION"]
    if data_per and data_per > 0:
        avg_line_size = sum(map(size_of_line, data)) / len(data)
        lines_per_batch = data_per / avg_line_size
        records_per = max(1, ceil(lines_per_batch))
        logging.info(
            f"data_per={data_per}, avg_line_size={avg_line_size}, lines_per_batch={lines_per_batch}, records_per={records_per}"
        )

    iter_size = 0
    iter_ts = time.time()
    iterations = 0
    while True:
        size = 0
        iterations += 1

        ts = time.time()
        lines = random.choices(data, k=records_per)

        size = sum(map(size_of_line, lines))
        for l in lines:
            # Pretend to be a logger, but fast
            print("{} {}".format(time.strftime(DATE_FORMAT), l))

        iter_size += size
        elap = time.time() - ts
        logging.info(
            f"Output {records_per} lines with a size of {format_bytes(size)} in {elap}s"
            + f" count={records_per} size={size} elap={elap}"
        )

        if config["MAX_ITERATIONS"] and iterations >= config["MAX_ITERATIONS"]:
            logging.info("Maximum number of iterations hit. Quitting..")
            elap = time.time() - iter_ts
            logging.info(
                f"Output {records_per * iterations} lines with a total size of {format_bytes(iter_size)} in {elap}s"
                + f" count={records_per * iterations} size={iter_size} elap={elap}"
            )
            return

        time.sleep(config["TIME_TO_SLEEP"])


def main():
    config = read_from_environment()
    if "--help" in sys.argv or "-h" in sys.argv:
        print(
            "Usage:\n {0}\n {0} [-h|--help]\n {0} [--show-config]".format(
                sys.argv[0]
            )
        )
        exit(0)
    elif "--show-config" in sys.argv:
        print(json.dumps(config, indent=2))
        exit(0)

    run(config)
