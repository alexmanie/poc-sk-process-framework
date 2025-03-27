# Copyright (c) Microsoft. All rights reserved.

import asyncio
from enum import Enum
from typing import ClassVar
import random

from pydantic import Field

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions import kernel_function
from semantic_kernel.kernel import Kernel
from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.processes.kernel_process import (
    KernelProcessStep,
    KernelProcessStepContext,
    KernelProcessStepState,
)


# Define a `xxStepState` that will keep track of the process.
class OperativaStepState(KernelBaseModel):
    info_a: str = None
    info_b: str = None
    info_c: str = None
    info_d: str = None

class CalidadStepState(KernelBaseModel):
    info_e: str = None
    info_f: str = None
    info_g: str = None

    @property
    def full_information(self) -> bool:
        return self.info_e is not None and self.info_f is not None and self.info_g is not None

class IngresosStepState(KernelBaseModel):
    info_h: str = None
    info_i: str = None
    info_j: str = None
    info_k: str = None    

class CommonEvents(Enum):
    """Common events for the sample process."""

    StartProcess = "StartProcess"
    StartOperativaRequested = "StartOperativaRequested"
    OperativaStepDone = "OperativaStepDone"
    StartCalidadEmpleoRequested = "StartCalidadEmpleoRequested"
    CalidadEmpleoStepDone = "CalidadEmpleoStepDone"
    StartIngresosRequested = "StartIngresosRequested"
    IngresosStepDone = "IngresosStepDone"
    AStepDone = "AStepDone"
    BStepDone = "BStepDone"
    CStepDone = "CStepDone"
    DStepDone = "DStepDone"
    EStepDone = "EStepDone"
    FStepDone = "FStepDone"
    GStepDone = "GStepDone"
    HStepDone = "HStepDone"
    IStepDone = "IStepDone"
    JStepDone = "JStepDone"
    KStepDone = "KStepDone"
    StartARequested = "StartARequested"
    StartBRequested = "StartBRequested"
    StartCRequested = "StartCRequested"
    StartDRequested = "StartDRequested"
    StartERequested = "StartERequested"
    StartFRequested = "StartFRequested"
    StartGRequested = "StartGRequested"
    StartHRequested = "StartHRequested"
    StartIRequested = "StartIRequested"
    StartJRequested = "StartJRequested"
    StartKRequested = "StartKRequested"
    ExitRequested = "ExitRequested"


# Define a sample step that once the `on_input_event` is received,
# it will emit multiple events to start the child steps.
class KickOffStep(KernelProcessStep):
    KICK_OFF_FUNCTION: ClassVar[str] = "kick_off"

    @kernel_function(name=KICK_OFF_FUNCTION)
    async def print_welcome_message(self, context: KernelProcessStepContext):
        print("##### Kickoff ran.")
        await context.emit_event(process_event=CommonEvents.StartOperativaRequested, data="Get Going Operativa")
        await context.emit_event(process_event=CommonEvents.StartCalidadEmpleoRequested, data="Get Going QA Empleo")
        await context.emit_event(process_event=CommonEvents.StartIngresosRequested, data="Get Going Ingresos")


# Define a sample `OperativaStep` step
class OperativaStep(KernelProcessStep[OperativaStepState]):
    state: OperativaStepState = Field(default_factory=OperativaStepState)

    @kernel_function()
    async def do_it(self, context: KernelProcessStepContext):
        print("##### OperativaStep \'do_it\' requested.")
        # await asyncio.sleep(1)
        await context.emit_event(process_event=CommonEvents.StartARequested, data="Get Going A")
        await context.emit_event(process_event=CommonEvents.StartBRequested, data="Get Going B")
        await context.emit_event(process_event=CommonEvents.StartCRequested, data="Get Going C")
        await context.emit_event(process_event=CommonEvents.StartDRequested, data="Get Going D")

    @kernel_function()
    async def receive_information(self, context: KernelProcessStepContext, astepdata: str = "", bstepdata: str = "", cstepdata: str = "", dstepdata: str = ""):
        print("##### OperativaStep \'receive_information\' requested.")

        if astepdata != "":
            print(f"##### OperativaStep received astepdata: {astepdata}")
            self.state.info_a = astepdata
        elif bstepdata != "":
            print(f"##### OperativaStep received bstepdata: {bstepdata}")
            self.state.info_b = bstepdata
        elif cstepdata != "":
            print(f"##### OperativaStep received cstepdata: {cstepdata}")
            self.state.info_c = cstepdata
        elif dstepdata != "":
            print(f"##### OperativaStep received dstepdata: {dstepdata}")
            self.state.info_d = dstepdata

        # Check if all data has been received
        if self.state.info_a is not None and self.state.info_b is not None and self.state.info_c is not None and self.state.info_d is not None:
            print("##### OperativaStep - All child data received.")
            print("##### OperativaStep - Sending event [OperativaStepDone].")
            await context.emit_event(process_event=CommonEvents.OperativaStepDone)
        else:
            print("##### OperativaStep - Some child data received.")


# Define a sample `CalidadEmpleoStep` step
class CalidadEmpleoStep(KernelProcessStep[CalidadStepState]):
    state: CalidadStepState = Field(default_factory=CalidadStepState)

    # The activate method overrides the base class method to set the state in the step.
    async def activate(self, state: KernelProcessStepState[CalidadStepState]):
        """Activates the step and sets the state."""
        self.state = state.state

    @kernel_function()
    async def do_it(self, context: KernelProcessStepContext):
        print(f"##### CalidadEmpleoStep requested with full information : '{self.state.full_information}'.")
        if self.state.full_information == False:
            await context.emit_event(process_event=CommonEvents.StartERequested, data="Get Going E")
            await context.emit_event(process_event=CommonEvents.StartFRequested, data="Get Going F")
            await context.emit_event(process_event=CommonEvents.StartGRequested, data="Get Going G")
            

    @kernel_function()
    async def receive_information(self, context: KernelProcessStepContext, estepdata: str = "", fstepdata: str = "", gstepdata: str = ""):
        print("##### CalidadEmpleoStep \'receive_information\' requested.")

        if estepdata != "":
            print(f"##### CalidadEmpleoStep received estepdata: {estepdata}")
            self.state.info_e = estepdata
        elif fstepdata != "":
            print(f"##### CalidadEmpleoStep received fstepdata: {fstepdata}")
            self.state.info_f = fstepdata
        elif gstepdata != "":
            print(f"##### CalidadEmpleoStep received gstepdata: {gstepdata}")
            self.state.info_g = gstepdata
        
        print(f"##### CalidadEmpleoStep requested with full information: '{self.state.full_information}'.")

        # Check if all data has been received
        if self.state.info_e is not None and self.state.info_f is not None and self.state.info_g is not None:
            print("##### CalidadEmpleoStep - All child data received.")
            print("##### CalidadEmpleoStep - Sending event [CalidadEmpleoStepDone].")
            await context.emit_event(process_event=CommonEvents.CalidadEmpleoStepDone)

    @kernel_function()
    async def receive_ingresos(self, context: KernelProcessStepContext, docs: str):
        print("##### CalidadEmpleoStep \'receive_ingresos\' requested.")
        print(f"##### CalidadEmpleoStep received docs from IngresosStep: {docs}")
        
        print("##### CalidadEmpleoStep - All data received ==> EXIT.")
        await context.emit_event(process_event=CommonEvents.ExitRequested)  

# Define a sample `IngresosStep` step
class IngresosStep(KernelProcessStep[IngresosStepState]):
    state: IngresosStepState = Field(default_factory=IngresosStepState)

    @kernel_function()
    async def do_it(self, context: KernelProcessStepContext):
        print("##### IngresosStep \'do_it\' requested.")
        await asyncio.sleep(1)
        await context.emit_event(process_event=CommonEvents.StartHRequested, data="Get Going H")
        await context.emit_event(process_event=CommonEvents.StartIRequested, data="Get Going I")
        await context.emit_event(process_event=CommonEvents.StartJRequested, data="Get Going J")
        await context.emit_event(process_event=CommonEvents.StartKRequested, data="Get Going K")

    @kernel_function()
    async def receive_information(self, context: KernelProcessStepContext, hstepdata: str = "", istepdata: str = "", jstepdata: str = "", kstepdata: str = ""):
        print("##### IngresosStep \'receive_information\' requested.")

        if hstepdata != "":
            print(f"##### IngresosStep received hstepdata: {hstepdata}")
            self.state.info_h = hstepdata
        elif istepdata != "":
            print(f"##### IngresosStep received istepdata: {istepdata}")
            self.state.info_i = istepdata
        elif jstepdata != "":
            print(f"##### IngresosStep received jstepdata: {jstepdata}")
            self.state.info_j = jstepdata
        elif kstepdata != "":
            print(f"##### IngresosStep received kstepdata: {kstepdata}")
            self.state.info_k = kstepdata

        # Check if all data has been received
        if self.state.info_h is not None and self.state.info_i is not None and self.state.info_j is not None and self.state.info_k is not None:
            print("##### IngresosStep - All child data received.")
            print("##### IngresosStep - Sending event [IngresosStepDone].")
            await context.emit_event(process_event=CommonEvents.IngresosStepDone, data="All information from IngressosStep goes here.")
        else:
            print("##### IngresosStep - Some child data received.")

# Define a sample `AStep` step that will emit an event after 1 second.
# The event will be sent to the `CStep` step with the data `I did A`.
class AStep(KernelProcessStep):
    @kernel_function()
    async def do_it(self, context: KernelProcessStepContext):
        seconds: int = random.randint(1, 10)
        await asyncio.sleep(seconds)
        print("##### AStep ran.")
        await context.emit_event(process_event=CommonEvents.AStepDone, data="I did A")

# Define a sample `BStep` step that will emit an event after 1 second.
class BStep(KernelProcessStep):
    @kernel_function()
    async def do_it(self, context: KernelProcessStepContext):
        seconds: int = random.randint(1, 8)
        await asyncio.sleep(seconds)
        print("##### BStep ran.")
        await context.emit_event(process_event=CommonEvents.BStepDone, data="I did B")


# Define a sample `CStep` step that will emit an event after 1 second.
class CStep(KernelProcessStep):
    @kernel_function()
    async def do_it(self, context: KernelProcessStepContext):
        seconds: int = random.randint(1, 9)
        await asyncio.sleep(seconds)
        print("##### CStep ran.")
        await context.emit_event(process_event=CommonEvents.CStepDone, data="I did C")


# Define a sample `DStep` step that will emit an event after 1 second.
class DStep(KernelProcessStep):
    @kernel_function()
    async def do_it(self, context: KernelProcessStepContext):
        seconds: int = random.randint(1, 6)
        await asyncio.sleep(seconds)
        print("##### DStep ran.")
        await context.emit_event(process_event=CommonEvents.DStepDone, data="I did D")


# Define a sample `EStep` step that will emit an event after 1 second.
class EStep(KernelProcessStep):
    @kernel_function()
    async def do_it(self, context: KernelProcessStepContext):
        seconds: int = random.randint(1, 3)
        await asyncio.sleep(seconds)
        print("##### EStep ran.")
        await context.emit_event(process_event=CommonEvents.EStepDone, data="I did E")


# Define a sample `FStep` step that will emit an event after 1 second.
class FStep(KernelProcessStep):
    @kernel_function()
    async def do_it(self, context: KernelProcessStepContext):
        seconds: int = random.randint(1, 7)
        await asyncio.sleep(seconds)
        print("##### FStep ran.")
        await context.emit_event(process_event=CommonEvents.FStepDone, data="I did F")


# Define a sample `GStep` step that will emit an event after 1 second.
class GStep(KernelProcessStep):
    @kernel_function()
    async def do_it(self, context: KernelProcessStepContext):
        seconds: int = random.randint(1, 5)
        await asyncio.sleep(seconds)
        print("##### GStep ran.")
        await context.emit_event(process_event=CommonEvents.GStepDone, data="I did G")


# Define a sample `HStep` step that will emit an event after 1 second.
class HStep(KernelProcessStep):
    @kernel_function()
    async def do_it(self, context: KernelProcessStepContext):
        seconds: int = random.randint(1, 5)
        await asyncio.sleep(seconds)
        print("##### HStep ran.")
        await context.emit_event(process_event=CommonEvents.HStepDone, data="I did H")


# Define a sample `IStep` step that will emit an event after 1 second.
class IStep(KernelProcessStep):
    @kernel_function()
    async def do_it(self, context: KernelProcessStepContext):
        seconds: int = random.randint(1, 5)
        await asyncio.sleep(seconds)
        print("##### IStep ran.")
        await context.emit_event(process_event=CommonEvents.IStepDone, data="I did I")


# Define a sample `JStep` step that will emit an event after 1 second.
class JStep(KernelProcessStep):
    @kernel_function()
    async def do_it(self, context: KernelProcessStepContext):
        seconds: int = random.randint(1, 5)
        await asyncio.sleep(seconds)
        print("##### JStep ran.")
        await context.emit_event(process_event=CommonEvents.JStepDone, data="I did J")


# Define a sample `KStep` step that will emit an event after 1 second.
class KStep(KernelProcessStep):
    @kernel_function()
    async def do_it(self, context: KernelProcessStepContext):
        seconds: int = random.randint(1, 5)
        await asyncio.sleep(seconds)
        print("##### KStep ran.")
        await context.emit_event(process_event=CommonEvents.KStepDone, data="I did K")