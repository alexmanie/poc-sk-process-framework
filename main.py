import os
import asyncio
from semantic_kernel.kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.processes.local_runtime.local_kernel_process import start
from semantic_kernel.processes.local_runtime.local_event import KernelProcessEvent

from steps import CommonEvents
from process import get_process

from dotenv import load_dotenv
load_dotenv(override=True)

async def run_the_process():
    """Run the process."""
    # Start the process
    process = get_process()
    
    try:
        # Configure the kernel with an AI Service and connection details, if necessary
        kernel = Kernel()
        kernel.add_service(
            AzureChatCompletion(
                endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),  
                # If you don't provide an API key, the service will attempt to authenticate using the Entra token.
                # api_key="my-api-key", 
            )
        )

        await start(
            process=process,
            kernel=kernel,
            initial_event=KernelProcessEvent(id=CommonEvents.StartProcess, data="foo"),
        )

        # kernel_process = await context.get_state()

        # c_step_state: KernelProcessStepState[CStepState] = next(
        #     (s.state for s in kernel_process.steps if s.state.name == "CStep"), None
        # )
        # c_step_state_validated = CStepState.model_validate(c_step_state.state)
        # print(f"[FINAL STEP STATE]: CStepState current cycle: {c_step_state_validated.current_cycle}")

        print("END.")

        # return JSONResponse(content={"processId": process_id}, status_code=200)
    except Exception as e:
        # return JSONResponse(content={"error": "Error starting process"}, status_code=500)
        print("Error starting process")
        print("Error:", str(e))
        raise

if __name__ == "__main__":
    asyncio.run(run_the_process())
