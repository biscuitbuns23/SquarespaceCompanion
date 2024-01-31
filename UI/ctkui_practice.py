import tkinter as tk
import customtkinter
from PIL import Image, ImageTk
from functools import wraps

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Squarespace Companion")
        self.geometry(f"{1100}x{580}")
        self.active_widget = None
        self._current_widget = None
        self._current_view = None

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2,3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Menu logo
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Menu",
                                                 font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20,10))
        
        # Create products button
        self.create_prod_button = customtkinter.CTkButton(self.sidebar_frame, text="Create Products", width = 140)
        self.create_prod_button.grid(row=1, column=0, padx=20, pady=(10, 10))

        # Settings button
        self.settings_button = customtkinter.CTkButton(self.sidebar_frame, text="Settings", width = 140,
                                                       command=self.view_toggle(view=SettingsView, parent=self))
        self.settings_button.grid(row=2, column=0, padx=20, pady=(10, 10))

        # info button
        self.info_button = customtkinter.CTkButton(self.sidebar_frame, text="Info", width = 140,
                                                   command=self.clear_view)
        self.info_button.grid(row=3, column=0, padx=20, pady=(10, 10))

        # create second sidebar frame for practice
        self.sidebar_frame2 = customtkinter.CTkFrame(self, width=200, corner_radius=2)
        self.sidebar_frame2.grid(row=0, column=2, rowspan=4, padx=40,  sticky="nsew")
        self.input_button = customtkinter.CTkButton(self.sidebar_frame2, text="click for input", command=self.input_dialog_event)
        self.input_button.grid(row=0, column=0, padx=20, pady=10)

        # Create welcome view
        #self.welcomeview = SettingsView(self)

    def input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="input here", title="dialog box")
        print(dialog.get_input())

    def submit_button_event(self, event=None):
        input = self.entry.get()
        self.entry.delete(0, 100)
        if input == '':
            None
        else:
            print(input)

    def hide_all_body(self):
        '''
        Hides all main body widgets. Used to switch between widgets. Button click should call this method
        then call method to make desired widget visible.

        Any newly created body widgets should be added here so they can be hidden when needed.
        '''
        self.announcement_box.grid_forget()

    def hide_test(self):
        self.welcomeview.destroy()

    def welcome_view_active(self):
        if  self.active_widget is None or not self.welcome_view:
            self.welcome_view = WelcomeView(self)
            self.active_widget = self.welcome_view
        else:
            self.welcome_view.destroy

    def settings_view_toggle(self):
        if  self.active_widget is None:
            print("Setting active widget")
            self.settings_view = SettingsView(self)
            self.active_widget = self.settings_view
        elif self.active_widget == self.settings_view:
            self.active_widget.destroy()
            self.active_widget = None
        else:
            self.active_widget.destroy()
            self.settings_view = SettingsView(self)
            self.active_widget = self.settings_view

    def view_toggle(self, view, parent):
        if self.active_widget is None:
            self.view = view(parent)
            self.active_widget = self.view
        elif self.active_widget == self.view:
            self.active_widget.destroy()
            self.active_widget = None
        else:
            self.active_widget.destroy()
            self.view = view(parent)
            self.active_widget = self.view

    def clear_view(self):
        if self.active_widget is not None:
            print(f"destroying {self.active_widget}")
            self.active_widget.destroy()
            self.active_widget = None



        # if  self.active_widget is None:
        #     self.settings_view = SettingsView(self)
        #     self.active_widget = self.settings_view
        # elif self.active_widget is not self.settings_view:
        #     self.active_widget.destroy
        #     self.active_widget = None
        # else:
        #     self.settings_view.destroy
        #     self.active_widget = None
            
def view_toggle_decorator(view_cls):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Destroy current view if it exists
            if hasattr(self, "_current_widget") and self._current_widget is not None:
                self._current_widget.destroy()

            # Create new view
            new_view = view_cls(self, *args, **kwargs)

            # Set current view and widget
            self._current_view = view_cls
            self._current_widget = new_view

            return func(self, *args, **kwargs)
        return wrapper
    return decorator



class WelcomeView(customtkinter.CTk):
    '''
    This is the welcome widget that is visible upon program startup. It Displays instructions
    or various info.

    WelcomeView objects must be instatiated with a parent argument. The parent is which app widget will
    contain the welcome view widget. To place the WelcomeView widget in the default window simply
    pass "self" as the argument.
    '''
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.announcement_box = tk.Text(parent, wrap="word", width=250)
        self.announcement_box.insert("1.0",
                                     '''Welcome to Squarespace Companion!

If you have not already, please configure your settings
under the settings option in the main menu.''')
        self.announcement_box.config(state="disabled", font="Helvetica", bg="#2b2d30")
        self.announcement_box.tag_configure("custom tag", foreground="white")
        self.announcement_box.tag_add("custom tag", 0.0, "end")
        self.announcement_box.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def destroy(self):
        self.announcement_box.destroy()

class SettingsView:
    def __init__(self, parent="self", *args, **kwargs):
        self.parent = parent
        self.settings_tabview = customtkinter.CTkTabview(parent, width=250)
        self.settings_tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.settings_tabview.add("Set API Key")
        self.settings_tabview.add("Select Inventory File")
        self.settings_tabview.add("Column Header Configuration")

    # def settings_view_active(self, parent):
    #     settings_view = SettingsView(parent)
    #     return settings_view

    def destroy(self):
        self.settings_tabview.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()