# /mnt/g/ai/projects/neurocore/tools/__init__.py

from tools.base_tool import BaseTool, ToolValidationError, ToolExecutionError
from tools.tool_registry import ToolRegistry, registry
from tools.execution_engine import ExecutionEngine

# System tools
from tools.system.system_info import SystemInfo
from tools.system.process_top import ProcessTop
from tools.system.disk_usage import DiskUsage
from tools.system.memory_usage import MemoryUsage
from tools.system.disk_layout import DiskLayout
from tools.system.network_interfaces import NetworkInterfaces
from tools.system.network_connections import NetworkConnections
from tools.system.uptime_load import UptimeLoad
from tools.system.system_logs import SystemLogs
from tools.system.users_sessions import UsersSessions
from tools.system.recent_logins import RecentLogins

# Control tools
from tools.system.service_manager import ServiceManager

# Argus tools
from tools.argus.system_summary import SystemSummary


def register_tools():
    # System tools
    registry.register(SystemInfo())
    registry.register(ProcessTop())
    registry.register(DiskUsage())
    registry.register(MemoryUsage())
    registry.register(DiskLayout())
    registry.register(NetworkInterfaces())
    registry.register(NetworkConnections())
    registry.register(UptimeLoad())
    registry.register(SystemLogs())
    registry.register(UsersSessions())
    registry.register(RecentLogins())

    # Control tools
    registry.register(ServiceManager())

    # Argus tools
    registry.register(SystemSummary())


register_tools()

__all__ = [
    "BaseTool",
    "ToolValidationError",
    "ToolExecutionError",
    "ToolRegistry",
    "registry",
    "ExecutionEngine",
]