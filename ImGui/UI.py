import sys
import dearpygui.dearpygui as dpg
import dearpygui_extend as dpge


class StdoutRedirector:
    def __init__(self, log_parent):
        self.log_parent = log_parent

    def write(self, text):
        if text.strip() != "":
            dpg.add_text(text, parent=self.log_parent)
            dpg.set_y_scroll(self.log_parent, dpg.get_y_scroll_max(self.log_parent))

    def flush(self):
        pass


def show_plugin_info(name, description):
    tag = f"{name}_info"
    if dpg.does_item_exist(tag):
        dpg.delete_item(tag)  # reopen clean

    with dpg.window(label=f"{name} Info", tag=tag, width=300, height=200,
                    modal=True, no_collapse=True, no_resize=True):
        dpg.add_text(description, wrap=280)
        dpg.add_spacer(height=100)
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=90)
            dpg.add_button(label="Close", width=75, callback=lambda: dpg.delete_item(tag))


# Clear log
def clear_log(sender, app_data, user_data):
    dpg.delete_item("log_window", children_only=True)


# Example script function that prints
def run_script(sender, app_data, user_data):
    print("Running scripts...")
    print("Running MapperScript...")
    print("MapperScript completed successfully.")
    print("Running Another Script...")
    print("Another Script completed successfully.")
    print("Running Yet Another Script...")
    print("Yet Another Script completed successfully.")
    print("All done")


# === FILE DIALOG CALLBACK ===
def callback(sender, app_data, user_data):
    file_path = app_data["file_path_name"]
    file_name = app_data["file_name"]

    # Create new button before "Add Script"
    dpg.add_button(
        label=f"- {file_name}",
        parent="scripts_group",
        before="add_script_button",
        callback=lambda s, a, u, fn=file_name: print(f"Running {fn}...")
    )

    print(f"Added script: {file_name}")


dpg.create_context()
dpg.create_viewport(title="Dockable Layout", width=1000, height=600)

# Enable docking everywhere
dpg.configure_app(docking=True, docking_space=True)

# Dockable windows
with dpg.window(label="Plugins", tag="Plugins"):
    dpg.add_button(label="- Pico Sensors", callback=lambda: show_plugin_info("Pico Sensors", "This plugin handles Pico board sensor input."))
    dpg.add_button(label="- Idk What This Is", callback=lambda: show_plugin_info("Mystery Plugin", "This plugin's purpose is unknown"))
    dpg.add_button(label="- Other Plugin", callback=lambda: show_plugin_info("Other Plugin", "Generic plugin for other tasks."))

with dpg.window(label="Scripts", tag="Scripts"):
    with dpg.group(tag="scripts_group"):
        dpg.add_button(label="- MapperScript")
        dpg.add_button(label="- Another Script")
        dpg.add_button(label="- Yet Another Script")
        dpg.add_button(label="Add Script", tag="add_script_button", callback=lambda: dpg.show_item("file_dialog_id"))

with dpg.window(label="ScriptRunner", tag="ScriptRunner"):
    dpg.add_text("Output Log:", bullet=True)
    with dpg.child_window(tag="log_window", width=-1, height=350, autosize_x=True):
        pass
    dpg.add_button(label="Clear Log", width=75, callback=clear_log)
    dpg.add_button(label="Run Script", width=75, callback=run_script)

with dpg.file_dialog(directory_selector=False, show=False, callback=callback, id="file_dialog_id", width=700, height=400):
    dpg.add_file_extension(".lua", color=(0, 255, 0, 255), custom_text="[Lua]")


# Redirect Python's stdout
sys.stdout = StdoutRedirector("log_window")


# Arrange docking AFTER startup
def setup_docking(sender, app_data):
    dpg.dock("Plugins", "DockSpace")
    dpg.dock("Scripts", "Plugins", slot=2)
    dpg.dock("ScriptRunner", "DockSpace", slot=1)
    dpg.delete_item(sender)


with dpg.window(show=False):
    dpg.set_frame_callback(1, setup_docking)


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
