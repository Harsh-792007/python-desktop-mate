import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

class FloatingGIF:
    def __init__(self, root, gif_path):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "black")

        self.label = tk.Label(root, bg="black")
        self.label.pack()

        self.gif = Image.open(gif_path)
        self.original_frames = [frame.convert("RGBA") for frame in ImageSequence.Iterator(self.gif)]
        self.scale = 1.0
        self.frames = []
        self.load_frames()

        self.frame_index = 0
        self.animate()

        # LEFT click → MOVE
        self.label.bind("<ButtonPress-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)

        # RIGHT click → MENU
        self.label.bind("<Button-3>", self.show_menu)

        # MIDDLE click → RESIZE
        self.resizing = False
        self.label.bind("<ButtonPress-2>", self.start_resize)
        self.label.bind("<B2-Motion>", self.resize)

        # Menu
        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Resize", command=self.enable_resize)
        self.menu.add_separator()
        self.menu.add_command(label="Quit", command=root.destroy)

        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()

    def load_frames(self):
        self.frames.clear()
        for frame in self.original_frames:
            w, h = frame.size
            resized = frame.resize((int(w * self.scale), int(h * self.scale)))
            self.frames.append(ImageTk.PhotoImage(resized))

    def animate(self):
        self.label.config(image=self.frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.root.after(80, self.animate)

    def show_menu(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = self.root.winfo_pointerx() - self.x
        y = self.root.winfo_pointery() - self.y

        w = self.label.winfo_width()
        h = self.label.winfo_height()

        # Keep above taskbar
        x = max(0, min(x, self.screen_w - w))
        y = max(0, min(y, self.screen_h - h - 40))

        self.root.geometry(f"+{x}+{y}")

    def enable_resize(self):
        self.resizing = True

    def start_resize(self, event):
        self.last_y = event.y

    def resize(self, event):
        if not self.resizing:
            return

        delta = event.y - self.last_y
        self.scale += delta * 0.005
        self.scale = max(0.2, min(self.scale, 3.0))

        self.load_frames()
        self.last_y = event.y


if __name__ == "__main__":
    root = tk.Tk()
    FloatingGIF(root, "your_gif.gif")
    root.mainloop()
