import asyncio
import tkinter
import tkinter.messagebox
import tkinter.ttk
import time


class GuiApp:
    """Main class for GUI"""

    def __init__(self):

        self.root = tkinter.Tk()

        # Build notebook which all GUI widgets will have as root
        self.notebook = tkinter.ttk.Notebook(self.root)

        # Build and add frames to notebook
        self.config_panel = ConfigPanel()

    async def async_update_loop(self, interval=1.0/60):
        """Corroutine which updates tkinter
        By default, interval is the interval between frames for 60fps
        It will wait interval - time taken to render frame
        """

        while True:
            begin_render_time = time.time()
            self.root.update()
            await asyncio.wait(interval - (begin_render_time - time.time()))


class ConfigPanel:
    """Panel for configuration"""

    def __init__(self, meme_directories=[], file_types=[]):

        # Build frame which all GUI widgets for the config panel will have as root
        self.frame = tkinter.Frame()

        # Build meme directories configuration
        self.meme_directories_header = tkinter.Label(self.frame, text="Meme Folders", font=("", 20))
        self.meme_directories = tkinter.Listbox(self.frame)
        self.meme_directories.insert(tkinter.END, meme_directories)


app = GuiApp()
app.root.mainloop()
