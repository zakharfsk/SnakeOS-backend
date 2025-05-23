from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class PlatformInfo(BaseModel):
    system: str = Field(description="Operating system name (Linux)")
    release: str = Field(description="OS release version")
    version: str = Field(description="OS version information")
    machine: str = Field(description="Machine architecture")
    processor: str = Field(description="Processor information")
    distribution: str = Field(description="Linux distribution name")
    distribution_version: str = Field(description="Linux distribution version")
    distribution_id: str = Field(description="Linux distribution ID")


class CpuInfo(BaseModel):
    physical_cores: int = Field(description="Number of physical CPU cores")
    total_cores: int = Field(description="Total number of CPU cores (including logical cores)")
    cpu_freq_current: Optional[float] = Field(None, description="Current CPU frequency in MHz")
    cpu_freq_min: Optional[float] = Field(None, description="Minimum CPU frequency in MHz")
    cpu_freq_max: Optional[float] = Field(None, description="Maximum CPU frequency in MHz")
    cpu_usage_per_core: List[float] = Field(description="CPU usage percentage per core")
    total_cpu_usage: float = Field(description="Total CPU usage percentage")


class SwapMemory(BaseModel):
    total: float = Field(description="Total swap memory in GB")
    used: float = Field(description="Used swap memory in GB")
    free: float = Field(description="Free swap memory in GB")
    percentage: float = Field(description="Swap memory usage percentage")


class MemoryInfo(BaseModel):
    total: float = Field(description="Total RAM in GB")
    available: float = Field(description="Available RAM in GB")
    used: float = Field(description="Used RAM in GB")
    percentage: float = Field(description="RAM usage percentage")
    swap: SwapMemory = Field(description="Swap memory information")


class DiskPartition(BaseModel):
    device: str = Field(description="Device path")
    mountpoint: str = Field(description="Mount point path")
    filesystem_type: str = Field(description="File system type")
    total: float = Field(description="Total disk space in GB")
    used: float = Field(description="Used disk space in GB")
    free: float = Field(description="Free disk space in GB")
    percentage: float = Field(description="Disk usage percentage")


class NetworkAddress(BaseModel):
    address: str = Field(description="Network interface address")
    netmask: Optional[str] = Field(None, description="Network interface netmask")
    family: str = Field(description="Address family")


class NetworkIOCounters(BaseModel):
    bytes_sent: int = Field(description="Number of bytes sent")
    bytes_recv: int = Field(description="Number of bytes received")
    packets_sent: int = Field(description="Number of packets sent")
    packets_recv: int = Field(description="Number of packets received")
    errors_in: int = Field(description="Number of incoming errors")
    errors_out: int = Field(description="Number of outgoing errors")
    drop_in: int = Field(description="Number of incoming packets dropped")
    drop_out: int = Field(description="Number of outgoing packets dropped")


class NetworkInfo(BaseModel):
    interfaces: Dict[str, List[NetworkAddress]] = Field(description="Network interfaces information")
    io_counters: Dict[str, NetworkIOCounters | Dict[str, str]] = Field(
        description="Network I/O statistics per interface or error message if not available"
    )


class SystemInfo(BaseModel):
    platform: PlatformInfo = Field(description="Platform and OS information")
    boot_time: str = Field(description="System boot time")
    cpu: CpuInfo = Field(description="CPU information")
    memory: MemoryInfo = Field(description="Memory information")
    disks: List[DiskPartition] = Field(description="Disk partitions information")
    network: NetworkInfo = Field(description="Network information")
