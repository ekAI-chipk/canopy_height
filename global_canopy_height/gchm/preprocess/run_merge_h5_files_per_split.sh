#!/bin/bash
#SBATCH --job-name=merge_h5
#SBATCH --array=0
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=8G  # this is muliplied by cpus-per-task AND ntasks
#SBATCH --time=0-48:00:00
#SBATCH --output=/cluster/work/igp_psr/nlang/experiments/gchm/slurm_logs/slurm-%A_%a_%x.out
# send email
#SBATCH --mail-type=ARRAY_TASKS  # send email for each individual array task, otherwise only for the job array as a whole.
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-type=fail         # send email if job fails

# module load gcc/6.3.0 openblas/0.2.20 nccl/2.7.8-1 python_gpu/3.8.5 cuda/11.7.0 cudnn/8.4.0.27 gdal/3.5.3
export PYTHONPATH="/mnt/hdd12tb/code/trivt/global-canopy-height-model:$PYTHONPATH"

# Set path to python
PYTHON="$HOME/anaconda3/envs/chme/bin/python"
echo ${PYTHON}
# Set path to repository
# /mnt/hdd12tb/code/trivt/global-canopy-height-model/data
CODE_PATH="/mnt/hdd12tb/code/trivt/global-canopy-height-model"

cd ${CODE_PATH}

in_h5_dir_parts="/mnt/hdd12tb/code/trivt/data/parts_shuffled"
out_h5_dir="/mnt/hdd12tb/code/trivt/data/merged_shuffled"

$PYTHON gchm/preprocess/merge_h5_files_per_split.py ${in_h5_dir_parts} ${out_h5_dir}

