#!/usr/bin/bash -l

# submit the job according to the hpc workload management system

#SBATCH -n 1
#SBATCH -c 6
#SBATCH --gpus=A100:1
#SBATCH --time=02:00:00
#SBATCH --mem=80G
#SBATCH --time=02:00:00

# create a workspace and prepare singularity
mkdir h2ogpt_trials
cd h2ogpt_trials

# customize the runtime environment according to the hpc system
module load singularityce

# build the singularity image file
singularity build ./h2ogpt_runtimev0_2_1_0947.sif docker://h2oairelease/h2oai-h2ogpt-runtime:v0.2.1-947

# create necessary directories
mkdir -p ./.cache/huggingface/hub/ &&
mkdir -p ./.triton/cache/ &&
mkdir -p ./.config/vllm/ &&
mkdir -p ./.cache &&
mkdir -p ./save &&
mkdir -p ./user_path &&
mkdir -p ./db_dir_UserData &&
mkdir -p ./users &&
mkdir -p ./db_nonusers &&
mkdir -p ./llamacpp_path &&
mkdir -p ./h2ogpt_auth &&

# execute a build of the RAG database followed the execution of the evalution script
singularity exec \
       --nv \
       -B /etc/passwd:/etc/passwd:ro \
       -B /etc/group:/etc/group:ro \
       -B ./.cache/huggingface/hub/:/workspace/.cache/huggingface/hub \
       -B ./.config:/workspace/.config/ \
       -B ./.triton:/workspace/.triton/  \
       -B ./save:/workspace/save \
       -B ./user_path:/workspace/user_path \
       -B ./db_dir_UserData:/workspace/db_dir_UserData \
       -B ./users:/workspace/users \
       -B ./db_nonusers:/workspace/db_nonusers \
       -B ./llamacpp_path:/workspace/llamacpp_path \
       -B ./h2ogpt_auth:/workspace/h2ogpt_auth \
       h2ogpt_runtimev0_2_1_1245.sif python /workspace/src/make_db.py && python eval.py