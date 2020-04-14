#!/bin/bash
# SBATCH -p ml_cpu-ivy
#SBATCH -p cpu_ivy
# SBATCH -p meta_gpu-x
# SBATCH -D /home/muelleph # we need this somehow when working with gpu-x
#SBATCH -t 0-02:00 # time (D-HH:MM)
#SBATCH -o /home/muelleph/HPOlib3/logs/cartpole_correlations/%x.%N.%j.out
#SBATCH -e /home/muelleph/HPOlib3/logs/cartpole_correlations/%x.%N.%j.err
#SBATCH -J hpolib_cc # sets the job name
#SBATCH -a 0-100
# SBATCH --mail-type=END,FAIL
#SBATCH --mail-type=FAIL
# SBATCH -c 1


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

python /home/muelleph/HPOlib3/experiments/cartpole_check_correlation.py --array_id  $SLURM_ARRAY_TASK_ID

echo Finished at $(date)
