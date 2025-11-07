from .backend import ImGuiBackend

from .utilities.PlaceManager import PlaceManager
from .utilities.PlacePanel import PlacePanel
from .utilities.ExplorerManager import ExplorerManager
from .utilities.SceneGraphExplorer import SceneGraphExplorer
from .utilities.TimeSliderManager import TimeSliderManager
from .utilities.IntervalTimeSlider import IntervalTimeSlider

__all__ = ['init',
           'ImGuiBackend',
           "PlacePanel",
           'PlaceManager',
           'ExplorerManager',
           'SceneGraphExplorer',
           'TimeSliderManager',
           'IntervalTimeSlider',
          ]

def init(window = None, parent = None,
         style = 'dark', wantPlaceManager = True,
         wantExplorerManager = True, wantTimeSliderManager = True):
    try:
        base.imgui
    except AttributeError:
        base.imgui = ImGuiBackend(window, parent, style)

        if wantPlaceManager:
            base.placeManager = PlaceManager()
        if wantExplorerManager:
            base.explorerManager = ExplorerManager()
        if wantTimeSliderManager:
            base.timeSliderManager = TimeSliderManager()
