from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class WebUIConfig(BaseModel):
    """Web UI configuration for the container"""

    protocol: str = Field(..., description="Protocol (http/https)")
    host: str = Field(..., description="Host address")
    port: int = Field(..., description="Port number")
    path: str = Field(..., description="Path")


class ContainerBase(BaseModel):
    """Base model for container operations"""

    name: str = Field(..., description="Name of the container")
    image: str = Field(..., description="Docker image to use")
    tag: Optional[str] = Field(None, description="Image tag/version")
    icon_url: Optional[str] = Field(None, description="URL for the container's icon")
    web_ui: Optional[WebUIConfig] = Field(None, description="Web UI configuration")
    network: Optional[Union[str, Dict[str, Any]]] = Field(None, description="Network name or configuration")
    ports: Optional[Dict[str, Any]] = Field(None, description="Port mappings")
    volumes: Optional[List[Dict[str, Any]]] = Field(None, description="Volume mappings")
    environment: Optional[List[str]] = Field(None, description="Environment variables")
    devices: Optional[List[str]] = Field(None, description="Device mappings")
    command: Optional[Union[str, List[str]]] = Field(None, description="Container command")
    privileged: Optional[bool] = Field(False, description="Privileged mode")
    cpu_allocation: Optional[str] = Field("low", description="CPU allocation (low/medium/high)")
    restart_policy: Optional[str] = Field("unless-stopped", description="Restart policy")


class ContainerCreate(ContainerBase):
    """Model for creating a new container"""

    pass


class ContainerUpdate(ContainerBase):
    """Model for updating an existing container"""

    pass


class ContainerResponse(ContainerBase):
    """Model for container response data"""

    id: str = Field(..., description="Container ID")
    status: str = Field(..., description="Container status")
    created: Optional[str] = Field(None, description="Container creation timestamp")


class ContainerListResponse(ContainerResponse):
    """Model for container list response"""

    pass


class ContainerDetailResponse(ContainerResponse):
    """Model for detailed container information"""

    ports: Dict[str, Any] = Field(..., description="Container port mappings")
    environment: List[str] = Field(..., description="Container environment variables")
    volumes: List[Dict[str, Any]] = Field(..., description="Container volume mappings")
    devices: List[str] = Field(..., description="Container device mappings")


class ContainerOperationResponse(BaseModel):
    """Model for container operation responses"""

    message: str = Field(..., description="Operation result message")
