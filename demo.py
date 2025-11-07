from panda3d.core import loadPrcFileData, WindowProperties, Point3
from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence

import p3dimgui

from imgui_bundle import imgui, imgui_ctx

import sys

class DemoBase(ShowBase):
    def __init__(self):
        # Start at a 720p resolution
        loadPrcFileData('', 'win-size 1280 720')

        ShowBase.__init__(self)

        # Enable debug output
        loadPrcFileData('', 'notify-level-imgui debug')

        # Disable the camera trackball controls.
        self.disableMouse()

        # Install Dear ImGui
        p3dimgui.init()

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")

        # Reparent the model to render.
        self.scene.reparentTo(self.render)

        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Load and transform the panda actor.
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})

        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)

        # Loop its animation.
        self.pandaActor.loop("walk")

        # Create the four lerp intervals needed for the panda to
        # walk back and forth.
        posInterval1 = self.pandaActor.posInterval(13,
                                                   Point3(0, -10, 0),
                                                   startPos=Point3(0, 10, 0))

        posInterval2 = self.pandaActor.posInterval(13,
                                                   Point3(0, 10, 0),
                                                   startPos=Point3(0, -10, 0))

        hprInterval1 = self.pandaActor.hprInterval(3,
                                                   Point3(180, 0, 0),
                                                   startHpr=Point3(0, 0, 0))

        hprInterval2 = self.pandaActor.hprInterval(3,
                                                   Point3(0, 0, 0),
                                                   startHpr=Point3(180, 0, 0))

        # Create and play the sequence that coordinates the intervals.
        self.pandaPace = Sequence(posInterval1, hprInterval1,
                                  posInterval2, hprInterval2,
                                  name="pandaPace")
        self.pandaPace.loop()

        # This assumes that the TimeSliderManager has replaced the .popupControls() method.
        self.pandaPace.popupControls()

        # This assumes that the ExplorerManager has replaced the .explore() method.
        self.render.explore()

        self.camera.setPosHpr((11.80, -24.85, 17.20), (30.00, -29.55, 0.00))

        # This assumes that the PlaceManager has replaced the .place() method.
        self.camera.place()

        self.showDemoWindow = True

        self.accept('imgui-new-frame', self.__newFrame)
        self.accept('`', self.__toggleImgui)

    def __toggleImgui(self):
        if not self.imgui.isKeyboardCaptured():
            self.imgui.toggle()

    def __newFrame(self):
        # Dear ImGui commands can be placed here.
        with imgui_ctx.begin_main_menu_bar() as mainMenu:
            if mainMenu:

                with imgui_ctx.begin_menu("Demo") as demoMenu:
                    if demoMenu:

                        clickedExplorer, _ = imgui.menu_item("Show Scene Graph Explorer", "", self.render in self.explorerManager.nodesToExplorers, True)
                        if clickedExplorer:
                            if self.render not in self.explorerManager.nodesToExplorers:
                                self.render.explore()
                            else:
                                self.explorerManager.nodesToExplorers[self.render].active = False

                        clickedPlacer, _ = imgui.menu_item("Show Camera Node Placer", "", self.camera in self.placeManager.nodesToPlacers, True)
                        if clickedPlacer:
                            if self.camera not in self.placeManager.nodesToPlacers:
                                self.camera.place()
                            else:
                                self.placeManager.nodesToPlacers[self.camera].active = False

                        clickedSlider, _ = imgui.menu_item("Show Interval Time Slider", "", self.pandaPace in self.timeSliderManager.intervalToTimeSliders, True)
                        if clickedSlider:
                            if self.pandaPace not in self.timeSliderManager.intervalToTimeSliders:
                                self.pandaPace.popupControls()
                            else:
                                self.timeSliderManager.intervalToTimeSliders[self.pandaPace].active = False

                        clickedDemo, _ = imgui.menu_item("Show Dear ImGui Demo Window", "", self.showDemoWindow, True)
                        if clickedDemo:
                            self.showDemoWindow = not self.showDemoWindow

                        clickedQuit, _ = imgui.menu_item("Quit", "Cmd+Q" if sys.platform == 'darwin' else "Alt+F4", False, True)
                        if clickedQuit:
                            self.userExit()

                # Display FPS after the menu on the menu bar, cause why not.
                imgui.set_cursor_pos_x(imgui.get_window_size().x - 140)
                imgui.text("%.2f FPS (%.2f ms)" % (imgui.get_io().framerate, 1000.0 / imgui.get_io().framerate))

        if self.showDemoWindow:
            imgui.show_demo_window()

demo = DemoBase()
demo.run()
