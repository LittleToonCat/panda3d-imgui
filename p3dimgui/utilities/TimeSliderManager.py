from direct.showbase.DirectObject import DirectObject
from panda3d.direct import CInterval

from p3dimgui.utilities.IntervalTimeSlider import IntervalTimeSlider

from direct.extensions_native.extension_native_helpers import Dtool_funcToMethod

class TimeSliderManager(DirectObject):
    def __init__(self):
        DirectObject.__init__(self)

        self.intervalToTimeSliders: dict[CInterval, IntervalTimeSlider] = {}

        # Replace the popupControls() extension method for CInterval
        def popupControls(interval):
            self.intervalToTimeSliders[interval] = IntervalTimeSlider(interval)

        Dtool_funcToMethod(popupControls, CInterval)
        Dtool_funcToMethod(popupControls, CInterval, "slider")
        self.accept('imgui-new-frame', self.__checkActive)

    def __checkActive(self):
        for node in list(self.intervalToTimeSliders.keys()):
            placer = self.intervalToTimeSliders[node]
            if not placer.active:
                del self.intervalToTimeSliders[node]
