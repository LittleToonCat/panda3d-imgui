from panda3d.core import (
    ButtonHandle,
    ButtonRegistry,
    ColorAttrib,
    ColorBlendAttrib,
    CullFaceAttrib,
    DepthTestAttrib,
    Geom,
    GeomNode,
    GeomTriangles,
    GeomVertexData,
    GeomVertexArrayFormat,
    GeomVertexFormat,
    InternalName,
    KeyboardButton,
    MouseButton,
    NodePath,
    RenderState,
    SamplerState,
    Shader,
    ScissorAttrib,
    Texture,
    TextureAttrib
)

from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject

try:
    from shaders import *
except ModuleNotFoundError:
    from .shaders import *

from imgui_bundle import imgui
import ctypes

import pyperclip
import sys

__all__ = ['ImGuiBackend', 'ImGuiStyles']

KEYBOARD_BUTTON_TO_IMGUI_KEY = {
    # Special keys
    KeyboardButton.tab(): imgui.Key.tab.value,
    KeyboardButton.left(): imgui.Key.left_arrow.value,
    KeyboardButton.right(): imgui.Key.right_arrow.value,
    KeyboardButton.up(): imgui.Key.up_arrow.value,
    KeyboardButton.down(): imgui.Key.down_arrow.value,
    KeyboardButton.enter(): imgui.Key.enter.value,
    KeyboardButton.escape(): imgui.Key.escape.value,
    KeyboardButton.backspace(): imgui.Key.backspace.value,
    KeyboardButton.space(): imgui.Key.space.value,
    KeyboardButton.lshift(): imgui.Key.left_shift.value,
    KeyboardButton.rshift(): imgui.Key.right_shift.value,
    KeyboardButton.shift(): imgui.Key.mod_shift.value,
    KeyboardButton.control(): imgui.Key.mod_ctrl.value,
    KeyboardButton.lcontrol(): imgui.Key.left_ctrl.value,
    KeyboardButton.rcontrol(): imgui.Key.right_ctrl.value,
    KeyboardButton.alt(): imgui.Key.mod_alt.value,
    KeyboardButton.lalt(): imgui.Key.left_alt.value,
    KeyboardButton.ralt(): imgui.Key.right_alt.value,
    KeyboardButton._del(): imgui.Key.delete.value,
    KeyboardButton.home(): imgui.Key.home.value,
    KeyboardButton.end(): imgui.Key.end.value,
    KeyboardButton.pageUp(): imgui.Key.page_up.value,
    KeyboardButton.pageDown(): imgui.Key.page_down.value,
    KeyboardButton.insert(): imgui.Key.insert.value,
    KeyboardButton.capsLock(): imgui.Key.caps_lock.value,
    KeyboardButton.numLock(): imgui.Key.num_lock.value,
    KeyboardButton.scrollLock(): imgui.Key.scroll_lock.value,
    KeyboardButton.menu(): imgui.Key.menu.value,
    KeyboardButton.lmeta(): imgui.Key.left_super.value,
    KeyboardButton.rmeta(): imgui.Key.right_super.value,
    KeyboardButton.meta(): imgui.Key.mod_super.value,

    # Function keys (F1 to F16)
    KeyboardButton.f1(): imgui.Key.f1.value,
    KeyboardButton.f2(): imgui.Key.f2.value,
    KeyboardButton.f3(): imgui.Key.f3.value,
    KeyboardButton.f4(): imgui.Key.f4.value,
    KeyboardButton.f5(): imgui.Key.f5.value,
    KeyboardButton.f6(): imgui.Key.f6.value,
    KeyboardButton.f7(): imgui.Key.f7.value,
    KeyboardButton.f8(): imgui.Key.f8.value,
    KeyboardButton.f9(): imgui.Key.f9.value,
    KeyboardButton.f10(): imgui.Key.f10.value,
    KeyboardButton.f11(): imgui.Key.f11.value,
    KeyboardButton.f12(): imgui.Key.f12.value,
    KeyboardButton.f13(): imgui.Key.f13.value,
    KeyboardButton.f14(): imgui.Key.f14.value,
    KeyboardButton.f15(): imgui.Key.f15.value,
    KeyboardButton.f16(): imgui.Key.f16.value,

    # Numeric keys (0-9) on the main keyboard
    KeyboardButton.asciiKey("0"): imgui.Key._0.value,
    KeyboardButton.asciiKey("1"): imgui.Key._1.value,
    KeyboardButton.asciiKey("2"): imgui.Key._2.value,
    KeyboardButton.asciiKey("3"): imgui.Key._3.value,
    KeyboardButton.asciiKey("4"): imgui.Key._4.value,
    KeyboardButton.asciiKey("5"): imgui.Key._5.value,
    KeyboardButton.asciiKey("6"): imgui.Key._6.value,
    KeyboardButton.asciiKey("7"): imgui.Key._7.value,
    KeyboardButton.asciiKey("8"): imgui.Key._8.value,
    KeyboardButton.asciiKey("9"): imgui.Key._9.value,

    # Alphabetic keys
    KeyboardButton.asciiKey("a"): imgui.Key.a.value,
    KeyboardButton.asciiKey("b"): imgui.Key.b.value,
    KeyboardButton.asciiKey("c"): imgui.Key.c.value,
    KeyboardButton.asciiKey("d"): imgui.Key.d.value,
    KeyboardButton.asciiKey("e"): imgui.Key.e.value,
    KeyboardButton.asciiKey("f"): imgui.Key.f.value,
    KeyboardButton.asciiKey("g"): imgui.Key.g.value,
    KeyboardButton.asciiKey("h"): imgui.Key.h.value,
    KeyboardButton.asciiKey("i"): imgui.Key.i.value,
    KeyboardButton.asciiKey("j"): imgui.Key.j.value,
    KeyboardButton.asciiKey("k"): imgui.Key.k.value,
    KeyboardButton.asciiKey("l"): imgui.Key.l.value,
    KeyboardButton.asciiKey("m"): imgui.Key.m.value,
    KeyboardButton.asciiKey("n"): imgui.Key.n.value,
    KeyboardButton.asciiKey("o"): imgui.Key.o.value,
    KeyboardButton.asciiKey("p"): imgui.Key.p.value,
    KeyboardButton.asciiKey("q"): imgui.Key.q.value,
    KeyboardButton.asciiKey("r"): imgui.Key.r.value,
    KeyboardButton.asciiKey("s"): imgui.Key.s.value,
    KeyboardButton.asciiKey("t"): imgui.Key.t.value,
    KeyboardButton.asciiKey("u"): imgui.Key.u.value,
    KeyboardButton.asciiKey("v"): imgui.Key.v.value,
    KeyboardButton.asciiKey("w"): imgui.Key.w.value,
    KeyboardButton.asciiKey("x"): imgui.Key.x.value,
    KeyboardButton.asciiKey("y"): imgui.Key.y.value,
    KeyboardButton.asciiKey("z"): imgui.Key.z.value,

    # Punctuation keys
    KeyboardButton.asciiKey("!"): imgui.Key._1.value,
    KeyboardButton.asciiKey("@"): imgui.Key._2.value,
    KeyboardButton.asciiKey("#"): imgui.Key._3.value,
    KeyboardButton.asciiKey("$"): imgui.Key._4.value,
    KeyboardButton.asciiKey("%"): imgui.Key._5.value,
    KeyboardButton.asciiKey("^"): imgui.Key._6.value,
    KeyboardButton.asciiKey("&"): imgui.Key._7.value,
    KeyboardButton.asciiKey("*"): imgui.Key._8.value,
    KeyboardButton.asciiKey("("): imgui.Key._9.value,
    KeyboardButton.asciiKey(")"): imgui.Key._0.value,
    KeyboardButton.asciiKey("-"): imgui.Key.minus.value,
    KeyboardButton.asciiKey("="): imgui.Key.equal.value,
    KeyboardButton.asciiKey("["): imgui.Key.left_bracket.value,
    KeyboardButton.asciiKey("]"): imgui.Key.right_bracket.value,
    KeyboardButton.asciiKey("\\"): imgui.Key.backslash.value,
    KeyboardButton.asciiKey(";"): imgui.Key.semicolon.value,
    KeyboardButton.asciiKey("'"): imgui.Key.apostrophe.value,
    KeyboardButton.asciiKey(","): imgui.Key.comma.value,
    KeyboardButton.asciiKey("."): imgui.Key.period.value,
    KeyboardButton.asciiKey("/"): imgui.Key.slash.value,

    # Special characters
    KeyboardButton.asciiKey("`"): imgui.Key.grave_accent.value,
    KeyboardButton.asciiKey("~"): imgui.Key.grave_accent.value,
    KeyboardButton.asciiKey("_"): imgui.Key.minus.value,
    KeyboardButton.asciiKey("+"): imgui.Key.equal.value,
    KeyboardButton.asciiKey("<"): imgui.Key.comma.value,
    KeyboardButton.asciiKey(">"): imgui.Key.period.value,
    KeyboardButton.asciiKey("?"): imgui.Key.slash.value,

    # Additional modifier keys
    KeyboardButton.printScreen(): imgui.Key.print_screen.value,
    KeyboardButton.pause(): imgui.Key.pause.value,
}

class GeomList:
    def __init__(self, vdata: GeomVertexData):
        self.vdata: GeomVertexData = vdata  # vertex data shared among the below GeomNodes
        self.nodepaths: list[NodePath] = []

class ImGuiBackend(DirectObject):
    """
    The main Dear ImGui backend code for Panda3D.
    (Based on https://github.com/bluekyu/panda3d_imgui; ported to
    Python using imgui-bundle and updated to support Dear ImGui version 1.92.3)
    """

    def __init__(self, window = None, parent = None, style = 'dark'):
        DirectObject.__init__(self)
        self.notify = DirectNotifyGlobal.directNotify.newCategory("imgui")
        if not window:
            window = base.win
        if not parent:
            parent = base.pixel2d

        self.window = window
        self.root = parent.attachNewNode('imgui-root', 1000)
        self.context = imgui.create_context()
        self.io = imgui.get_io()

        # Add backend flag for rendering textures
        self.io.backend_flags |= imgui.BackendFlags_.renderer_has_textures.value

        self.vformat = None
        self.textures: dict[int, Texture] = {}
        self.geomData: list[GeomList] = []

        self.__setupStyle(style)
        self.__setupGeom()
        self.__setupShader()
        self.__setupFront()
        self.__setupEvent()
        self.__windowEvent()
        self.__setupButton()
        self.__setupRender()

        # Set Clipboard functions
        imgui.get_platform_io().platform_set_clipboard_text_fn = self.__setClipboardText
        imgui.get_platform_io().platform_get_clipboard_text_fn = self.__getClipboardText

    def toggle(self):
        if self.root.isHidden():
            self.root.show()
        else:
            self.root.hide()

    def hide(self):
        self.root.hide()

    def show(self):
        self.root.show()

    def isMouseCaptured(self) -> bool:
        # This returns True if the mouse is over
        # a Imgui window or any other reason.
        return self.io.want_capture_mouse

    def isKeyboardCaptured(self) -> bool:
        # This returns True when a Imgui text
        # input widget is focused or any other reason.
        return self.io.want_capture_keyboard

    def __setupStyle(self, style):
        match style:
            case 'dark':
                imgui.style_colors_dark()
            case 'classic':
                imgui.style_colors_classic()
            case 'light':
                imgui.style_colors_light()
            case _:
                self.notify.warning(f"Unknown style: \"{style}\"")

    def __onButton(self, keyName: str, down: bool):
        # Panda3D adds the prefix of the modifier keys to the key name
        # if they are held down, so we have to strip them out.
        if keyName.startswith(('control-', 'alt-', 'shift-', 'shift-control-', 'shift-alt-', 'shift-control-alt-',
                               'meta-', 'control-meta-', 'alt-meta-', 'control-alt-meta-', 'shift-meta-',
                               'shift-control-meta', 'shift-alt-meta-', 'shift-control-alt-meta-')):
            keyName = keyName.split('-')[-1]
            if keyName == '':
                # must be minus.
                keyName = '-'

        button = ButtonRegistry.ptr().getButton(keyName)
        if button == ButtonHandle.none():
            return
        if MouseButton.isMouseButton(button):
            if button == MouseButton.one():
                self.io.add_mouse_button_event(0, down)
            elif button == MouseButton.three():
                # NOTE: In Panda3D, MouseButton.three() is the right mouse button
                # while MouseButton.two() is the middle (scroll wheel) button
                self.io.add_mouse_button_event(1, down)
            elif button == MouseButton.two():
                self.io.add_mouse_button_event(2, down)
            elif button == MouseButton.four():
                self.io.add_mouse_button_event(3, down)
            elif button == MouseButton.five():
                self.io.add_mouse_button_event(4, down)
            elif button == MouseButton.wheelUp() and down:
                self.io.add_mouse_wheel_event(0, .5)
            elif button == MouseButton.wheelDown() and down:
                self.io.add_mouse_wheel_event(0, -.5)
            elif button == MouseButton.wheelLeft() and down:
                self.io.add_mouse_wheel_event(.5, 0)
            elif button == MouseButton.wheelRight() and down:
                self.io.add_mouse_wheel_event(-.5, 0)
        else:
            imguiKey = KEYBOARD_BUTTON_TO_IMGUI_KEY.get(button, imgui.Key.none.value)
            self.io.add_key_event(imguiKey, down)

    def __onKeystroke(self, keyName):
        # NOTE: Panda3D for some reason doesn't recognize if
        # the caps lock is on for macOS. You would have to
        # hold down shift to input capital letters.
        # Windows/Linux handles this just fine.
        button = ButtonRegistry.ptr().getButton(keyName)
        if keyName == ' ':
            # There is no space button on the ButtonRegistry.
            button = KeyboardButton.space()
        if button.hasAsciiEquivalent():
            self.io.add_input_character(ord(button.getAsciiEquivalent()))

    def __setupGeom(self):
        self.notify.debug("__setupGeom")
        arrayFormat = GeomVertexArrayFormat(
            InternalName.getVertex(), 4, Geom.NT_stdfloat, Geom.C_point,
            InternalName.getColor(), 1, Geom.NT_packed_dabc, Geom.C_color
        )

        self.vformat = GeomVertexFormat.registerFormat(GeomVertexFormat(arrayFormat))

        self.root.setState(RenderState.make(
            ColorAttrib.makeVertex(),
            ColorBlendAttrib.make(ColorBlendAttrib.M_add, ColorBlendAttrib.O_incoming_alpha, ColorBlendAttrib.O_one_minus_incoming_alpha),
            DepthTestAttrib.make(DepthTestAttrib.M_none),
            CullFaceAttrib.make(CullFaceAttrib.M_cull_none)
        ))

    def __setupShader(self):
        self.notify.debug("__setupShader")
        shader = Shader.make(
            Shader.SL_GLSL,
            VERT_SHADER,
            FRAG_SHADER,
        )

        self.root.setShader(shader)

    def __setupFront(self):
        self.notify.debug("__setupFront")
        self.io.fonts.add_font_default()

    def __setupEvent(self):
        self.notify.debug("__setupEvent")
        self.accept("window-event", self.__windowEvent)

    def __windowEvent(self, _ = None):
        if self.window:
            self.io.display_size = (self.window.getXSize(), self.window.getYSize())

    def __setupButton(self):
        self.notify.debug("__setupButton")
        # FIXME: THe event names gets replaced when base.oobe() is called.
        base.buttonThrowers[0].node().setButtonDownEvent('buttonDown')
        base.buttonThrowers[0].node().setButtonUpEvent('buttonUp')
        base.buttonThrowers[0].node().setKeystrokeEvent('keystroke')

        def __buttonDown(keyName):
            self.__onButton(keyName, True)

        def __buttonUp(keyName):
            self.__onButton(keyName, False)

        def __keyStroke(keyName):
            self.__onKeystroke(keyName)

        self.accept('buttonDown', __buttonDown)
        self.accept('buttonUp', __buttonUp)
        self.accept('keystroke', __keyStroke)

    def __setupRender(self):
        self.notify.debug("__setupRender")
        # NOTE: igLoop (frame rendering) has 50 sort.
        base.taskMgr.add(self.__newFrame, "imgui-new-frame", 0)
        base.taskMgr.add(self.__renderFrame, "imgui-render-frame", 40)

    def __newFrame(self, task):
        if self.root.isHidden():
            return task.cont

        self.io.delta_time = base.clock.getDt()
        if self.window:
            mouse = self.window.getPointer(0)
            if mouse.getInWindow():
                if self.io.want_set_mouse_pos:
                    self.window.movePointer(0, self.io.mouse_pos.x, self.io.mouse_pos.y)
                else:
                    self.io.mouse_pos = mouse.getX(), mouse.getY()
            else:
                self.io.mouse_pos = (-imgui.FLT_MAX, -imgui.FLT_MAX)

        imgui.new_frame()
        base.messenger.send("imgui-new-frame")

        return task.cont

    def __renderFrame(self, task):
        if self.root.isHidden():
            return task.cont

        imgui.render()

        fbWidth = self.io.display_size.x * self.io.display_framebuffer_scale.x
        fbHeight = self.io.display_size.y * self.io.display_framebuffer_scale.y

        self.__updateTextures()

        drawData = imgui.get_draw_data()

        for child in self.root.children:
            child.detachNode()

        for i, cmdList in enumerate(drawData.cmd_lists):
            if i > len(self.geomData) - 1:
                self.geomData.append(GeomList(GeomVertexData(f"imgui-vertex-{i}", self.vformat, Geom.UH_stream)))

            geomList = self.geomData[i]
            vertexHandle = geomList.vdata.modifyArrayHandle(0)
            if vertexHandle.getNumRows() < cmdList.vtx_buffer.size():
                vertexHandle.uncleanSetNumRows(cmdList.vtx_buffer.size())
            vertexHandle.setData(ctypes.string_at(cmdList.vtx_buffer.data_address(), cmdList.vtx_buffer.size() * imgui.VERTEX_SIZE))

            indexBuffer = cmdList.idx_buffer.data_address()
            for k, drawCmd, in enumerate(cmdList.cmd_buffer):
                if k > len(geomList.nodepaths) - 1:
                    geomList.nodepaths.append(self.__createGeomnode(geomList.vdata))

                np = geomList.nodepaths[k]
                np.reparentTo(self.root)

                node = np.node()
                indexHandle = node.modifyGeom(0).modifyPrimitive(0).modifyVertices(drawCmd.elem_count).modifyHandle()
                if indexHandle.getNumRows() < drawCmd.elem_count:
                    indexHandle.uncleanSetNumRows(drawCmd.elem_count)

                indexHandle.setData(ctypes.string_at(indexBuffer, drawCmd.elem_count * imgui.INDEX_SIZE))
                indexBuffer += (drawCmd.elem_count * imgui.INDEX_SIZE)

                # FIXME: This works, but it breaks Modal windows as the white
                # covers the window (but still usable) instead of the background.
                # (Not sure if this is to blame or the shader...)
                state = RenderState.make(ScissorAttrib.make(
                    drawCmd.clip_rect.x / fbWidth,
                    drawCmd.clip_rect.z / fbWidth,
                    1 - drawCmd.clip_rect.w / fbHeight,
                    1 - drawCmd.clip_rect.y / fbHeight
                ))

                if drawCmd.tex_ref.get_tex_id():
                    texture = self.textures[drawCmd.tex_ref.get_tex_id()]
                    state = state.addAttrib(TextureAttrib.make(texture))

                node.setGeomState(0, state)

        return task.cont

    def __updateTextures(self):
        for tex in imgui.get_platform_io().textures:
            if tex.status != imgui.ImTextureStatus.ok:
                self.__updateTexture(tex)

    def __updateTexture(self, tex: imgui.ImTextureData):
        def __setPixelsToTexture(texture: Texture):
            # The easiest way to update a Panda texture
            # is to recreate the ram image and rewrite
            # all the pixels.

            # This clears the RamImage if one exists already.
            textureData = texture.makeRamImage()

            pixels = tex.get_pixels_array()
            textureData.setData(pixels.tobytes())

        match tex.status:
            case imgui.ImTextureStatus.want_create:
                self.notify.debug(f"__updateTexture ({tex.unique_id}): create ({tex.width}x{tex.height})")
                assert tex.tex_id == 0
                assert tex.backend_user_data is None
                assert tex.format == imgui.ImTextureFormat.rgba32

                texture = Texture()
                texture.setName(f"imgui-texture-{tex.unique_id}")
                texture.setup2dTexture(tex.width, tex.height, Texture.T_unsigned_byte, Texture.F_rgba32)
                texture.setMinfilter(SamplerState.FT_linear)
                texture.setMagfilter(SamplerState.FT_linear)

                __setPixelsToTexture(texture)

                self.textures[tex.unique_id] = texture

                tex.tex_id = tex.unique_id
                tex.status = imgui.ImTextureStatus.ok
            case imgui.ImTextureStatus.want_updates:
                self.notify.debug(f"__updateTexture ({tex.unique_id}): update ({tex.width}x{tex.height})")

                __setPixelsToTexture(self.textures[tex.tex_id])

                tex.status = imgui.ImTextureStatus.ok
            case imgui.ImTextureStatus.want_destroy:
                texture = self.textures.get(tex.tex_id, None)
                if texture:
                    texture.clear()
                    del texture
                    del self.textures[tex.tex_id]

                tex.tex_id = 0
                tex.status = imgui.ImTextureStatus.destroyed

    @staticmethod
    def __createGeomnode(vdata: GeomVertexData) -> NodePath:
        prim = GeomTriangles(Geom.UH_stream)
        if imgui.INDEX_SIZE == 2:
            prim.setIndexType(Geom.NT_uint16)
        else:
            prim.setIndexType(Geom.NT_uint32)
        prim.closePrimitive()

        geom = Geom(vdata)
        geom.addPrimitive(prim)

        node = GeomNode("imgui-geom")
        node.addGeom(geom, RenderState.makeEmpty())

        return NodePath(node)

    def cleanup(self):
        if self.context:
            imgui.destroy_context()
            self.context = None

    @staticmethod
    def __setClipboardText(_, str: str):
        pyperclip.copy(str)

    @staticmethod
    def __getClipboardText(_):
        return pyperclip.paste()
