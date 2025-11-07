from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath

from p3dimgui.utilities.PlacePanel import PlacePanel

from direct.extensions_native.extension_native_helpers import Dtool_funcToMethod

class PlaceManager(DirectObject):
    def __init__(self):
        DirectObject.__init__(self)

        self.nodesToPlacers: dict[NodePath, PlacePanel] = {}

        # Replace the place() and rgbPanel() extension methods for NodePath
        def place(nodePath):
            self.nodesToPlacers[nodePath] = PlacePanel(nodePath)

        Dtool_funcToMethod(place, NodePath)
        Dtool_funcToMethod(place, NodePath, 'rgbPanel')
        self.accept('imgui-new-frame', self.__checkActive)

    def __checkActive(self):
        for node in list(self.nodesToPlacers.keys()):
            placer = self.nodesToPlacers[node]
            if not placer.active:
                del self.nodesToPlacers[node]

