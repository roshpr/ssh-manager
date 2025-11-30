from textual.app import ComposeResult
from textual.widgets import Static, Button, Label, Input, ListItem, ListView, Header, Footer
from textual.containers import Container, Vertical, Horizontal
from textual.screen import ModalScreen, Screen
from textual.binding import Binding
from textual.reactive import reactive
from textual import on

class HostListItem(ListItem):
    highlighted = reactive(False)
    
    def __init__(self, host_obj):
        super().__init__()
        self.host_obj = host_obj

    def compose(self) -> ComposeResult:
        # Get hostname and user from config
        hostname = self.host_obj.config.get('HostName', 'N/A')
        user = self.host_obj.config.get('User', 'N/A')
        
        # Create label with space for arrow (initially no arrow, just spacing)
        label_text = f"  [bold #1976d2]🖥️  {self.host_obj.name}[/]  [#616161]{user}@{hostname}[/]"
        yield Label(label_text, markup=True, id="host-label")
    
    def watch_highlighted(self, highlighted: bool) -> None:
        """Update the label when highlight state changes"""
        # Only update if the widget is mounted
        if not self.is_mounted:
            return
            
        try:
            label = self.query_one("#host-label", Label)
            hostname = self.host_obj.config.get('HostName', 'N/A')
            user = self.host_obj.config.get('User', 'N/A')
            
            if highlighted:
                # Add arrow when highlighted
                label_text = f"[bold #ff6f00]▶[/] [bold #1976d2]🖥️  {self.host_obj.name}[/]  [#616161]{user}@{hostname}[/]"
            else:
                # No arrow when not highlighted
                label_text = f"  [bold #1976d2]🖥️  {self.host_obj.name}[/]  [#616161]{user}@{hostname}[/]"
            
            label.update(label_text)
        except Exception:
            # Silently ignore if label not found
            pass

class HostListView(ListView):
    def __init__(self, hosts):
        super().__init__()
        self.hosts = hosts

    def on_mount(self):
        for host in self.hosts:
            self.append(HostListItem(host))
    
    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """Update highlighted state when selection changes"""
        # Clear all highlights first
        for item in self.query(HostListItem):
            item.highlighted = False
        
        # Set the new highlighted item
        if event.item and isinstance(event.item, HostListItem):
            event.item.highlighted = True

class DetailScreen(ModalScreen):
    BINDINGS = [("escape", "app.pop_screen", "Close")]

    def __init__(self, host_obj):
        super().__init__()
        self.host_obj = host_obj

    def compose(self) -> ComposeResult:
        with Container(id="detail-view"):
            yield Label(f"Host: {self.host_obj.name}", classes="label")
            for k, v in self.host_obj.config.items():
                yield Label(f"{k}: {v}", classes="label")
            yield Button("Close", variant="primary", id="close_btn")

    @on(Button.Pressed, "#close_btn")
    def close_screen(self):
        self.dismiss()

class AddHostScreen(ModalScreen):
    BINDINGS = [("escape", "app.pop_screen", "Cancel")]

    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.identity_files = config_manager.get_identity_files()

    def compose(self) -> ComposeResult:
        with Container(id="add-host-container"):
            yield Label("Add New Host", classes="header")
            yield Input(placeholder="Host Alias (e.g. my-server)", id="alias")
            yield Input(placeholder="Hostname (IP or domain)", id="hostname")
            yield Input(placeholder="User", id="user")
            
            # For IdentityFile, we could use a Select, but Input is simpler for now.
            # We can suggest files or just let them type. 
            # Requirement: "should list all existing identity files".
            # I'll use a placeholder for now, or maybe a datalist if Textual supports it (it doesn't natively yet easily).
            # I'll just list them in a label or use a simplified selection logic if I had more time.
            # For now, I'll use an Input but show available keys in a label above it.
            
            ident_files_str = ", ".join(self.identity_files) if self.identity_files else "None found"
            yield Label(f"Available Keys: {ident_files_str}", classes="label")
            yield Input(placeholder="IdentityFile (e.g. id_rsa)", id="identity_file")
            
            yield Input(placeholder="ProxyJump (Optional)", id="proxy_jump")
            yield Input(placeholder="ForwardAgent (yes/no)", id="forward_agent")
            
            with Horizontal():
                yield Button("Save", variant="success", id="save_btn")
                yield Button("Cancel", variant="error", id="cancel_btn")

    @on(Button.Pressed, "#save_btn")
    def save_host(self):
        alias = self.query_one("#alias", Input).value
        hostname = self.query_one("#hostname", Input).value
        user = self.query_one("#user", Input).value
        identity_file = self.query_one("#identity_file", Input).value
        proxy_jump = self.query_one("#proxy_jump", Input).value
        forward_agent = self.query_one("#forward_agent", Input).value

        if alias and hostname and user:
            self.config_manager.add_host(
                alias, hostname, user, 
                identity_file if identity_file else None,
                proxy_jump if proxy_jump else None,
                forward_agent if forward_agent else None
            )
            self.dismiss(True) # Return True to indicate success
        else:
            # Show error or just don't submit
            pass

    @on(Button.Pressed, "#cancel_btn")
    def cancel(self):
        self.dismiss(False)
