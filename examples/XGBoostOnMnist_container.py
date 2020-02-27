import logging
import time
import numpy as np

logger = logging.getLogger()
logger.setLevel(level=logging.DEBUG)

from hpolib.container.benchmarks.ml.xgboost_benchmark import XGBoostBenchmark as Benchmark

myrng = np.random.RandomState(10)

# container_name must be the exact same as the suffix in the recipe name
# (Singuarity.XGBoostBenchmark --> XGBoostBenchmark)
b = Benchmark(rng=myrng,
              container_name='XGBoostBenchmark',
              container_source='/home/philipp/.cache/hpolib3/hpolib3-1000',
              task_id=167149)
print(b.get_meta_information())

start = time.time()
values = []
cs = b.get_configuration_space()

for i in range(1000):
    configuration = cs.sample_configuration()
    rval = b.objective_function(configuration, n_estimators=5, subsample=0.1)
    loss = rval['function_value']
    print(f'[{i + 1}|1000]Loss {loss:.4f}')

    values.append(loss)

print("Done, took totally %.2f s" % (time.time() - start))
