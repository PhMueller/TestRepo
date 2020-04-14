#!/bin/bash
#SBATCH -p ml_cpu-ivy
#SBATCH -t 2-00:00 # time (D-HH:MM)

# SBATCH -p cpu_ivy
# SBATCH -t 0-02:00 # time (D-HH:MM)

# SBATCH -p meta_gpu-x
# SBATCH -D /home/muelleph # we need this somehow when working with gpu-x

#SBATCH -o /home/muelleph/HPOlib3/logs/batch/%x.%N.%j.out # This folder must exist
#SBATCH -e /home/muelleph/HPOlib3/logs/batch/%x.%N.%j.err
#SBATCH -J hpolib

# SBATCH -a 0-23,25-26,28-52,54-63,65-72
# SBATCH -a 64,53,27,24
#SBATCH -a 1-3

# SBATCH --mail-type=END,FAIL
#SBATCH --mail-type=FAIL

#SBATCH -c 1


# Print some information about the job to STDOUT

source ~/miniconda3/bin/activate && conda activate hpolib
cd ~/HPOlib3
export PATH=/usr/local/kislurm/singularity-3.5/bin/:$PATH

echo "Here's what we know from the SGE environment"
echo SHELL=$SHELL
echo HOME=$HOME
echo USER=$USER
echo JOB_ID=$JOB_ID
echo JOB_NAME=$JOB_NAME
echo HOSTNAME=$HOSTNAME
echo SLURM_TASK_ID=$SLURM_ARRAY_TASK_ID
echo Here we are: `pwd`

# python /home/muelleph/HPOlib3/examples/xgboost_cc_variance.py --array_id $SLURM_ARRAY_TASK_ID
# python /home/muelleph/HPOlib3/examples/xgboost_cc_variance_xgb_diff.py --array_id $SLURM_ARRAY_TASK_ID

if [ 1 -eq $SLURM_ARRAY_TASK_ID ]; then
python /home/muelleph/HPOlib3/examples/cartpole_bohb.py --out_path /home/muelleph/HPOlib3/experiments/cartpole_bohb
fi

if [ 2 -eq $SLURM_ARRAY_TASK_ID ]; then
python /home/muelleph/HPOlib3/examples/cartpole_hyperband.py --out_path /home/muelleph/HPOlib3/experiments/cartpole_smac_hb
fi

if [ 3 -eq $SLURM_ARRAY_TASK_ID ]; then
python /home/muelleph/HPOlib3/examples/cartpole_succesive_halving.py --out_path /home/muelleph/HPOlib3/experiments/cartpole_smac_sh
fi

echo Finished at $(date)
