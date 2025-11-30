import os
import re
from typing import List, Dict, Optional

class SSHHost:
    def __init__(self, name: str, config: Dict[str, str]):
        self.name = name
        self.config = config

    def to_string(self) -> str:
        lines = [f"Host {self.name}"]
        for key, value in self.config.items():
            lines.append(f"    {key} {value}")
        return "\n".join(lines)

class ConfigManager:
    def __init__(self, config_path: str = "~/.ssh/config"):
        self.config_path = os.path.expanduser(config_path)
        self.hosts: List[SSHHost] = []

    def load_hosts(self):
        self.hosts = []
        if not os.path.exists(self.config_path):
            return

        with open(self.config_path, 'r') as f:
            lines = f.readlines()

        current_host = None
        current_config = {}

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split(maxsplit=1)
            if not parts:
                continue

            key = parts[0]
            value = parts[1] if len(parts) > 1 else ""

            if key.lower() == 'host':
                if current_host:
                    self.hosts.append(SSHHost(current_host, current_config))
                current_host = value
                current_config = {}
            elif current_host:
                # Normalize key to title case for consistency
                normalized_key = key.capitalize()
                if key.lower() == 'hostname':
                    normalized_key = 'HostName'
                elif key.lower() == 'identityfile':
                    normalized_key = 'IdentityFile'
                elif key.lower() == 'proxyjump':
                    normalized_key = 'ProxyJump'
                elif key.lower() == 'forwardagent':
                    normalized_key = 'ForwardAgent'
                current_config[normalized_key] = value

        if current_host:
            self.hosts.append(SSHHost(current_host, current_config))

    def add_host(self, name: str, hostname: str, user: str, identity_file: Optional[str] = None, 
                 proxy_jump: Optional[str] = None, forward_agent: Optional[str] = None):
        
        config = {
            "HostName": hostname,
            "User": user,
        }
        if identity_file:
            config["IdentityFile"] = identity_file
        if proxy_jump:
            config["ProxyJump"] = proxy_jump
        if forward_agent:
            config["ForwardAgent"] = forward_agent

        new_host = SSHHost(name, config)
        self.hosts.append(new_host)
        self.save_host(new_host)

    def save_host(self, host: SSHHost):
        # Appends the new host to the file
        with open(self.config_path, 'a') as f:
            f.write("\n" + host.to_string() + "\n")

    def get_identity_files(self) -> List[str]:
        ssh_dir = os.path.dirname(self.config_path)
        if not os.path.exists(ssh_dir):
            return []
        
        files = []
        try:
            for f in os.listdir(ssh_dir):
                if f.startswith('id_') and not f.endswith('.pub'):
                    files.append(f)
                elif f.endswith('.pem'):
                    files.append(f)
        except OSError:
            pass
        return sorted(files)
