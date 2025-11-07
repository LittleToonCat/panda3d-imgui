from imgui_bundle import imgui, imgui_ctx

from direct.showbase.DirectObject import DirectObject

class IntervalTimeSlider(DirectObject):
    def __init__(self, interval, active=True):
        DirectObject.__init__(self)
        self.interval = interval

        self.active = active

        self.__firstDraw = True
        self.accept('imgui-new-frame', self.__draw)

    def __draw(self):
        if not self.active:
            return
        curDuration = self.interval.getT()
        maxDuration = self.interval.getDuration()

        if self.__firstDraw:
            # imgui.set_next_window_content_size((784.0, 77.0))
            imgui.set_next_window_size((745,76))
            self.__firstDraw = False
        with imgui_ctx.begin(f"Time Slider \"{self.interval.getName()}\"", True,
                             imgui.WindowFlags_.no_resize.value | imgui.WindowFlags_.no_scrollbar.value | imgui.WindowFlags_.no_scroll_with_mouse.value) as (_, windowOpen):
            imgui.push_item_width(732)
            changed, value = imgui.slider_float(
                "##slider", curDuration,
                v_min=0.0, v_max=self.interval.getDuration(),
                format=f"{self.__calculateTimeFormat(curDuration)}/{self.__calculateTimeFormat(maxDuration)}",
                flags=imgui.SliderFlags_.no_input.value
            )
            imgui.pop_item_width()

            if not windowOpen:
                self.active = False
            if changed:
                self.interval.setT(value)

            imgui.spacing()
            imgui.same_line(spacing=312)
            if imgui.button("<<"):
                self.interval.setT(0)
                self.interval.pause()

            imgui.same_line()

            if imgui.button("Pause" if self.interval.isPlaying() else "Play"):
                if self.interval.isPlaying():
                    self.interval.pause()
                else:
                    self.interval.resume()

            imgui.same_line()

            if imgui.button(">>"):
                self.interval.setT(self.interval.getDuration())
                self.interval.pause()


    def __calculateTimeFormat(self, duration):
        if duration >= 60:
            self.currentTime = "00:00"
            totalSeconds = int(duration) % 60
            totalMinutes = int((duration - totalSeconds) / 60)

            if totalMinutes < 10:
                totalMinutes = "%s%s" % (0, totalMinutes)
            if totalSeconds < 10:
                totalSeconds = "%s%s" % (0, totalSeconds)

            return "%s:%s" % (totalMinutes, totalSeconds)
        else:
            if duration < 10:
                return "00:0%s" % (int(duration))
            else:
                return "00:%s" % (int(duration))
