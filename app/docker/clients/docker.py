from typing import Any, Dict, List, Optional

import docker
from docker.errors import DockerException
from fastapi import HTTPException

from ..models import ContainerDetailResponse, ContainerListResponse, ContainerOperationResponse


class DockerClient:
    def __init__(self):
        try:
            self.client = docker.from_env()
        except DockerException as e:
            raise HTTPException(status_code=500, detail=f"Failed to connect to Docker: {str(e)}")

    def _format_ports(self, ports: Dict[str, Any]) -> Dict[str, Any]:
        """Format ports from Docker API format to our format"""
        if not ports:
            return {}
        formatted_ports = {}
        for container_port, host_bindings in ports.items():
            if host_bindings:
                formatted_ports[container_port] = host_bindings[0] if isinstance(host_bindings, list) else host_bindings
        return formatted_ports

    def _format_volumes(self, mounts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format volume mounts from Docker API format to our format"""
        if not mounts:
            return []
        return [
            {
                "source": mount.get("Source", ""),
                "destination": mount.get("Destination", ""),
                "type": mount.get("Type", ""),
                "readonly": mount.get("RW", False),
            }
            for mount in mounts
        ]

    def _format_environment(self, env: List[str]) -> List[str]:
        """Format environment variables from Docker API format to our format"""
        return env if env else []

    def _format_command(self, cmd: Optional[List[str]]) -> Optional[str]:
        """Format command from Docker API format to our format"""
        if not cmd:
            return None
        return " ".join(cmd) if isinstance(cmd, list) else cmd

    async def list_containers(self, all_containers: bool = False) -> List[ContainerListResponse]:
        """List all containers"""
        try:
            containers = self.client.containers.list(all=all_containers)
            return [
                ContainerListResponse(
                    id=container.id,
                    name=container.name,
                    status=container.status,
                    image=container.image.tags[0] if container.image.tags else container.image.id,
                    created=container.attrs["Created"],
                    ports=self._format_ports(container.ports),
                    volumes=self._format_volumes(container.attrs["Mounts"]),
                    devices=container.attrs["HostConfig"]["Devices"] if container.attrs["HostConfig"].get("Devices") else [],
                    environment=self._format_environment(container.attrs["Config"]["Env"]),
                    privileged=container.attrs["HostConfig"]["Privileged"],
                    restart_policy=container.attrs["HostConfig"]["RestartPolicy"]["Name"],
                    cpu_allocation=self._get_cpu_allocation(container.attrs["HostConfig"]),
                    network=container.attrs["NetworkSettings"]["Networks"],
                    command=self._format_command(container.attrs["Config"]["Cmd"]),
                    tag=container.image.tags[0].split(":")[1]
                    if container.image.tags and ":" in container.image.tags[0]
                    else None,
                )
                for container in containers
            ]
        except DockerException as e:
            raise HTTPException(status_code=500, detail=f"Failed to list containers: {str(e)}")

    def _get_cpu_allocation(self, host_config: Dict) -> str:
        """Convert CPU shares to allocation level"""
        cpu_shares = host_config.get("CpuShares", 1024)
        if cpu_shares <= 512:
            return "low"
        elif cpu_shares <= 1024:
            return "medium"
        return "high"

    async def create_container(
        self,
        image: str,
        name: str,
        tag: Optional[str] = None,
        web_ui: Optional[Dict] = None,
        network: Optional[str] = None,
        ports: Optional[Dict[str, str]] = None,
        volumes: Optional[Dict[str, str]] = None,
        environment: Optional[Dict[str, str]] = None,
        devices: Optional[List[str]] = None,
        command: Optional[str] = None,
        privileged: bool = False,
        cpu_allocation: str = "low",
        restart_policy: str = "unless-stopped",
    ) -> ContainerDetailResponse:
        """Create a new container"""
        try:
            # Prepare image name with tag
            image_with_tag = f"{image}:{tag}" if tag else image

            # Convert CPU allocation to shares
            cpu_shares = {"low": 512, "medium": 1024, "high": 2048}.get(cpu_allocation.lower(), 1024)

            # Convert environment dict to list of strings
            env_list = [f"{k}={v}" for k, v in (environment or {}).items()]

            # Prepare host config
            host_config = self.client.api.create_host_config(
                privileged=privileged,
                cpu_shares=cpu_shares,
                restart_policy={"Name": restart_policy},
                devices=devices if devices else None,
                port_bindings=ports if ports else None,
                binds=volumes if volumes else None,
                network_mode=network if network else None,
            )

            # Create container
            container = self.client.containers.create(
                image=image_with_tag,
                name=name,
                command=command.split() if command else None,
                environment=env_list,
                host_config=host_config,
                detach=True,
            )

            return await self.get_container(container.id)
        except DockerException as e:
            raise HTTPException(status_code=500, detail=f"Failed to create container: {str(e)}")

    async def get_container(self, container_id: str) -> ContainerDetailResponse:
        """Get container details"""
        try:
            container = self.client.containers.get(container_id)
            attrs = container.attrs
            return ContainerDetailResponse(
                id=container.id,
                name=container.name,
                status=container.status,
                image=container.image.tags[0] if container.image.tags else container.image.id,
                created=attrs["Created"],
                ports=self._format_ports(container.ports),
                environment=self._format_environment(attrs["Config"]["Env"]),
                volumes=self._format_volumes(attrs["Mounts"]),
                devices=attrs["HostConfig"]["Devices"] if attrs["HostConfig"].get("Devices") else [],
                privileged=attrs["HostConfig"]["Privileged"],
                restart_policy=attrs["HostConfig"]["RestartPolicy"]["Name"],
                cpu_allocation=self._get_cpu_allocation(attrs["HostConfig"]),
                network=attrs["NetworkSettings"]["Networks"],
                command=self._format_command(attrs["Config"]["Cmd"]),
                tag=container.image.tags[0].split(":")[1] if container.image.tags and ":" in container.image.tags[0] else None,
            )
        except DockerException as e:
            raise HTTPException(status_code=404, detail=f"Container not found: {str(e)}")

    async def update_container(self, container_id: str, **kwargs) -> ContainerDetailResponse:
        """Update container configuration"""
        try:
            container = self.client.containers.get(container_id)
            container.update(**kwargs)
            return await self.get_container(container_id)
        except DockerException as e:
            raise HTTPException(status_code=500, detail=f"Failed to update container: {str(e)}")

    async def delete_container(self, container_id: str, force: bool = False) -> ContainerOperationResponse:
        """Delete a container"""
        try:
            container = self.client.containers.get(container_id)
            container.remove(force=force)
            return ContainerOperationResponse(message=f"Container {container_id} successfully deleted")
        except DockerException as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete container: {str(e)}")

    async def start_container(self, container_id: str) -> ContainerDetailResponse:
        """Start a container"""
        try:
            container = self.client.containers.get(container_id)
            container.start()
            return await self.get_container(container_id)
        except DockerException as e:
            raise HTTPException(status_code=500, detail=f"Failed to start container: {str(e)}")

    async def stop_container(self, container_id: str) -> ContainerDetailResponse:
        """Stop a container"""
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            return await self.get_container(container_id)
        except DockerException as e:
            raise HTTPException(status_code=500, detail=f"Failed to stop container: {str(e)}")

    async def restart_container(self, container_id: str) -> ContainerDetailResponse:
        """Restart a container"""
        try:
            container = self.client.containers.get(container_id)
            container.restart()
            return await self.get_container(container_id)
        except DockerException as e:
            raise HTTPException(status_code=500, detail=f"Failed to restart container: {str(e)}")
