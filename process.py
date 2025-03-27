# Copyright (c) Microsoft. All rights reserved.

from typing import TYPE_CHECKING

from steps import *

from semantic_kernel.processes import ProcessBuilder

if TYPE_CHECKING:
    from semantic_kernel.processes.kernel_process.kernel_process import KernelProcess


def get_process() -> "KernelProcess":
    # Define the process builder
    process_builder = ProcessBuilder(name="Multiple Steps Process", description="Process with multiple steps")

    # Add the step types to the builder
    kickoff_step = process_builder.add_step(step_type=KickOffStep)
    myAStep = process_builder.add_step(step_type=AStep)
    # myBStep = process_builder.add_step(step_type=BStep, factory_function=bstep_factory)
    myBStep = process_builder.add_step(step_type=BStep)
    myCStep = process_builder.add_step(step_type=CStep)
    myDStep = process_builder.add_step(step_type=DStep)
    myEStep = process_builder.add_step(step_type=EStep)
    myFStep = process_builder.add_step(step_type=FStep)
    myGStep = process_builder.add_step(step_type=GStep)
    myHStep = process_builder.add_step(step_type=HStep)
    myIStep = process_builder.add_step(step_type=IStep)
    myJStep = process_builder.add_step(step_type=JStep)
    myKStep = process_builder.add_step(step_type=KStep)

    operativaStep = process_builder.add_step(step_type=OperativaStep)
    calidadEmpleoStep = process_builder.add_step(step_type=CalidadEmpleoStep)
    ingresosStep = process_builder.add_step(step_type=IngresosStep)

    # Initialize the CStep with an initial state and the state's current cycle set to 1
    # myCStep = process_builder.add_step(step_type=CStep, initial_state=CStepState(current_cycle=1))

    # Define the input event and where to send it to
    process_builder.on_input_event(event_id=CommonEvents.StartProcess).send_event_to(target=kickoff_step)

    # Define the process flow
    kickoff_step.on_event(event_id=CommonEvents.StartOperativaRequested).send_event_to(target=operativaStep, function_name="do_it")
    kickoff_step.on_event(event_id=CommonEvents.StartCalidadEmpleoRequested).send_event_to(target=calidadEmpleoStep, function_name="do_it")
    kickoff_step.on_event(event_id=CommonEvents.StartIngresosRequested).send_event_to(target=ingresosStep, function_name="do_it")

    operativaStep.on_event(event_id=CommonEvents.StartARequested).send_event_to(target=myAStep)
    operativaStep.on_event(event_id=CommonEvents.StartBRequested).send_event_to(target=myBStep)
    operativaStep.on_event(event_id=CommonEvents.StartCRequested).send_event_to(target=myCStep)
    operativaStep.on_event(event_id=CommonEvents.StartDRequested).send_event_to(target=myDStep)
    
    calidadEmpleoStep.on_event(event_id=CommonEvents.StartERequested).send_event_to(target=myEStep)
    calidadEmpleoStep.on_event(event_id=CommonEvents.StartFRequested).send_event_to(target=myFStep)
    calidadEmpleoStep.on_event(event_id=CommonEvents.StartGRequested).send_event_to(target=myGStep)
    
    ingresosStep.on_event(event_id=CommonEvents.StartHRequested).send_event_to(target=myHStep)
    ingresosStep.on_event(event_id=CommonEvents.StartIRequested).send_event_to(target=myIStep)
    ingresosStep.on_event(event_id=CommonEvents.StartJRequested).send_event_to(target=myJStep)
    ingresosStep.on_event(event_id=CommonEvents.StartKRequested).send_event_to(target=myKStep)
    
    myAStep.on_event(event_id=CommonEvents.AStepDone).send_event_to(target=operativaStep, function_name="receive_information", parameter_name="astepdata")
    myBStep.on_event(event_id=CommonEvents.BStepDone).send_event_to(target=operativaStep, function_name="receive_information", parameter_name="bstepdata")
    myCStep.on_event(event_id=CommonEvents.CStepDone).send_event_to(target=operativaStep, function_name="receive_information", parameter_name="cstepdata")
    myDStep.on_event(event_id=CommonEvents.DStepDone).send_event_to(target=operativaStep, function_name="receive_information", parameter_name="dstepdata")

    myEStep.on_event(event_id=CommonEvents.EStepDone).send_event_to(target=calidadEmpleoStep, function_name="receive_information", parameter_name="estepdata")
    myFStep.on_event(event_id=CommonEvents.FStepDone).send_event_to(target=calidadEmpleoStep, function_name="receive_information", parameter_name="fstepdata")
    myGStep.on_event(event_id=CommonEvents.GStepDone).send_event_to(target=calidadEmpleoStep, function_name="receive_information", parameter_name="gstepdata")

    myHStep.on_event(event_id=CommonEvents.HStepDone).send_event_to(target=ingresosStep, function_name="receive_information", parameter_name="hstepdata")
    myIStep.on_event(event_id=CommonEvents.IStepDone).send_event_to(target=ingresosStep, function_name="receive_information", parameter_name="istepdata")
    myJStep.on_event(event_id=CommonEvents.JStepDone).send_event_to(target=ingresosStep, function_name="receive_information", parameter_name="jstepdata")
    myKStep.on_event(event_id=CommonEvents.KStepDone).send_event_to(target=ingresosStep, function_name="receive_information", parameter_name="kstepdata")

    ingresosStep.on_event(event_id=CommonEvents.IngresosStepDone).send_event_to(target=calidadEmpleoStep, function_name="receive_ingresos")

    calidadEmpleoStep.on_event(event_id=CommonEvents.ExitRequested).stop_process()

    # Build the process
    return process_builder.build()
