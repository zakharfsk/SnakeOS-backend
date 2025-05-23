from typing import List

from fastapi import APIRouter, Depends

from ..auth.utils import get_current_user
from ..models import User
from .clients import DockerClient
from .schemas import ContainerCreate, ContainerDetailResponse, ContainerListResponse, ContainerOperationResponse, ContainerUpdate

router = APIRouter(prefix="/docker", tags=["docker"])


async def get_docker_client() -> DockerClient:
    return DockerClient()


@router.get("/containers", response_model=List[ContainerListResponse])
async def list_containers(
    all_containers: bool = False,
    client: DockerClient = Depends(get_docker_client),
    _: User = Depends(get_current_user),
):
    """List all Docker containers"""
    return await client.list_containers(all_containers)


@router.post("/containers", response_model=ContainerDetailResponse)
async def create_container(
    container: ContainerCreate,
    client: DockerClient = Depends(get_docker_client),
    _: User = Depends(get_current_user),
):
    """Create a new Docker container"""
    return await client.create_container(
        image=container.image,
        name=container.name,
        tag=container.tag,
        web_ui=container.web_ui.model_dump() if container.web_ui else None,
        network=container.network,
        ports=container.ports,
        volumes=container.volumes,
        environment=container.environment,
        devices=container.devices,
        command=container.command,
        privileged=container.privileged,
        cpu_allocation=container.cpu_allocation,
        restart_policy=container.restart_policy,
    )


@router.get("/containers/{container_id}", response_model=ContainerDetailResponse)
async def get_container(
    container_id: str,
    client: DockerClient = Depends(get_docker_client),
    _: User = Depends(get_current_user),
):
    """Get details of a specific container"""
    return await client.get_container(container_id)


@router.put("/containers/{container_id}", response_model=ContainerDetailResponse)
async def update_container(
    container_id: str,
    container: ContainerUpdate,
    client: DockerClient = Depends(get_docker_client),
    _: User = Depends(get_current_user),
):
    """Update container configuration"""
    return await client.update_container(container_id, **container.dict(exclude_unset=True))


@router.delete("/containers/{container_id}", response_model=ContainerOperationResponse)
async def delete_container(
    container_id: str,
    force: bool = False,
    client: DockerClient = Depends(get_docker_client),
    _: User = Depends(get_current_user),
):
    """Delete a container"""
    return await client.delete_container(container_id, force)


@router.post("/containers/{container_id}/start", response_model=ContainerDetailResponse)
async def start_container(
    container_id: str,
    client: DockerClient = Depends(get_docker_client),
    _: User = Depends(get_current_user),
):
    """Start a container"""
    return await client.start_container(container_id)


@router.post("/containers/{container_id}/stop", response_model=ContainerDetailResponse)
async def stop_container(
    container_id: str,
    client: DockerClient = Depends(get_docker_client),
    _: User = Depends(get_current_user),
):
    """Stop a container"""
    return await client.stop_container(container_id)


@router.post("/containers/{container_id}/restart", response_model=ContainerDetailResponse)
async def restart_container(
    container_id: str,
    client: DockerClient = Depends(get_docker_client),
    _: User = Depends(get_current_user),
):
    """Restart a container"""
    return await client.restart_container(container_id)
