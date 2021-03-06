import time

import ConfigSpace as CS
import numpy as np
import tensorflow as tf

from tensorforce.agents import PPOAgent
from tensorforce.contrib.openai_gym import OpenAIGym
from tensorforce.execution import Runner
from typing import Dict

from hpolib.abstract_benchmark import AbstractBenchmark
from hpolib.util import rng_helper


class CartpoleBase(AbstractBenchmark):
    def __init__(self, rng=None, defaults=None, max_budget=9):
        """
        Parameters
        ----------
        rng : int,None,np.RandomState
            RandomState for the experiment
        defaults : dict
            default configuration used for the PPO agent
        max_budget : int
            number of repetitions for the cartpole runner
        """

        super(CartpoleBase, self).__init__()

        self.rng = rng_helper.get_rng(rng=rng)
        tf.random.set_random_seed(0)
        np.random.seed(0)
        self.env = OpenAIGym('CartPole-v0', visualize=False)
        self.max_episodes = 3000
        self.avg_n_episodes = 20
        self.max_budget = max_budget

        self.defaults = {"n_units_1": 64,
                         "n_units_2": 64,
                         "batch_size": 64,
                         "learning_rate": 1e-3,
                         "discount": 0.99,
                         "likelihood_ratio_clipping": 0.2,
                         "activation_1": "tanh",
                         "activation_2": "tanh",
                         "optimizer_type": "adam",
                         "optimization_steps": 10,

                         "baseline_mode": "states",
                         "baseline_n_units_1": 64,
                         "baseline_n_units_2": 64,
                         "baseline_learning_rate": 1e-3,
                         "baseline_optimization_steps": 10,
                         "baseline_optimizer_type": "adam"}

        if defaults is not None:
            self.defaults.update(defaults)

    @staticmethod
    def get_configuration_space() -> CS.ConfigurationSpace:
        raise NotImplementedError()

    @AbstractBenchmark._check_configuration
    def objective_function(self, config: Dict, budget: int = None, **kwargs) -> Dict:
        # fill in missing entries with default values for 'incomplete/reduced' configspaces
        c = self.defaults
        c.update(config)
        config = c

        start_time = time.time()

        budget = budget or self.max_budget

        network_spec = [{'type': 'dense', 'size': config["n_units_1"], 'activation': config['activation_1']},
                        {'type': 'dense', 'size': config["n_units_2"], 'activation': config['activation_2']}]

        converged_episodes = []
        tf.random.set_random_seed(0)
        np.random.seed(0)

        for i in range(budget):
            agent = PPOAgent(states=self.env.states,
                             actions=self.env.actions,
                             network=network_spec,
                             update_mode={'unit': 'episodes', 'batch_size': config["batch_size"]},
                             step_optimizer={'type': config["optimizer_type"],
                                             'learning_rate': config["learning_rate"]},
                             optimization_steps=config["optimization_steps"],
                             discount=config["discount"],
                             baseline_mode=config["baseline_mode"],
                             baseline={"type": "mlp",
                                       "sizes": [config["baseline_n_units_1"], config["baseline_n_units_2"]]},
                             baseline_optimizer={"type": "multi_step",
                                                 "optimizer": {"type": config["baseline_optimizer_type"],
                                                               "learning_rate": config["baseline_learning_rate"]},
                                                 "num_steps": config["baseline_optimization_steps"]},
                             likelihood_ratio_clipping=config["likelihood_ratio_clipping"]
                             )

            def episode_finished(r):
                # Check if we have converged
                return np.mean(r.episode_rewards[-self.avg_n_episodes:]) != 200

            runner = Runner(agent=agent, environment=self.env)
            runner.run(episodes=self.max_episodes, max_episode_timesteps=200, episode_finished=episode_finished)
            converged_episodes.append(len(runner.episode_rewards))

        cost = time.time() - start_time

        return {'function_value': np.mean(converged_episodes),
                'cost': cost,
                'max_episodes': self.max_episodes,
                'budget': budget,
                'all_runs': converged_episodes}

    @AbstractBenchmark._check_configuration
    def objective_function_test(self, config: Dict, **kwargs) -> Dict:
        return self.objective_function(config, budget=self.max_budget, **kwargs)

    @staticmethod
    def get_meta_information() -> Dict:
        return {'name': 'Cartpole',
                'references': [],
                'note': 'This benchmark is not deterministic, since the gym environment is not deterministic.'
                        ' Also, often the benchmark is already converged after 1000 episodes.'
                        ' Increasing the budget \"max_episodes\" may lead to the same results.'}


class CartpoleFull(CartpoleBase):
    """Cartpole experiment on full configuration space"""
    @staticmethod
    def get_configuration_space(seed=0) -> CS.configuration_space:
        cs = CS.ConfigurationSpace(seed=seed)
        cs.add_hyperparameters([
            CS.UniformIntegerHyperparameter("n_units_1", lower=8, default_value=64, upper=64, log=True),
            CS.UniformIntegerHyperparameter("n_units_2", lower=8, default_value=64, upper=64, log=True),
            CS.UniformIntegerHyperparameter("batch_size", lower=8, default_value=64, upper=256, log=True),
            CS.UniformFloatHyperparameter("learning_rate", lower=1e-7, default_value=1e-3, upper=1e-1, log=True),
            CS.UniformFloatHyperparameter("discount", lower=0, default_value=.99, upper=1),
            CS.UniformFloatHyperparameter("likelihood_ratio_clipping", lower=0, default_value=.2, upper=1),
            CS.CategoricalHyperparameter("activation_1", ["tanh", "relu"]),
            CS.CategoricalHyperparameter("activation_2", ["tanh", "relu"]),
            CS.CategoricalHyperparameter("optimizer_type", ["adam", "rmsprop"]),
            CS.UniformIntegerHyperparameter("optimization_steps", lower=1, default_value=10, upper=10),
            CS.CategoricalHyperparameter("baseline_mode", ["states", "network"]),
            CS.UniformIntegerHyperparameter("baseline_n_units_1", lower=8, default_value=64, upper=128, log=True),
            CS.UniformIntegerHyperparameter("baseline_n_units_2", lower=8, default_value=64, upper=128, log=True),
            CS.UniformFloatHyperparameter("baseline_learning_rate",
                                          lower=1e-7, default_value=1e-3, upper=1e-1, log=True),
            CS.UniformIntegerHyperparameter("baseline_optimization_steps", lower=1, default_value=10, upper=10),
            CS.CategoricalHyperparameter("baseline_optimizer_type", ["adam", "rmsprop"]),
        ])
        return cs

    @staticmethod
    def get_meta_information() -> Dict:
        meta_information = CartpoleBase.get_meta_information()
        meta_information['description'] = 'Cartpole with full configuration space'
        return meta_information


class CartpoleReduced(CartpoleBase):
    """Cartpole experiment on smaller configuration space"""
    @staticmethod
    def get_configuration_space(seed=0) -> CS.configuration_space:
        cs = CS.ConfigurationSpace(seed=seed)
        cs.add_hyperparameters([
            CS.UniformIntegerHyperparameter("n_units_1", lower=8, default_value=64, upper=128, log=True),
            CS.UniformIntegerHyperparameter("n_units_2", lower=8, default_value=64, upper=128, log=True),
            CS.UniformIntegerHyperparameter("batch_size", lower=8, default_value=64, upper=256, log=True),
            CS.UniformFloatHyperparameter("learning_rate", lower=1e-7, default_value=1e-3, upper=1e-1, log=True),
            CS.UniformFloatHyperparameter("discount", lower=0, default_value=.99, upper=1),
            CS.UniformFloatHyperparameter("likelihood_ratio_clipping", lower=0, default_value=.2, upper=1),
            CS.UniformFloatHyperparameter("entropy_regularization", lower=0, default_value=0.01, upper=1)
        ])
        return cs

    @staticmethod
    def get_meta_information() -> Dict:
        meta_information = CartpoleBase.get_meta_information()
        meta_information['description'] = 'Cartpole with reduced configuration space'
        return meta_information
