import logging
import time
import numpy as np
import json_tricks
import argparse

from pathlib import Path

# logging.basicConfig(level=logging.DEBUG)

from hpolib.util.openml_data_manager import get_openmlcc18_taskids
from hpolib.benchmarks.ml.xgboost_benchmark import XGBoostBenchmark as Benchmark


def run_benchmark(task_id):
    logger = logging.getLogger()
    logger.setLevel(level=logging.DEBUG)

    result_path = Path('./var_results_same_xgb_seed_diff_run_seed')
    result_path.mkdir(exist_ok=True, parents=True)

    start = time.time()

    n_estimators = [2, 4, 8, 16, 32, 64]
    subsamples = [0.1, 0.2, 0.4, 0.8, 1]

    result_per_data_set = []
    num_seeds = 50
    for i in range(num_seeds):
        my_rng = np.random.RandomState(i)
        b = Benchmark(rng=my_rng, task_id=task_id)
        cs = b.get_configuration_space()
        configuration = cs.get_default_configuration()
        data_per_config = {estimator: {subsample: {} for subsample in subsamples} for estimator in n_estimators}
        for estimator in n_estimators:
            for subsample in subsamples:
                try:
                    result_dict = b.objective_function(configuration, n_estimators=estimator, subsample=subsample,
                                                       rng=i, shuffle=True)
                    valid_loss = result_dict['function_value']
                    train_loss = result_dict['train_loss']
                    result_dict = b.objective_function_test(configuration, n_estimators=estimator, rng=i)
                    test_loss = result_dict['function_value']
                except:
                    train_loss, valid_loss, test_loss = -1024, -1024, -1024

                logger.info(f'[{i+1}|{num_seeds}] No Estimator: {estimator:3d} - Subsample Rate: {subsample:.1f} '
                            f'- Test {test_loss:.4f} - Valid {valid_loss:.4f} - Train {train_loss:.4f}')

                result = {'train_loss': train_loss, 'valid_loss': valid_loss, 'test_loss': test_loss}
                data_per_config[estimator][subsample] = result

        result_per_data_set.append([configuration.get_dictionary(), data_per_config])

    data_result_path = result_path / f'{task_id}.json'
    with data_result_path.open('w') as fh:
        json_tricks.dump(result_per_data_set, fh)

    logger.info("Done, took totally %.2f s" % (time.time() - start))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='HPOlib CC Datasets',
                                     description='HPOlib3',
                                     usage='%(prog)s <task_id>')
    parser.add_argument('--array_id', type=int,
                        help='values from 0 to 71')

    args = parser.parse_args()
    task_ids = get_openmlcc18_taskids()
    if args.array_id < len(task_ids):
        run_benchmark(task_ids[args.array_id])