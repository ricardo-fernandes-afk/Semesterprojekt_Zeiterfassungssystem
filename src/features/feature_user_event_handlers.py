from db.db_connection import create_connection

class UserEventHandlers:
    def __init__(self, project_frame, selected_frame):
        self.project_frame = project_frame
        self.selected_frame = selected_frame

    def on_project_double_click(self, event):
        project_number, project_name, description = self.get_selected_project()
        if project_number:
            # Aktualisiere den SelectedFrame
            self.selected_frame.update_project_details(
                selected_id=project_number,
                selected_name=project_name,
                description=description
            )
            self.selected_frame.master.selected_project_number = project_number
        else:
            print("Kein Projekt ausgewählt.")

    def get_selected_project(self):
        try:
            selected_item = self.project_frame.project_treeview.selection()[0]
            project_values = self.project_frame.project_treeview.item(selected_item, 'values')
            print(f"Ausgewähltes Projekt: {project_values}")
            return project_values[0], project_values[1], project_values[2]
        except IndexError:
            return None, None, None
