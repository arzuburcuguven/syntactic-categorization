#!/bin/bash
#SBATCH --job-name=babytrain_curr_1
#SBATCH --gres=gpu:1
#SBATCH --mem=40GB
#SBATCH --time=24:00:00
#SBATCH --partition=scavenge
#SBATCH --output=logs/babytrain_curr_1_%j.out
#SBATCH --account=researchers


export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export WANDB_PROJECT=babylm_curriculum_experiments
export WANDB_ENTITY=arzuburcuguven-it-universitetet-i-k-benhavn
export WANDB_API_KEY=f393a3703562e8a5de71e1c8b47bb81c350603c2


# Load Conda
module load Anaconda3

# Explicitly activate the environment
source /opt/itu/easybuild/software/Anaconda3/2024.02-1/etc/profile.d/conda.sh
conda activate /home/argy/.conda/envs/trainbaby
echo "Activated environment: $(which python)"

# Navigate to project directory
cd /home/argy/extractor/src/experiments/scripts

accelerate launch --main_process_port 29501 run_clm_no_trainer.py \
  --config /home/argy/extractor/src/experiments/configs/curr_1.yaml
