# These shaders is in GLSL version 1.20 is because so they can work
# right out of the box in macOS without having to force the OpenGL version
# to 3.2 (gl-version 3 2).

FRAG_SHADER = """
#version 120

varying vec2 texcoord;
varying vec4 color;

uniform sampler2D p3d_Texture0;

void main()
{
    gl_FragColor = color * texture2D(p3d_Texture0, texcoord);
}
"""

VERT_SHADER = """
#version 120

attribute vec4 p3d_Vertex;  // { vec2 pos, vec2 uv }
attribute vec4 p3d_Color;

varying vec2 texcoord;
varying vec4 color;

uniform mat4 p3d_ModelViewProjectionMatrix;

void main()
{
    texcoord = p3d_Vertex.zw;
    color = p3d_Color.bgra;
    gl_Position = p3d_ModelViewProjectionMatrix * vec4(p3d_Vertex.x, 0.0, -p3d_Vertex.y, 1.0);
}
"""

