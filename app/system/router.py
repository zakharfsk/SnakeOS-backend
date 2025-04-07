from fastapi import APIRouter, Depends
from ..auth.utils import get_current_user
from ..models.user import User
from . import schemas
from .utils import system_monitor
from ..settings import settings

router = APIRouter(prefix=f"{settings.API_V1_STR}/system", tags=["System"])


@router.get("/", response_model=schemas.SystemInfo)
async def get_system_info(current_user: User = Depends(get_current_user)):
    """Get complete system information including CPU, memory, disk, and network."""
    return system_monitor.get_system_info()


@router.get("/cpu", response_model=schemas.CpuInfo)
async def get_cpu_info(current_user: User = Depends(get_current_user)):
    """Get CPU information including usage and frequency."""
    return system_monitor.get_cpu_info()


@router.get("/memory", response_model=schemas.MemoryInfo)
async def get_memory_info(current_user: User = Depends(get_current_user)):
    """Get memory information including RAM and swap usage."""
    return system_monitor.get_memory_info()


@router.get("/disk", response_model=list[schemas.DiskPartition])
async def get_disk_info(current_user: User = Depends(get_current_user)):
    """Get disk information for all partitions."""
    return system_monitor.get_disk_info()


@router.get("/network", response_model=schemas.NetworkInfo)
async def get_network_info(current_user: User = Depends(get_current_user)):
    """Get network information including interfaces and IO statistics."""
    return system_monitor.get_network_info()
