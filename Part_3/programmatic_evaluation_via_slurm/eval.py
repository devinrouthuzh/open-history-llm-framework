# define the evaluation function (then run it)
from tests.utils import make_user_path_test
def run_eval(cpu=False,
             bits=None,
             base_model='h2oai/h2ogpt-4096-llama2-13b-chat',
             eval_filename=None,
             eval_prompts_only_num=1):
    from src.gen import main
    user_path = make_user_path_test()
    kwargs = dict(
            stream_output=False,
            langchain_mode='UserData',
            langchain_modes=['UserData']
    )
    eval_out_filename = main(base_model=base_model,
                             eval=True, gradio=False,
                             eval_filename=eval_filename,
                             eval_prompts_only_num=eval_prompts_only_num,
                             eval_as_output=False,
                             eval_prompts_only_seed=42,
                             score_model='h2oai/h2ogpt-4096-llama2-7b-chat', # !! Consider using a different model if numeric scores are assessed
                             answer_with_sources=True,append_sources_to_answer=True,append_sources_to_chat=False, # !! Added so sources are appended
                             user_path='src/user_path',show_link_in_sources=True, # !! Added so sources are appended
                             **kwargs)
    return eval_out_filename

# input the desired parameters to the function
eval_filename = 'prompts.json'
nprompts = 2 # !! Currently this is manually set based on the number of questions; could be automated
bits = 8
cpu = False
base_model = 'h2oai/h2ogpt-4096-llama2-13b-chat'

# run the function
eval_out_filename = run_eval(cpu=cpu, bits=bits, base_model=base_model,eval_filename=eval_filename,eval_prompts_only_num=nprompts)

# write the outputs to a csv for downstream parsing
import pandas as pd
df = pd.read_parquet(eval_out_filename)
df.to_csv('outputs.csv')