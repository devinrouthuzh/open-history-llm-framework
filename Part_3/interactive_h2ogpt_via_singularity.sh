# create a workspace and prepare singularity
mkdir h2ogpt_trials
cd h2ogpt_trials

# customize the runtime environment according to the hpc system
module load singularityce

# build the singularity image file
singularity build ./h2ogpt_runtimev0_2_1_1245.sif docker://h2oairelease/h2oai-h2ogpt-runtime:v0.2.1-1245

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

# run the server from the singularity image file (sif)
singularity run \
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
       h2ogpt_runtimev0_2_1_1245.sif /workspace/generate.py \
          --base_model=h2oai/h2ogpt-4096-llama2-70b-chat \ # !! choose the model here !!
          --use_safetensors=True \
          --prompt_type=llama2 \
          --save_dir='/workspace/save/' \
          --auth_filename='/workspace/h2ogpt_auth/auth.db' \
          --use_gpu_id=False \
          --user_path=/workspace/user_path \
          --langchain_mode="LLM" \
          --langchain_modes="['UserData', 'LLM']" \
          --score_model=None \
          --max_max_new_tokens=2048 \
          --max_new_tokens=1024 \
          --gpus '"device=0"'