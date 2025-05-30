#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --job-name=realness
#SBATCH --output=job_%A_%a.out
#SBATCH --error=job_%A_%a.err
#SBATCH --time=06:00:00
#SBATCH --mem=2G
#SBATCH --array=0-5

# Load modules
module load anaconda3
module load python

# Activate env
source activate realness

# Define the input directory
input_dir="realness_files_to_process_warda/real2"

# Get the list of all files in the input directory
input_files=($(ls $input_dir/*.xlsx))  # Modify the pattern if you need other file types


# Get the input file for the current job (based on task ID)
input_file=${input_files[$SLURM_ARRAY_TASK_ID]}

# Define the output file (change the extension to .txt)
output_file="${input_file}_realness.xlsx"

# Check if the output file exists
if [ -f "$output_file" ]; then
    echo "Output file $output_file already exists. Skipping processing."
else
    echo "Output file $output_file does not exist. Running Python script to process the file."
    python realness.py "$input_file"
fi
