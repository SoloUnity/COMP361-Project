from gui.tab import Tab 
from models.project import Project

class TabManager:
    def __init__(self):
        """Initialize the tab manager with an empty list of tabs."""
        self.tabs = []
        self.active_tab_index = None  # No active tab initially

    def add_tab(self, tab_id, position, project=None):
        """Add a new tab to the manager."""
        if project == None:
            new_project = Project(tab_id)  #create a new project
            new_tab = Tab(new_project, tab_id, position)
        else:
            new_tab = Tab(project,tab_id, position)
        self.tabs.append(new_tab)

        # Switch to the newly added tab
        self.active_tab_index = len(self.tabs) - 1
        self.select_tab(new_tab.tab_id)  # Ensure only this tab is selected

    def remove_tab(self, tab_id):
        """Remove a tab by its ID."""
        self.tabs = [tab for tab in self.tabs if tab.tab_id != tab_id]

        # Adjust active tab index if necessary
        if self.active_tab_index is not None:
            if self.active_tab_index >= len(self.tabs):
                self.active_tab_index = len(self.tabs) - 1  # Set to last tab
            if len(self.tabs) == 0:
                self.active_tab_index = None  # No tabs left

    def select_tab(self, tab_id):
        """Set a tab as the active tab based on its ID."""
        for index, tab in enumerate(self.tabs):
            tab.is_selected = (tab.tab_id == tab_id)  # Only the selected tab is set to True
            if tab.tab_id == tab_id:
                self.active_tab_index = index
        return

    def get_active_tab(self):
        """Return the currently active tab."""
        if self.active_tab_index is not None and 0 <= self.active_tab_index < len(self.tabs):
            return self.tabs[self.active_tab_index]
        return None  # No active tab

    def get_tab_by_id(self, tab_id):
        """Return a tab by its ID."""
        for tab in self.tabs:
            if tab.tab_id == tab_id:
                return tab
        return None

