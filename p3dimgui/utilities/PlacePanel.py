from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath

from imgui_bundle import imgui, imgui_ctx

class PlacePanel(DirectObject):
    def __init__(self, nodePath: NodePath, active=True):
        DirectObject.__init__(self)

        self.nodePath: NodePath = nodePath

        self.active = active

        self.scaleUniform = True
        scale = self.nodePath.getScale()
        if scale[0] != scale[1] or \
            scale[0] != scale[2] or \
            scale[1] != scale[2]:
                self.scaleUniform = False

        self.accept('imgui-new-frame', self.__draw)

    def __del__(self):
        self.ignoreAll()

    def __draw(self):
        if not self.active:
            return

        if not self.nodePath:
            # Must've gotten deleted.
            self.active = False
            return

        pos = self.nodePath.getPos()
        hpr = self.nodePath.getHpr()
        scale = self.nodePath.getScale()

        # This is done to silence the "has no color set" warnings.
        color = (1.0, 1.0, 1.0, 1.0)
        if self.nodePath.hasColor():
            color = self.nodePath.getColor()

        colorScale = (1.0, 1.0, 1.0, 1.0)
        if self.nodePath.hasColorScale():
            colorScale = self.nodePath.getColorScale()

        with imgui_ctx.begin(f"Node Placer \"{self.nodePath.getName()}\"", True) as (_, windowOpen):
            if not windowOpen:
                # Close has been clicked.
                self.active = False
                return

            with imgui_ctx.begin_group():
                imgui.text("Position")

                imgui.push_item_width(50)
                xChanged, xValue = imgui.drag_float("X", pos[0], v_speed=0.05, format='%.3f')
                yChanged, yValue = imgui.drag_float("Y", pos[1], v_speed=0.05, format='%.3f')
                zChanged, zValue = imgui.drag_float("Z", pos[2], v_speed=0.05, format='%.3f')
                imgui.pop_item_width()

                if xChanged:
                    self.nodePath.setX(xValue)
                elif yChanged:
                    self.nodePath.setY(yValue)
                elif zChanged:
                    self.nodePath.setZ(zValue)

            imgui.same_line(spacing=20)

            with imgui_ctx.begin_group():
                imgui.text("Orientation")

                imgui.push_item_width(50)
                hChanged, hValue = imgui.drag_float("H", hpr[0], v_speed=0.05, format='%.3f')
                pChanged, pValue = imgui.drag_float("P", hpr[1], v_speed=0.05, format='%.3f')
                rChanged, rValue = imgui.drag_float("R", hpr[2], v_speed=0.05, format='%.3f')
                imgui.pop_item_width()

                if hChanged:
                    self.nodePath.setH(hValue)
                elif pChanged:
                    self.nodePath.setP(pValue)
                elif rChanged:
                    self.nodePath.setR(rValue)

            imgui.same_line(spacing=20)

            with imgui_ctx.begin_group():
                imgui.text("Scaling")

                imgui.push_item_width(50)
                sxChanged, sxValue = imgui.drag_float("X##scale", scale[0], v_speed=0.05, format='%.3f')
                syChanged, syValue = imgui.drag_float("Y##scale", scale[1], v_speed=0.05, format='%.3f')
                szChanged, szValue = imgui.drag_float("Z##scale", scale[2], v_speed=0.05, format='%.3f')
                uniformBoxClicked, _ = imgui.checkbox("Uniform Scaling", self.scaleUniform)
                imgui.pop_item_width()

                if uniformBoxClicked:
                    self.scaleUniform = not self.scaleUniform

                if sxChanged:
                    if self.scaleUniform:
                        self.nodePath.setScale(sxValue)
                    else:
                        self.nodePath.setSx(sxValue)
                elif syChanged:
                    if self.scaleUniform:
                        self.nodePath.setScale(syValue)
                    else:
                        self.nodePath.setSy(syValue)
                elif szChanged:
                    if self.scaleUniform:
                        self.nodePath.setScale(szValue)
                    else:
                        self.nodePath.setSz(szValue)

            # Colors
            colorChanged, newColor = imgui.color_edit4('Color', color, imgui.ColorEditFlags_.float.value)
            if colorChanged:
                self.nodePath.setColor(*newColor)
            colorScaleChanged, newColorScale = imgui.color_edit4('Color Scale', colorScale, imgui.ColorEditFlags_.float.value)
            if colorScaleChanged:
                self.nodePath.setColorScale(*newColorScale)

            imgui.separator()

            # Copy buttons
            if imgui.button("Copy setPosHprScale()"):
                imgui.open_popup("posHprScaleMenu")

            with imgui_ctx.begin_popup("posHprScaleMenu") as posHprScaleMenuOpened:
                if posHprScaleMenuOpened:
                    for string in (
                        f".setPosHpr(({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f}), ({hpr[0]:.2f}, {hpr[1]:.2f}, {hpr[2]:.2f}))",
                        f".setPosHprScale(({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f}), ({hpr[0]:.2f}, {hpr[1]:.2f}, {hpr[2]:.2f}), ({scale[0]:.2f}, {scale[1]:.2f}, {scale[2]:.2f}))",
                        "",
                        f".setPos(({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f}))",
                        f".setHpr(({hpr[0]:.2f}, {hpr[1]:.2f}, {hpr[2]:.2f}))",
                        f".setScale(({scale[0]:.2f}, {scale[1]:.2f}, {scale[2]:.2f}))",
                        "",
                        f".setX({pos[0]:.2f})",
                        f".setY({pos[1]:.2f})",
                        f".setZ({pos[2]:.2f})",
                        "",
                        f".setH({hpr[0]:.2f})",
                        f".setP({hpr[1]:.2f})",
                        f".setR({hpr[2]:.2f})",
                        "",
                        f".setSx({scale[0]:.2f})",
                        f".setSy({scale[1]:.2f})",
                        f".setSz({scale[2]:.2f})",
                        "",
                        f".posHprInterval(1, ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f}), ({hpr[0]:.2f}, {hpr[1]:.2f}, {hpr[2]:.2f}), blendType='easeInOut'),",
                        f".scaleInterval(1, ({scale[0]:.2f}, {scale[1]:.2f}, {scale[2]:.2f}), blendType='easeInOut'),",
                        f".posHprScaleInterval(1, ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f}), ({hpr[0]:.2f}, {hpr[1]:.2f}, {hpr[2]:.2f}), ({scale[0]:.2f}, {scale[1]:.2f}, {scale[2]:.2f}), blendType='easeInOut'),",
                        "",
                        f"Func(node.setScale, ({scale[0]:.2f}, {scale[1]:.2f}, {scale[2]:.2f})),",
                        f"Func(node.setPosHpr, ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f}), ({hpr[0]:.2f}, {hpr[1]:.2f}, {hpr[2]:.2f})),",
                        f"Func(node.setPosHprScale, ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f}), ({hpr[0]:.2f}, {hpr[1]:.2f}, {hpr[2]:.2f}), ({scale[0]:.2f}, {scale[1]:.2f}, {scale[2]:.2f})),",
                    ):
                        if not string:
                            imgui.separator()
                            continue
                        clicked, _ = imgui.menu_item(string, "", False)
                        if clicked:
                            imgui.set_clipboard_text(string)
                            imgui.close_current_popup()

            imgui.same_line(spacing=20)

            if imgui.button("Copy setColor()"):
                imgui.open_popup("colorMenu")

            with imgui_ctx.begin_popup("colorMenu") as colorMenuOpened:
                if colorMenuOpened:
                    for string in (
                        f".setColor(({colorScale[0]:.2f}, {color[1]:.2f}, {color[2]:.2f}))",
                        "",
                        f".colorInterval(1, ({color[0]:.2f}, {color[1]:.2f}, {color[2]:.2f}), blendType='easeInOut'),",
                        "",
                        f"Func(node.setColor, ({color[0]:.2f}, {color[1]:.2f}, {color[2]:.2f})),"
                    ):
                        if not string:
                            imgui.separator()
                            continue
                        clicked, _ = imgui.menu_item(string, "", False)
                        if clicked:
                            imgui.set_clipboard_text(string)
                            imgui.close_current_popup()

            imgui.same_line(spacing=20)

            if imgui.button("Copy setColorScale()"):
                imgui.open_popup("colorScaleMenu")

            with imgui_ctx.begin_popup("colorScaleMenu") as colorScaleMenuOpened:
                if colorScaleMenuOpened:
                    for string in (
                        f".setColorScale(({colorScale[0]:.2f}, {colorScale[1]:.2f}, {colorScale[2]:.2f}))",
                        "",
                        f".colorScaleInterval(1, ({colorScale[0]:.2f}, {colorScale[1]:.2f}, {colorScale[2]:.2f}), blendType='easeInOut'),",
                        "",
                        f"Func(node.setColorScale, ({colorScale[0]:.2f}, {colorScale[1]:.2f}, {colorScale[2]:.2f})),"
                    ):
                        if not string:
                            imgui.separator()
                            continue
                        clicked, _ = imgui.menu_item(string, "", False)
                        if clicked:
                            imgui.set_clipboard_text(string)
                            imgui.close_current_popup()


