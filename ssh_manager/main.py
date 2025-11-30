import os
import sys
import shutil
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, ListItem, ListView, Input, Static
from textual.containers import Container, Horizontal
from textual import on
from .config_parser import ConfigManager
from .tui import HostListView, AddHostScreen, DetailScreen, HostListItem

class CustomHeader(Static):
    """Custom header with icon, title, and copyright"""
    
    def compose(self) -> ComposeResult:
        with Horizontal(id="header-container"):
            yield Label("🔐 SSH Manager", id="header-title")
            yield Label("© Rosh PR", id="header-copyright")

class SSHManagerApp(App):
    CSS_PATH = "ssh_manager.css"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("a", "add_host", "Add Host"),
        ("d", "show_details", "Details"),
        ("/", "focus_search", "Search"),
    ]

    def __init__(self, config_path=None):
        super().__init__()
        # Allow overriding config path for testing
        self.config_path = config_path or os.path.expanduser("~/.ssh/config")
        self.config_manager = ConfigManager(self.config_path)
        self.config_manager.load_hosts()
        self.all_hosts = self.config_manager.hosts

    def compose(self) -> ComposeResult:
        with Container(id="app-container"):
            yield CustomHeader()
            yield Footer()
            yield Label("Search (/) | Select host (Enter) | Details (d) | Add (a)", classes="label")
            yield Input(placeholder="Type to search hosts...", id="search-input")
            # Container to hold the list, allowing us to refresh it
            with Container(id="list-container"):
                yield HostListView(self.all_hosts)

    def action_focus_search(self):
        """Focus the search input"""
        search_input = self.query_one("#search-input", Input)
        search_input.focus()

    @on(Input.Changed, "#search-input")
    def filter_hosts(self, event: Input.Changed):
        """Filter hosts based on search query with fuzzy matching"""
        query = event.value.lower().strip()
        
        if not query:
            # Show all hosts if search is empty
            filtered_hosts = self.all_hosts
        else:
            # Fuzzy matching: check if all characters in query appear in order in host name
            filtered_hosts = []
            for host in self.all_hosts:
                host_name = host.name.lower()
                query_idx = 0
                
                for char in host_name:
                    if query_idx < len(query) and char == query[query_idx]:
                        query_idx += 1
                
                # If all query characters were found in order, include this host
                if query_idx == len(query):
                    filtered_hosts.append(host)
        
        # Update the list view
        list_container = self.query_one("#list-container")
        list_container.query("HostListView").remove()
        list_container.mount(HostListView(filtered_hosts))

    def action_add_host(self):
        def check_add(added: bool):
            if added:
                self.refresh_list()
        self.push_screen(AddHostScreen(self.config_manager), check_add)

    def action_show_details(self):
        list_view = self.query_one(HostListView)
        if list_view.highlighted_child:
            host_item = list_view.highlighted_child
            if isinstance(host_item, HostListItem):
                self.push_screen(DetailScreen(host_item.host_obj))

    @on(ListView.Selected)
    def on_host_selected(self, event: ListView.Selected):
        host_item = event.item
        if isinstance(host_item, HostListItem):
            host_name = host_item.host_obj.name
            self.exit(result=host_name)

    def refresh_list(self):
        # Reload hosts and rebuild list
        self.config_manager.load_hosts()
        self.all_hosts = self.config_manager.hosts
        
        # Clear search and show all hosts
        search_input = self.query_one("#search-input", Input)
        search_input.value = ""
        
        list_container = self.query_one("#list-container")
        list_container.query("HostListView").remove()
        list_container.mount(HostListView(self.all_hosts))

def main():
    # Check for test config arg
    config_arg = sys.argv[1] if len(sys.argv) > 1 else None
    app = SSHManagerApp(config_path=config_arg)
    result = app.run()
    
    if result:
        # Clear screen to ensure clean terminal for ssh
        print(f"\033[H\033[JConnecting to {result}...", flush=True)
        try:
            # Replace process with ssh
            # We use the full path to ssh to be safe, or just rely on PATH
            ssh_path = shutil.which("ssh") or "/usr/bin/ssh"
            os.execvp(ssh_path, ["ssh", result])
        except Exception as e:
            print(f"Error launching ssh: {e}")

if __name__ == "__main__":
    main()


