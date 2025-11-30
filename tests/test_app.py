import unittest
import os
import shutil
from textual.widgets import Input, Button
from ssh_manager.main import SSHManagerApp
from ssh_manager.config_parser import ConfigManager

class TestSSHManager(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Create a temporary config file
        self.test_dir = os.path.dirname(__file__)
        self.test_config_source = os.path.join(self.test_dir, "test_config")
        self.test_config_path = os.path.join(self.test_dir, "temp_config")
        shutil.copy(self.test_config_source, self.test_config_path)
        self.app = SSHManagerApp(config_path=self.test_config_path)

    async def asyncTearDown(self):
        if os.path.exists(self.test_config_path):
            os.remove(self.test_config_path)

    async def test_load_hosts(self):
        async with self.app.run_test(size=(80, 40)) as pilot:
            # Check if hosts are loaded
            # We can access the app instance via pilot.app
            assert len(pilot.app.config_manager.hosts) == 2
            assert pilot.app.config_manager.hosts[0].name == "myserver"

    async def test_add_host(self):
        async with self.app.run_test(size=(80, 40)) as pilot:
            # Trigger add host action
            await pilot.press("a")
            
            # Fill form
            await pilot.click("#alias")
            await pilot.press(*list("newhost"))
            
            await pilot.click("#hostname")
            await pilot.press(*list("10.0.0.1"))
            
            await pilot.click("#user")
            await pilot.press(*list("root"))
            
            # Save
            await pilot.click("#save_btn")
            
            # Check if added to config manager
            assert len(pilot.app.config_manager.hosts) == 3
            assert pilot.app.config_manager.hosts[2].name == "newhost"
            
            # Verify file content
            with open(self.test_config_path, 'r') as f:
                content = f.read()
                assert "Host newhost" in content
                assert "HostName 10.0.0.1" in content

if __name__ == "__main__":
    unittest.main()
