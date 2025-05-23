import platform
from datetime import datetime
from typing import Dict, List

import distro
import psutil
from fastapi import HTTPException


def get_platform_info() -> Dict:
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "distribution": distro.name(pretty=True),
        "distribution_version": distro.version(),
        "distribution_id": distro.id(),
    }


def get_cpu_info() -> Dict:
    try:
        cpu_freq = psutil.cpu_freq()
        cpu_info = {
            "physical_cores": psutil.cpu_count(logical=False),
            "total_cores": psutil.cpu_count(logical=True),
            "cpu_freq_current": round(cpu_freq.current, 2) if cpu_freq else None,
            "cpu_freq_min": round(cpu_freq.min, 2) if cpu_freq else None,
            "cpu_freq_max": round(cpu_freq.max, 2) if cpu_freq else None,
            "cpu_usage_per_core": [round(x, 2) for x in psutil.cpu_percent(percpu=True, interval=1)],
            "total_cpu_usage": round(psutil.cpu_percent(interval=1), 2),
        }
        return cpu_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting CPU info: {str(e)}")


def get_memory_info() -> Dict:
    """Get memory information using psutil"""
    try:
        virtual_memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        return {
            "total": round(virtual_memory.total / (1024**3), 2),  # GB
            "available": round(virtual_memory.available / (1024**3), 2),  # GB
            "used": round(virtual_memory.used / (1024**3), 2),  # GB
            "percentage": virtual_memory.percent,
            "swap": {
                "total": round(swap.total / (1024**3), 2),  # GB
                "used": round(swap.used / (1024**3), 2),  # GB
                "free": round(swap.free / (1024**3), 2),  # GB
                "percentage": swap.percent,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting memory info: {str(e)}")


def get_disk_info() -> List[Dict]:
    try:
        disk_info = []
        for partition in psutil.disk_partitions(all=False):  # all=False to skip special filesystems
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append(
                    {
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "filesystem_type": partition.fstype,
                        "total": round(usage.total / (1024**3), 2),  # GB
                        "used": round(usage.used / (1024**3), 2),  # GB
                        "free": round(usage.free / (1024**3), 2),  # GB
                        "percentage": usage.percent,
                    }
                )
            except PermissionError:
                # Skip partitions that we don't have access to
                continue
            except Exception:
                # Skip problematic partitions
                continue
        return disk_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting disk info: {str(e)}")


def get_network_info() -> Dict:
    try:
        network_info = {"interfaces": {}, "io_counters": {}}

        # Get network interfaces
        for interface_name, addresses in psutil.net_if_addrs().items():
            network_info["interfaces"][interface_name] = []
            for addr in addresses:
                network_info["interfaces"][interface_name].append(
                    {
                        "address": addr.address,
                        "netmask": addr.netmask,
                        "family": str(addr.family),
                    }
                )

        # Get IO statistics
        try:
            io_counters = psutil.net_io_counters(pernic=True)
            for nic, counters in io_counters.items():
                network_info["io_counters"][nic] = {
                    "bytes_sent": counters.bytes_sent,
                    "bytes_recv": counters.bytes_recv,
                    "packets_sent": counters.packets_sent,
                    "packets_recv": counters.packets_recv,
                    "errors_in": counters.errin,
                    "errors_out": counters.errout,
                    "drop_in": counters.dropin,
                    "drop_out": counters.dropout,
                }
        except Exception as e:
            network_info["io_counters"] = {"error": f"Network IO statistics not available: {str(e)}"}

        return network_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting network info: {str(e)}")


def get_system_info() -> Dict:
    try:
        boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        system_info = {
            "platform": get_platform_info(),
            "boot_time": boot_time,
            "cpu": get_cpu_info(),
            "memory": get_memory_info(),
            "disks": get_disk_info(),
            "network": get_network_info(),
        }

        return system_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting system info: {str(e)}")
