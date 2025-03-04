from __future__ import annotations

import numpy as np
from OpenGL import GL as gl
from pixutils.fpscounter import FPSCounter


class ESMatrix:
    def __init__(self):
        self.m = np.identity(4, dtype=np.float32)

    def load_identity(self):
        self.m = np.identity(4, dtype=np.float32)

    def translate(self, tx, ty, tz):
        translation = np.identity(4, dtype=np.float32)
        translation[3, 0] = tx
        translation[3, 1] = ty
        translation[3, 2] = tz
        self.m = translation @ self.m

    def rotate(self, angle, x, y, z):
        angle_rad = angle * np.pi / 180.0
        sin_angle = np.sin(angle_rad)
        cos_angle = np.cos(angle_rad)

        # Normalize rotation axis
        axis = np.array([x, y, z], dtype=np.float32)
        mag = np.linalg.norm(axis)

        if mag > 0.0:
            axis /= mag
            x, y, z = axis

            rot_mat = np.identity(4, dtype=np.float32)
            one_minus_cos = 1.0 - cos_angle

            # Compute common terms once
            xx, yy, zz = x * x, y * y, z * z
            xy, yz, zx = x * y, y * z, z * x
            xs, ys, zs = x * sin_angle, y * sin_angle, z * sin_angle

            # First row
            rot_mat[0, 0] = one_minus_cos * xx + cos_angle
            rot_mat[0, 1] = one_minus_cos * xy - zs
            rot_mat[0, 2] = one_minus_cos * zx + ys

            # Second row
            rot_mat[1, 0] = one_minus_cos * xy + zs
            rot_mat[1, 1] = one_minus_cos * yy + cos_angle
            rot_mat[1, 2] = one_minus_cos * yz - xs

            # Third row
            rot_mat[2, 0] = one_minus_cos * zx - ys
            rot_mat[2, 1] = one_minus_cos * yz + xs
            rot_mat[2, 2] = one_minus_cos * zz + cos_angle

            self.m = rot_mat @ self.m

    def frustum(self, left, right, bottom, top, near_z, far_z):
        delta_x, delta_y, delta_z = right - left, top - bottom, far_z - near_z

        if near_z <= 0.0 or far_z <= 0.0 or delta_x <= 0.0 or delta_y <= 0.0 or delta_z <= 0.0:
            return

        frust = np.zeros((4, 4), dtype=np.float32)

        frust[0, 0] = 2.0 * near_z / delta_x
        frust[1, 1] = 2.0 * near_z / delta_y

        frust[2, 0] = (right + left) / delta_x
        frust[2, 1] = (top + bottom) / delta_y
        frust[2, 2] = -(near_z + far_z) / delta_z
        frust[2, 3] = -1.0

        frust[3, 2] = -2.0 * near_z * far_z / delta_z

        self.m = frust @ self.m


def check_shader_compile(shader, shader_type):
    if gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS) != gl.GL_TRUE:
        error_log = gl.glGetShaderInfoLog(shader).decode()
        raise RuntimeError(f'{shader_type} shader compilation failed:\n{error_log}')


def check_program_link(program):
    if gl.glGetProgramiv(program, gl.GL_LINK_STATUS) != gl.GL_TRUE:
        error_log = gl.glGetProgramInfoLog(program).decode()
        raise RuntimeError(f'Shader program linking failed:\n{error_log}')


def get_gl_string(name):
    s = gl.glGetString(name)
    return s.decode() if s else ''


class GlScene:
    def __init__(self):
        self.fps = FPSCounter()
        self.width = 0
        self.height = 0

        # Log GL information
        print(f'GL_VENDOR: {get_gl_string(gl.GL_VENDOR)}')
        print(f'GL_VERSION: {get_gl_string(gl.GL_VERSION)}')
        print(f'GL_RENDERER: {get_gl_string(gl.GL_RENDERER)}')

        # Initialize OpenGL resources
        self.program = self._create_program()
        self.vbo = self._create_cube_buffers()

        # Get uniform locations
        self.modelview_matrix_loc = gl.glGetUniformLocation(self.program, 'modelviewMatrix')
        self.modelviewprojection_matrix_loc = gl.glGetUniformLocation(self.program, 'modelviewprojectionMatrix')
        self.normal_matrix_loc = gl.glGetUniformLocation(self.program, 'normalMatrix')

        gl.glEnable(gl.GL_CULL_FACE)

    def cleanup(self):
        gl.glDeleteBuffers(1, [self.vbo])
        gl.glDeleteProgram(self.program)

    def _create_cube_buffers(self):
        size = 1.0

        # Define the 8 corners of a cube
        corner_vertices = np.array([
            # Front face corners (z+)
            [-size, -size, size],  # bottom-left-front
            [size, -size, size],   # bottom-right-front
            [-size, size, size],   # top-left-front
            [size, size, size],    # top-right-front

            # Back face corners (z-)
            [size, -size, -size],  # bottom-right-back
            [-size, -size, -size], # bottom-left-back
            [size, size, -size],   # top-right-back
            [-size, size, -size],  # top-left-back
        ])

        # Define the 6 face normals
        face_normals = np.array([
            [0, 0, 1],    # front (+z)
            [0, 0, -1],   # back (-z)
            [1, 0, 0],    # right (+x)
            [-1, 0, 0],   # left (-x)
            [0, 1, 0],    # top (+y)
            [0, -1, 0],   # bottom (-y)
        ])

        # Define vertex indices for each face as triangle strips
        # Each face uses 4 vertices
        face_indices = [
            [0, 1, 2, 3],   # front
            [4, 5, 6, 7],   # back
            [1, 4, 3, 6],   # right
            [5, 0, 7, 2],   # left
            [2, 3, 7, 6],   # top
            [5, 4, 0, 1]    # bottom
        ]

        # Generate a color for each corner (RGB)
        corner_colors = np.array([
            [0, 0, 1],      # blue (bottom-left-front)
            [1, 0, 1],      # magenta (bottom-right-front)
            [0, 1, 1],      # cyan (top-left-front)
            [1, 1, 1],      # white (top-right-front)
            [1, 0, 0],      # red (bottom-right-back)
            [0, 0, 0],      # black (bottom-left-back)
            [1, 1, 0],      # yellow (top-right-back)
            [0, 1, 0],      # green (top-left-back)
        ])

        # Initialize arrays for vertices, colors, and normals
        vertices = []
        colors = []
        normals = []

        # Generate data for each face
        faces = []
        start_idx = 0

        for face_idx, indices in enumerate(face_indices):
            faces.append((start_idx, 4))  # (start_index, count)

            # Add the 4 vertices for this face
            for vertex_idx in indices:
                vertices.append(corner_vertices[vertex_idx])
                colors.append(corner_colors[vertex_idx])
                normals.append(face_normals[face_idx])

            start_idx += 4

        vertices = np.array(vertices, dtype=np.float32)
        colors = np.array(colors, dtype=np.float32)
        normals = np.array(normals, dtype=np.float32)
        self.faces = faces

        # Create and bind vertex buffers
        vbo = gl.glGenBuffers(3)

        # Position buffer
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo[0])
        gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glEnableVertexAttribArray(0)

        # Normal buffer
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo[1])
        gl.glBufferData(gl.GL_ARRAY_BUFFER, normals.nbytes, normals, gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glEnableVertexAttribArray(1)

        # Color buffer
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo[2])
        gl.glBufferData(gl.GL_ARRAY_BUFFER, colors.nbytes, colors, gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(2, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glEnableVertexAttribArray(2)

        return vbo

    def _create_program(self):
        vertex_shader_source = '''
        uniform mat4 modelviewMatrix;
        uniform mat4 modelviewprojectionMatrix;
        uniform mat3 normalMatrix;

        attribute vec4 in_position;
        attribute vec3 in_normal;
        attribute vec3 in_color;

        vec4 lightSource = vec4(2.0, 2.0, 20.0, 0.0);

        varying vec4 vVaryingColor;

        void main()
        {
            gl_Position = modelviewprojectionMatrix * in_position;
            vec3 vEyeNormal = normalMatrix * in_normal;
            vec4 vPosition4 = modelviewMatrix * in_position;
            vec3 vPosition3 = vPosition4.xyz / vPosition4.w;
            vec3 vLightDir = normalize(lightSource.xyz - vPosition3);
            float diff = max(0.0, dot(vEyeNormal, vLightDir));
            vVaryingColor = vec4(diff * in_color, 1.0);
        }
        '''

        fragment_shader_source = '''
        precision mediump float;

        varying vec4 vVaryingColor;

        void main()
        {
            gl_FragColor = vVaryingColor;
        }
        '''

        # Compile vertex shader
        vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(vertex_shader, vertex_shader_source)
        gl.glCompileShader(vertex_shader)
        check_shader_compile(vertex_shader, 'Vertex')

        # Compile fragment shader
        fragment_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(fragment_shader, fragment_shader_source)
        gl.glCompileShader(fragment_shader)
        check_shader_compile(fragment_shader, 'Fragment')

        # Create and link program
        program = gl.glCreateProgram()
        gl.glAttachShader(program, vertex_shader)
        gl.glAttachShader(program, fragment_shader)

        # Bind attribute locations
        gl.glBindAttribLocation(program, 0, 'in_position')
        gl.glBindAttribLocation(program, 1, 'in_normal')
        gl.glBindAttribLocation(program, 2, 'in_color')

        gl.glLinkProgram(program)
        check_program_link(program)
        gl.glUseProgram(program)

        # Clean up shaders
        gl.glDeleteShader(vertex_shader)
        gl.glDeleteShader(fragment_shader)

        return program

    def set_viewport(self, width, height):
        self.width = width
        self.height = height
        gl.glViewport(0, 0, width, height)

    def draw(self, frame_num):
        self.fps.tick()

        # Clear the screen
        gl.glClearColor(0.5, 0.5, 0.5, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # Create modelview matrix
        modelview = ESMatrix()
        modelview.translate(0.0, 0.0, -8.0)

        # Apply rotations
        rotations = [
            (45.0 + (0.75 * frame_num), 1.0, 0.0, 0.0),
            (45.0 - (0.5 * frame_num), 0.0, 1.0, 0.0),
            (10.0 + (0.45 * frame_num), 0.0, 0.0, 1.0),
        ]

        for angle, x, y, z in rotations:
            modelview.rotate(angle, x, y, z)

        # Create projection matrix
        aspect = float(self.height) / self.width
        projection = ESMatrix()
        projection.frustum(-2.8, 2.8, -2.8 * aspect, 2.8 * aspect, 6.0, 10.0)

        # Create modelviewprojection matrix
        modelviewprojection = ESMatrix()
        modelviewprojection.m = modelview.m @ projection.m

        # Extract normal matrix
        normal = modelview.m[:3, :3].flatten()

        # Set uniforms
        gl.glUniformMatrix4fv(self.modelview_matrix_loc, 1, gl.GL_FALSE, modelview.m.flatten())
        gl.glUniformMatrix4fv(
            self.modelviewprojection_matrix_loc, 1, gl.GL_FALSE, modelviewprojection.m.flatten()
        )
        gl.glUniformMatrix3fv(self.normal_matrix_loc, 1, gl.GL_FALSE, normal)

        # Draw all cube faces
        for start, count in self.faces:
            gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, start, count)
