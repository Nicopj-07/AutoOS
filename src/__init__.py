"""
AutoOS - Simulación de Sistema Operativo para Vehículo Inteligente
Módulo de Procesos y CPU.
"""
from src.core import (
    ProcessState,
    VALID_TRANSITIONS,
    AutoOSError,
    InvalidStateTransitionError,
    InvalidProcessPriorityError,
    InvalidProcessAttributeError,
    CPUBusyError,
    DuplicateProcessError,
    Process,
    CPU,
    Scheduler,
    Event,
    EventLogger,
    SimulationEngine,
)
from src.dto import (
    ProcessDTO,
    CPUDTO,
    SchedulerDTO,
    EventDTO,
    SystemStatusDTO,
)
from src.services import AutoOSService

__all__ = [
    "ProcessState",
    "VALID_TRANSITIONS",
    "AutoOSError",

    "InvalidStateTransitionError",
    "InvalidProcessPriorityError",
    "InvalidProcessAttributeError",
    "CPUBusyError",
    "DuplicateProcessError",
    "Process",
    "CPU",
    "Scheduler",
    "Event",
    "EventLogger",
    "SimulationEngine",
    "ProcessDTO",
    "CPUDTO",
    "SchedulerDTO",
    "EventDTO",
    "SystemStatusDTO",
    "AutoOSService",
]

