from gui.tab import Tab 
from models.project import Project

class TabManager:
    def __init__(self):
        """Initialize the tab manager with an empty list of tabs."""
        self.tabs = [None] * 10 # max 10 tabs
        self.active_tab_index = None  # No active tab initially

    def add_tab(self, position, project=None):
        """Add a new tab to the manager."""
        if project == None:
            new_project = Project(position)  #create a new project
            new_tab = Tab(new_project, tab_id=position, position=position)
        else:
            new_tab = Tab(project,tab_id=position, position=position)
        self.tabs[position] = new_tab

        # Switch to the newly added tab
        self.active_tab_index = position
        self.select_tab(new_tab.tab_id)  # Ensure only this tab is selected

    def remove_tab(self, tab_id):
        """Remove a tab by its ID and switch to the closest available tab, keeping gaps."""
        if not self.tabs:
            return  # No tabs to remove

        # Find the index of the tab to remove
        tab_index = next((i for i, tab in enumerate(self.tabs) if tab and tab.tab_id == tab_id), None)

        if tab_index is None:
            return  # Tab ID not found

        # Remove the tab by replacing it with None (to keep gaps)
        self.tabs[tab_index] = None  

        print("Removing tab:", tab_index)
        print("Active tab index before removal:", self.active_tab_index)
      
        # Determine the new active tab
        if self.active_tab_index == tab_index:
            new_index = None

            # Check previous tabs first
            for i in range(tab_index - 1, -1, -1):
                if self.tabs[i] is not None:
                    new_index = i
                    break

            # If no previous tab found, check next tabs
            if new_index is None:
                for i in range(tab_index + 1, len(self.tabs)):
                    if self.tabs[i] is not None:
                        new_index = i
                        break

            # Update active tab index
            self.active_tab_index = new_index

        print("Tabs after removal:", self.tabs)
        print("Active tab after removal:", self.active_tab_index)

        # """Remove a tab by its ID."""
        # self.tabs = [tab for tab in self.tabs if tab.tab_id != tab_id]

        # # Adjust active tab index if necessary
        # if self.active_tab_index is not None:
        #     if self.active_tab_index >= len(self.tabs):
        #         self.active_tab_index = len(self.tabs) - 1  # Set to last tab
        #     if len(self.tabs) == 0:
        #         self.active_tab_index = None  # No tabs left

        # print(self.tabs)

    def select_tab(self, tab_id):
        """Set a tab as the active tab based on its ID."""
        for index, tab in enumerate(filter(None, self.tabs)):
            tab.is_selected = (tab.tab_id == tab_id)  # Only the selected tab is set to True
            if tab.tab_id == tab_id:
                self.active_tab_index = tab_id
        print("Selected tab using select_tab: ", self.active_tab_index)
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
    

