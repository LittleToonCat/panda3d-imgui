# panda3d-imgui
A [Dear ImGui](https://github.com/ocornut/imgui) backend for Python-based Panda3D projects with built-in utilities (based on DIRECT Tools). 

<img width="1920" height="1080" alt="Screenshot 2025-11-05 at 10 58 18 PM" src="https://github.com/user-attachments/assets/0de21a26-b37a-40a3-9ae9-b07b2a853742" />

This module will allow you to use and create Dear ImGui user interfaces within a Panda3D window, preferbly used to create content creation/debugging tools.
(It uses [Dear ImGui Bundle](https://pthom.github.io/imgui_bundle/) which contains not only the Python bindings for Dear ImGui, but with other goodies as well.

## How to use
You can install the module through pip:
```
pip install panda3d-imgui
```

And you can import this module as `p3dimgui`
```python
import p3dimgui
```

It has a helper method called `init` which you can easlily add in your ShowBase class.  This will create a `ImGuiBackend` object into `base.imgui`
and initialize it, along side the built-in ultilities.

```python
from direct.showbase.ShowBase import ShowBase

from imgui_bundle import imgui

import p3dimgui

class MyApp(ShowBase):
    def  __init__(self):
        ShowBase.__init__(self)

        # Install Dear ImGui
        p3dimgui.init()
```

Once initalized, it will send an event called `imgui-new-frame` every frame.  You can accept this event whenever you want to draw with ImGui:
```python
def draw(self):
   # Show the demo window.
   imgui.show_demo_window()

self.accept('imgui-new-frame', self.draw)

```

Combine all this and you would have something like this, which will start up a new Panda3D window and shows the Dear ImGui demo window.
```python
from direct.showbase.ShowBase import ShowBase

from imgui_bundle import imgui

import p3dimgui

class MyApp(ShowBase):
    def  __init__(self):
        ShowBase.__init__(self)

        # Install Dear ImGui
        p3dimgui.init()

        self.accept('imgui-new-frame', self.draw)

    def draw(self):
        # Show the demo window.
        imgui.show_demo_window()

app = MyApp()
app.run()
```
<img width="800" height="628" alt="image" src="https://github.com/user-attachments/assets/ab233406-c187-4061-bbe3-49420294f524" />

For a more better demo which showcases all the built-in utilities aviliable (like the screenshot at the top), see the [demo.py](https://github.com/LittleToonCat/panda3d-imgui/blob/main/demo.py) file.
