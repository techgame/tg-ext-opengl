#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from _ctypes_opengl import *
from gl import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Code generated from:
#~   "inc/OpenGL/glu.h"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GLU_EXT_object_space_tess = 1
GLU_EXT_nurbs_tessellator = 1

GLU_FALSE = 0
GLU_TRUE = 1

GLU_VERSION_1_1 = 1
GLU_VERSION_1_2 = 1
GLU_VERSION_1_3 = 1

GLU_VERSION = 100800
GLU_EXTENSIONS = 100801

GLU_INVALID_ENUM = 100900
GLU_INVALID_VALUE = 100901
GLU_OUT_OF_MEMORY = 100902
GLU_INCOMPATIBLE_GL_VERSION = 100903
GLU_INVALID_OPERATION = 100904

#~ line: 44, skipped: 5 ~~~~~~

GLU_OUTLINE_POLYGON = 100240
GLU_OUTLINE_PATCH = 100241

GLU_NURBS_ERROR = 100103
GLU_ERROR = 100103
GLU_NURBS_BEGIN = 100164
GLU_NURBS_BEGIN_EXT = 100164
GLU_NURBS_VERTEX = 100165
GLU_NURBS_VERTEX_EXT = 100165
GLU_NURBS_NORMAL = 100166
GLU_NURBS_NORMAL_EXT = 100166
GLU_NURBS_COLOR = 100167
GLU_NURBS_COLOR_EXT = 100167
GLU_NURBS_TEXTURE_COORD = 100168
GLU_NURBS_TEX_COORD_EXT = 100168
GLU_NURBS_END = 100169
GLU_NURBS_END_EXT = 100169
GLU_NURBS_BEGIN_DATA = 100170
GLU_NURBS_BEGIN_DATA_EXT = 100170
GLU_NURBS_VERTEX_DATA = 100171
GLU_NURBS_VERTEX_DATA_EXT = 100171
GLU_NURBS_NORMAL_DATA = 100172
GLU_NURBS_NORMAL_DATA_EXT = 100172
GLU_NURBS_COLOR_DATA = 100173
GLU_NURBS_COLOR_DATA_EXT = 100173
GLU_NURBS_TEXTURE_COORD_DATA = 100174
GLU_NURBS_TEX_COORD_DATA_EXT = 100174
GLU_NURBS_END_DATA = 100175
GLU_NURBS_END_DATA_EXT = 100175

GLU_NURBS_ERROR1 = 100251
GLU_NURBS_ERROR2 = 100252
GLU_NURBS_ERROR3 = 100253
GLU_NURBS_ERROR4 = 100254
GLU_NURBS_ERROR5 = 100255
GLU_NURBS_ERROR6 = 100256
GLU_NURBS_ERROR7 = 100257
GLU_NURBS_ERROR8 = 100258
GLU_NURBS_ERROR9 = 100259
GLU_NURBS_ERROR10 = 100260
GLU_NURBS_ERROR11 = 100261
GLU_NURBS_ERROR12 = 100262
GLU_NURBS_ERROR13 = 100263
GLU_NURBS_ERROR14 = 100264
GLU_NURBS_ERROR15 = 100265
GLU_NURBS_ERROR16 = 100266
GLU_NURBS_ERROR17 = 100267
GLU_NURBS_ERROR18 = 100268
GLU_NURBS_ERROR19 = 100269
GLU_NURBS_ERROR20 = 100270
GLU_NURBS_ERROR21 = 100271
GLU_NURBS_ERROR22 = 100272
GLU_NURBS_ERROR23 = 100273
GLU_NURBS_ERROR24 = 100274
GLU_NURBS_ERROR25 = 100275
GLU_NURBS_ERROR26 = 100276
GLU_NURBS_ERROR27 = 100277
GLU_NURBS_ERROR28 = 100278
GLU_NURBS_ERROR29 = 100279
GLU_NURBS_ERROR30 = 100280
GLU_NURBS_ERROR31 = 100281
GLU_NURBS_ERROR32 = 100282
GLU_NURBS_ERROR33 = 100283
GLU_NURBS_ERROR34 = 100284
GLU_NURBS_ERROR35 = 100285
GLU_NURBS_ERROR36 = 100286
GLU_NURBS_ERROR37 = 100287

GLU_AUTO_LOAD_MATRIX = 100200
GLU_CULLING = 100201
GLU_SAMPLING_TOLERANCE = 100203
GLU_DISPLAY_MODE = 100204
GLU_PARAMETRIC_TOLERANCE = 100202
GLU_SAMPLING_METHOD = 100205
GLU_U_STEP = 100206
GLU_V_STEP = 100207
GLU_NURBS_MODE = 100160
GLU_NURBS_MODE_EXT = 100160
GLU_NURBS_TESSELLATOR = 100161
GLU_NURBS_TESSELLATOR_EXT = 100161
GLU_NURBS_RENDERER = 100162
GLU_NURBS_RENDERER_EXT = 100162

GLU_OBJECT_PARAMETRIC_ERROR = 100208
GLU_OBJECT_PARAMETRIC_ERROR_EXT = 100208
GLU_OBJECT_PATH_LENGTH = 100209
GLU_OBJECT_PATH_LENGTH_EXT = 100209
GLU_PATH_LENGTH = 100215
GLU_PARAMETRIC_ERROR = 100216
GLU_DOMAIN_DISTANCE = 100217

GLU_MAP1_TRIM_2 = 100210
GLU_MAP1_TRIM_3 = 100211

GLU_POINT = 100010
GLU_LINE = 100011
GLU_FILL = 100012
GLU_SILHOUETTE = 100013

#~ line: 153, skipped: 6 ~~~~~~

GLU_SMOOTH = 100000
GLU_FLAT = 100001
GLU_NONE = 100002

GLU_OUTSIDE = 100020
GLU_INSIDE = 100021

GLU_TESS_BEGIN = 100100
GLU_BEGIN = 100100
GLU_TESS_VERTEX = 100101
GLU_VERTEX = 100101
GLU_TESS_END = 100102
GLU_END = 100102
GLU_TESS_ERROR = 100103
GLU_TESS_EDGE_FLAG = 100104
GLU_EDGE_FLAG = 100104
GLU_TESS_COMBINE = 100105
GLU_TESS_BEGIN_DATA = 100106
GLU_TESS_VERTEX_DATA = 100107
GLU_TESS_END_DATA = 100108
GLU_TESS_ERROR_DATA = 100109
GLU_TESS_EDGE_FLAG_DATA = 100110
GLU_TESS_COMBINE_DATA = 100111

GLU_CW = 100120
GLU_CCW = 100121
GLU_INTERIOR = 100122
GLU_EXTERIOR = 100123
GLU_UNKNOWN = 100124

GLU_TESS_WINDING_RULE = 100140
GLU_TESS_BOUNDARY_ONLY = 100141
GLU_TESS_TOLERANCE = 100142

GLU_TESS_ERROR1 = 100151
GLU_TESS_ERROR2 = 100152
GLU_TESS_ERROR3 = 100153
GLU_TESS_ERROR4 = 100154
GLU_TESS_ERROR5 = 100155
GLU_TESS_ERROR6 = 100156
GLU_TESS_ERROR7 = 100157
GLU_TESS_ERROR8 = 100158
GLU_TESS_MISSING_BEGIN_POLYGON = 100151
GLU_TESS_MISSING_BEGIN_CONTOUR = 100152
GLU_TESS_MISSING_END_POLYGON = 100153
GLU_TESS_MISSING_END_CONTOUR = 100154
GLU_TESS_COORD_TOO_LARGE = 100155
GLU_TESS_NEED_COMBINE_CALLBACK = 100156

GLU_TESS_WINDING_ODD = 100130
GLU_TESS_WINDING_NONZERO = 100131
GLU_TESS_WINDING_POSITIVE = 100132
GLU_TESS_WINDING_NEGATIVE = 100133
GLU_TESS_WINDING_ABS_GEQ_TWO = 100134

#~ line: 218, skipped: 6 ~~~~~~

class GLUnurbs(Structure):
    _fields_ = []
class GLUquadric(Structure):
    _fields_ = []
class GLUtesselator(Structure):
    _fields_ = []

#~ line: 237, skipped: 17 ~~~~~~

GLU_TESS_MAX_COORD = 1.0e150

@bind(None, [POINTER(GLUnurbs)])
def gluBeginCurve(nurb, _api_=None): 
    """gluBeginCurve(nurb)
    
        nurb : POINTER(GLUnurbs)
    """
    return _api_(nurb)
    
@bind(None, [POINTER(GLUtesselator)])
def gluBeginPolygon(tess, _api_=None): 
    """gluBeginPolygon(tess)
    
        tess : POINTER(GLUtesselator)
    """
    return _api_(tess)
    
@bind(None, [POINTER(GLUnurbs)])
def gluBeginSurface(nurb, _api_=None): 
    """gluBeginSurface(nurb)
    
        nurb : POINTER(GLUnurbs)
    """
    return _api_(nurb)
    
@bind(None, [POINTER(GLUnurbs)])
def gluBeginTrim(nurb, _api_=None): 
    """gluBeginTrim(nurb)
    
        nurb : POINTER(GLUnurbs)
    """
    return _api_(nurb)
    
@bind(GLint, [GLenum, GLint, GLsizei, GLenum, GLenum, GLint, GLint, GLint, c_void_p])
def gluBuild1DMipmapLevels(target, internalFormat, width, format, type, level, base, max, data, _api_=None): 
    """gluBuild1DMipmapLevels(target, internalFormat, width, format, type, level, base, max, data)
    
        target : GLenum
        internalFormat : GLint
        width : GLsizei
        format : GLenum
        type : GLenum
        level : GLint
        base : GLint
        max : GLint
        data : c_void_p
    """
    return _api_(target, internalFormat, width, format, type, level, base, max, data)
    
@bind(GLint, [GLenum, GLint, GLsizei, GLenum, GLenum, c_void_p])
def gluBuild1DMipmaps(target, internalFormat, width, format, type, data, _api_=None): 
    """gluBuild1DMipmaps(target, internalFormat, width, format, type, data)
    
        target : GLenum
        internalFormat : GLint
        width : GLsizei
        format : GLenum
        type : GLenum
        data : c_void_p
    """
    return _api_(target, internalFormat, width, format, type, data)
    
@bind(GLint, [GLenum, GLint, GLsizei, GLsizei, GLenum, GLenum, GLint, GLint, GLint, c_void_p])
def gluBuild2DMipmapLevels(target, internalFormat, width, height, format, type, level, base, max, data, _api_=None): 
    """gluBuild2DMipmapLevels(target, internalFormat, width, height, format, type, level, base, max, data)
    
        target : GLenum
        internalFormat : GLint
        width : GLsizei
        height : GLsizei
        format : GLenum
        type : GLenum
        level : GLint
        base : GLint
        max : GLint
        data : c_void_p
    """
    return _api_(target, internalFormat, width, height, format, type, level, base, max, data)
    
@bind(GLint, [GLenum, GLint, GLsizei, GLsizei, GLenum, GLenum, c_void_p])
def gluBuild2DMipmaps(target, internalFormat, width, height, format, type, data, _api_=None): 
    """gluBuild2DMipmaps(target, internalFormat, width, height, format, type, data)
    
        target : GLenum
        internalFormat : GLint
        width : GLsizei
        height : GLsizei
        format : GLenum
        type : GLenum
        data : c_void_p
    """
    return _api_(target, internalFormat, width, height, format, type, data)
    
@bind(GLint, [GLenum, GLint, GLsizei, GLsizei, GLsizei, GLenum, GLenum, GLint, GLint, GLint, c_void_p])
def gluBuild3DMipmapLevels(target, internalFormat, width, height, depth, format, type, level, base, max, data, _api_=None): 
    """gluBuild3DMipmapLevels(target, internalFormat, width, height, depth, format, type, level, base, max, data)
    
        target : GLenum
        internalFormat : GLint
        width : GLsizei
        height : GLsizei
        depth : GLsizei
        format : GLenum
        type : GLenum
        level : GLint
        base : GLint
        max : GLint
        data : c_void_p
    """
    return _api_(target, internalFormat, width, height, depth, format, type, level, base, max, data)
    
@bind(GLint, [GLenum, GLint, GLsizei, GLsizei, GLsizei, GLenum, GLenum, c_void_p])
def gluBuild3DMipmaps(target, internalFormat, width, height, depth, format, type, data, _api_=None): 
    """gluBuild3DMipmaps(target, internalFormat, width, height, depth, format, type, data)
    
        target : GLenum
        internalFormat : GLint
        width : GLsizei
        height : GLsizei
        depth : GLsizei
        format : GLenum
        type : GLenum
        data : c_void_p
    """
    return _api_(target, internalFormat, width, height, depth, format, type, data)
    
@bind(GLboolean, [POINTER(GLubyte), POINTER(GLubyte)])
def gluCheckExtension(extName, extString, _api_=None): 
    """gluCheckExtension(extName, extString)
    
        extName : POINTER(GLubyte)
        extString : POINTER(GLubyte)
    """
    return _api_(extName, extString)
    
@bind(None, [POINTER(GLUquadric), GLdouble, GLdouble, GLdouble, GLint, GLint])
def gluCylinder(quad, base, top, height, slices, stacks, _api_=None): 
    """gluCylinder(quad, base, top, height, slices, stacks)
    
        quad : POINTER(GLUquadric)
        base : GLdouble
        top : GLdouble
        height : GLdouble
        slices : GLint
        stacks : GLint
    """
    return _api_(quad, base, top, height, slices, stacks)
    
@bind(None, [POINTER(GLUnurbs)])
def gluDeleteNurbsRenderer(nurb, _api_=None): 
    """gluDeleteNurbsRenderer(nurb)
    
        nurb : POINTER(GLUnurbs)
    """
    return _api_(nurb)
    
@bind(None, [POINTER(GLUquadric)])
def gluDeleteQuadric(quad, _api_=None): 
    """gluDeleteQuadric(quad)
    
        quad : POINTER(GLUquadric)
    """
    return _api_(quad)
    
@bind(None, [POINTER(GLUtesselator)])
def gluDeleteTess(tess, _api_=None): 
    """gluDeleteTess(tess)
    
        tess : POINTER(GLUtesselator)
    """
    return _api_(tess)
    
@bind(None, [POINTER(GLUquadric), GLdouble, GLdouble, GLint, GLint])
def gluDisk(quad, inner, outer, slices, loops, _api_=None): 
    """gluDisk(quad, inner, outer, slices, loops)
    
        quad : POINTER(GLUquadric)
        inner : GLdouble
        outer : GLdouble
        slices : GLint
        loops : GLint
    """
    return _api_(quad, inner, outer, slices, loops)
    
@bind(None, [POINTER(GLUnurbs)])
def gluEndCurve(nurb, _api_=None): 
    """gluEndCurve(nurb)
    
        nurb : POINTER(GLUnurbs)
    """
    return _api_(nurb)
    
@bind(None, [POINTER(GLUtesselator)])
def gluEndPolygon(tess, _api_=None): 
    """gluEndPolygon(tess)
    
        tess : POINTER(GLUtesselator)
    """
    return _api_(tess)
    
@bind(None, [POINTER(GLUnurbs)])
def gluEndSurface(nurb, _api_=None): 
    """gluEndSurface(nurb)
    
        nurb : POINTER(GLUnurbs)
    """
    return _api_(nurb)
    
@bind(None, [POINTER(GLUnurbs)])
def gluEndTrim(nurb, _api_=None): 
    """gluEndTrim(nurb)
    
        nurb : POINTER(GLUnurbs)
    """
    return _api_(nurb)
    
@bind(c_char_p, [GLenum])
def gluErrorString(error, _api_=None): 
    """gluErrorString(error)
    
        error : GLenum
    """
    return _api_(error)
    
@bind(None, [POINTER(GLUnurbs), GLenum, POINTER(GLfloat)])
def gluGetNurbsProperty(nurb, property, data, _api_=None): 
    """gluGetNurbsProperty(nurb, property, data)
    
        nurb : POINTER(GLUnurbs)
        property : GLenum
        data : POINTER(GLfloat)
    """
    return _api_(nurb, property, data)
    
@bind(POINTER(GLubyte), [GLenum])
def gluGetString(name, _api_=None): 
    """gluGetString(name)
    
        name : GLenum
    """
    return _api_(name)
    
@bind(None, [POINTER(GLUtesselator), GLenum, POINTER(GLdouble)])
def gluGetTessProperty(tess, which, data, _api_=None): 
    """gluGetTessProperty(tess, which, data)
    
        tess : POINTER(GLUtesselator)
        which : GLenum
        data : POINTER(GLdouble)
    """
    return _api_(tess, which, data)
    
@bind(None, [POINTER(GLUnurbs), POINTER(GLfloat), POINTER(GLfloat), POINTER(GLint)])
def gluLoadSamplingMatrices(nurb, model, perspective, view, _api_=None): 
    """gluLoadSamplingMatrices(nurb, model, perspective, view)
    
        nurb : POINTER(GLUnurbs)
        model : POINTER(GLfloat)
        perspective : POINTER(GLfloat)
        view : POINTER(GLint)
    """
    return _api_(nurb, model, perspective, view)
    
@bind(None, [GLdouble, GLdouble, GLdouble, GLdouble, GLdouble, GLdouble, GLdouble, GLdouble, GLdouble])
def gluLookAt(eyeX, eyeY, eyeZ, centerX, centerY, centerZ, upX, upY, upZ, _api_=None): 
    """gluLookAt(eyeX, eyeY, eyeZ, centerX, centerY, centerZ, upX, upY, upZ)
    
        eyeX : GLdouble
        eyeY : GLdouble
        eyeZ : GLdouble
        centerX : GLdouble
        centerY : GLdouble
        centerZ : GLdouble
        upX : GLdouble
        upY : GLdouble
        upZ : GLdouble
    """
    return _api_(eyeX, eyeY, eyeZ, centerX, centerY, centerZ, upX, upY, upZ)
    
@bind(POINTER(GLUnurbs), [])
def gluNewNurbsRenderer(_api_=None): 
    """gluNewNurbsRenderer()
    
        
    """
    return _api_()
    
@bind(POINTER(GLUquadric), [])
def gluNewQuadric(_api_=None): 
    """gluNewQuadric()
    
        
    """
    return _api_()
    
@bind(POINTER(GLUtesselator), [])
def gluNewTess(_api_=None): 
    """gluNewTess()
    
        
    """
    return _api_()
    
@bind(None, [POINTER(GLUtesselator), GLenum])
def gluNextContour(tess, type, _api_=None): 
    """gluNextContour(tess, type)
    
        tess : POINTER(GLUtesselator)
        type : GLenum
    """
    return _api_(tess, type)
    
@bind(None, [POINTER(GLUnurbs), GLenum, POINTER(CFUNCTYPE(GLvoid, ))])
def gluNurbsCallback(nurb, which, CallBackFunc, _api_=None): 
    """gluNurbsCallback(nurb, which, CallBackFunc)
    
        nurb : POINTER(GLUnurbs)
        which : GLenum
        CallBackFunc : POINTER(CFUNCTYPE(GLvoid, ))
    """
    return _api_(nurb, which, CallBackFunc)
    
@bind(None, [POINTER(GLUnurbs), POINTER(GLvoid)])
def gluNurbsCallbackData(nurb, userData, _api_=None): 
    """gluNurbsCallbackData(nurb, userData)
    
        nurb : POINTER(GLUnurbs)
        userData : POINTER(GLvoid)
    """
    return _api_(nurb, userData)
    
@bind(None, [POINTER(GLUnurbs), POINTER(GLvoid)])
def gluNurbsCallbackDataEXT(nurb, userData, _api_=None): 
    """gluNurbsCallbackDataEXT(nurb, userData)
    
        nurb : POINTER(GLUnurbs)
        userData : POINTER(GLvoid)
    """
    return _api_(nurb, userData)
    
@bind(None, [POINTER(GLUnurbs), GLint, POINTER(GLfloat), GLint, POINTER(GLfloat), GLint, GLenum])
def gluNurbsCurve(nurb, knotCount, knots, stride, control, order, type, _api_=None): 
    """gluNurbsCurve(nurb, knotCount, knots, stride, control, order, type)
    
        nurb : POINTER(GLUnurbs)
        knotCount : GLint
        knots : POINTER(GLfloat)
        stride : GLint
        control : POINTER(GLfloat)
        order : GLint
        type : GLenum
    """
    return _api_(nurb, knotCount, knots, stride, control, order, type)
    
@bind(None, [POINTER(GLUnurbs), GLenum, GLfloat])
def gluNurbsProperty(nurb, property, value, _api_=None): 
    """gluNurbsProperty(nurb, property, value)
    
        nurb : POINTER(GLUnurbs)
        property : GLenum
        value : GLfloat
    """
    return _api_(nurb, property, value)
    
@bind(None, [POINTER(GLUnurbs), GLint, POINTER(GLfloat), GLint, POINTER(GLfloat), GLint, GLint, POINTER(GLfloat), GLint, GLint, GLenum])
def gluNurbsSurface(nurb, sKnotCount, sKnots, tKnotCount, tKnots, sStride, tStride, control, sOrder, tOrder, type, _api_=None): 
    """gluNurbsSurface(nurb, sKnotCount, sKnots, tKnotCount, tKnots, sStride, tStride, control, sOrder, tOrder, type)
    
        nurb : POINTER(GLUnurbs)
        sKnotCount : GLint
        sKnots : POINTER(GLfloat)
        tKnotCount : GLint
        tKnots : POINTER(GLfloat)
        sStride : GLint
        tStride : GLint
        control : POINTER(GLfloat)
        sOrder : GLint
        tOrder : GLint
        type : GLenum
    """
    return _api_(nurb, sKnotCount, sKnots, tKnotCount, tKnots, sStride, tStride, control, sOrder, tOrder, type)
    
@bind(None, [GLdouble, GLdouble, GLdouble, GLdouble])
def gluOrtho2D(left, right, bottom, top, _api_=None): 
    """gluOrtho2D(left, right, bottom, top)
    
        left : GLdouble
        right : GLdouble
        bottom : GLdouble
        top : GLdouble
    """
    return _api_(left, right, bottom, top)
    
@bind(None, [POINTER(GLUquadric), GLdouble, GLdouble, GLint, GLint, GLdouble, GLdouble])
def gluPartialDisk(quad, inner, outer, slices, loops, start, sweep, _api_=None): 
    """gluPartialDisk(quad, inner, outer, slices, loops, start, sweep)
    
        quad : POINTER(GLUquadric)
        inner : GLdouble
        outer : GLdouble
        slices : GLint
        loops : GLint
        start : GLdouble
        sweep : GLdouble
    """
    return _api_(quad, inner, outer, slices, loops, start, sweep)
    
@bind(None, [GLdouble, GLdouble, GLdouble, GLdouble])
def gluPerspective(fovy, aspect, zNear, zFar, _api_=None): 
    """gluPerspective(fovy, aspect, zNear, zFar)
    
        fovy : GLdouble
        aspect : GLdouble
        zNear : GLdouble
        zFar : GLdouble
    """
    return _api_(fovy, aspect, zNear, zFar)
    
@bind(None, [GLdouble, GLdouble, GLdouble, GLdouble, POINTER(GLint)])
def gluPickMatrix(x, y, delX, delY, viewport, _api_=None): 
    """gluPickMatrix(x, y, delX, delY, viewport)
    
        x : GLdouble
        y : GLdouble
        delX : GLdouble
        delY : GLdouble
        viewport : POINTER(GLint)
    """
    return _api_(x, y, delX, delY, viewport)
    
@bind(GLint, [GLdouble, GLdouble, GLdouble, POINTER(GLdouble), POINTER(GLdouble), POINTER(GLint), POINTER(GLdouble), POINTER(GLdouble), POINTER(GLdouble)])
def gluProject(objX, objY, objZ, model, proj, view, winX, winY, winZ, _api_=None): 
    """gluProject(objX, objY, objZ, model, proj, view, winX, winY, winZ)
    
        objX : GLdouble
        objY : GLdouble
        objZ : GLdouble
        model : POINTER(GLdouble)
        proj : POINTER(GLdouble)
        view : POINTER(GLint)
        winX : POINTER(GLdouble)
        winY : POINTER(GLdouble)
        winZ : POINTER(GLdouble)
    """
    return _api_(objX, objY, objZ, model, proj, view, winX, winY, winZ)
    
@bind(None, [POINTER(GLUnurbs), GLint, POINTER(GLfloat), GLint, GLenum])
def gluPwlCurve(nurb, count, data, stride, type, _api_=None): 
    """gluPwlCurve(nurb, count, data, stride, type)
    
        nurb : POINTER(GLUnurbs)
        count : GLint
        data : POINTER(GLfloat)
        stride : GLint
        type : GLenum
    """
    return _api_(nurb, count, data, stride, type)
    
@bind(None, [POINTER(GLUquadric), GLenum, POINTER(CFUNCTYPE(GLvoid, ))])
def gluQuadricCallback(quad, which, CallBackFunc, _api_=None): 
    """gluQuadricCallback(quad, which, CallBackFunc)
    
        quad : POINTER(GLUquadric)
        which : GLenum
        CallBackFunc : POINTER(CFUNCTYPE(GLvoid, ))
    """
    return _api_(quad, which, CallBackFunc)
    
@bind(None, [POINTER(GLUquadric), GLenum])
def gluQuadricDrawStyle(quad, draw, _api_=None): 
    """gluQuadricDrawStyle(quad, draw)
    
        quad : POINTER(GLUquadric)
        draw : GLenum
    """
    return _api_(quad, draw)
    
@bind(None, [POINTER(GLUquadric), GLenum])
def gluQuadricNormals(quad, normal, _api_=None): 
    """gluQuadricNormals(quad, normal)
    
        quad : POINTER(GLUquadric)
        normal : GLenum
    """
    return _api_(quad, normal)
    
@bind(None, [POINTER(GLUquadric), GLenum])
def gluQuadricOrientation(quad, orientation, _api_=None): 
    """gluQuadricOrientation(quad, orientation)
    
        quad : POINTER(GLUquadric)
        orientation : GLenum
    """
    return _api_(quad, orientation)
    
@bind(None, [POINTER(GLUquadric), GLboolean])
def gluQuadricTexture(quad, texture, _api_=None): 
    """gluQuadricTexture(quad, texture)
    
        quad : POINTER(GLUquadric)
        texture : GLboolean
    """
    return _api_(quad, texture)
    
@bind(GLint, [GLenum, GLsizei, GLsizei, GLenum, c_void_p, GLsizei, GLsizei, GLenum, POINTER(GLvoid)])
def gluScaleImage(format, wIn, hIn, typeIn, dataIn, wOut, hOut, typeOut, dataOut, _api_=None): 
    """gluScaleImage(format, wIn, hIn, typeIn, dataIn, wOut, hOut, typeOut, dataOut)
    
        format : GLenum
        wIn : GLsizei
        hIn : GLsizei
        typeIn : GLenum
        dataIn : c_void_p
        wOut : GLsizei
        hOut : GLsizei
        typeOut : GLenum
        dataOut : POINTER(GLvoid)
    """
    return _api_(format, wIn, hIn, typeIn, dataIn, wOut, hOut, typeOut, dataOut)
    
@bind(None, [POINTER(GLUquadric), GLdouble, GLint, GLint])
def gluSphere(quad, radius, slices, stacks, _api_=None): 
    """gluSphere(quad, radius, slices, stacks)
    
        quad : POINTER(GLUquadric)
        radius : GLdouble
        slices : GLint
        stacks : GLint
    """
    return _api_(quad, radius, slices, stacks)
    
@bind(None, [POINTER(GLUtesselator)])
def gluTessBeginContour(tess, _api_=None): 
    """gluTessBeginContour(tess)
    
        tess : POINTER(GLUtesselator)
    """
    return _api_(tess)
    
@bind(None, [POINTER(GLUtesselator), POINTER(GLvoid)])
def gluTessBeginPolygon(tess, data, _api_=None): 
    """gluTessBeginPolygon(tess, data)
    
        tess : POINTER(GLUtesselator)
        data : POINTER(GLvoid)
    """
    return _api_(tess, data)
    
@bind(None, [POINTER(GLUtesselator), GLenum, POINTER(CFUNCTYPE(GLvoid, ))])
def gluTessCallback(tess, which, CallBackFunc, _api_=None): 
    """gluTessCallback(tess, which, CallBackFunc)
    
        tess : POINTER(GLUtesselator)
        which : GLenum
        CallBackFunc : POINTER(CFUNCTYPE(GLvoid, ))
    """
    return _api_(tess, which, CallBackFunc)
    
@bind(None, [POINTER(GLUtesselator)])
def gluTessEndContour(tess, _api_=None): 
    """gluTessEndContour(tess)
    
        tess : POINTER(GLUtesselator)
    """
    return _api_(tess)
    
@bind(None, [POINTER(GLUtesselator)])
def gluTessEndPolygon(tess, _api_=None): 
    """gluTessEndPolygon(tess)
    
        tess : POINTER(GLUtesselator)
    """
    return _api_(tess)
    
@bind(None, [POINTER(GLUtesselator), GLdouble, GLdouble, GLdouble])
def gluTessNormal(tess, valueX, valueY, valueZ, _api_=None): 
    """gluTessNormal(tess, valueX, valueY, valueZ)
    
        tess : POINTER(GLUtesselator)
        valueX : GLdouble
        valueY : GLdouble
        valueZ : GLdouble
    """
    return _api_(tess, valueX, valueY, valueZ)
    
@bind(None, [POINTER(GLUtesselator), GLenum, GLdouble])
def gluTessProperty(tess, which, data, _api_=None): 
    """gluTessProperty(tess, which, data)
    
        tess : POINTER(GLUtesselator)
        which : GLenum
        data : GLdouble
    """
    return _api_(tess, which, data)
    
@bind(None, [POINTER(GLUtesselator), POINTER(GLdouble), POINTER(GLvoid)])
def gluTessVertex(tess, location, data, _api_=None): 
    """gluTessVertex(tess, location, data)
    
        tess : POINTER(GLUtesselator)
        location : POINTER(GLdouble)
        data : POINTER(GLvoid)
    """
    return _api_(tess, location, data)
    
@bind(GLint, [GLdouble, GLdouble, GLdouble, POINTER(GLdouble), POINTER(GLdouble), POINTER(GLint), POINTER(GLdouble), POINTER(GLdouble), POINTER(GLdouble)])
def gluUnProject(winX, winY, winZ, model, proj, view, objX, objY, objZ, _api_=None): 
    """gluUnProject(winX, winY, winZ, model, proj, view, objX, objY, objZ)
    
        winX : GLdouble
        winY : GLdouble
        winZ : GLdouble
        model : POINTER(GLdouble)
        proj : POINTER(GLdouble)
        view : POINTER(GLint)
        objX : POINTER(GLdouble)
        objY : POINTER(GLdouble)
        objZ : POINTER(GLdouble)
    """
    return _api_(winX, winY, winZ, model, proj, view, objX, objY, objZ)
    
@bind(GLint, [GLdouble, GLdouble, GLdouble, GLdouble, POINTER(GLdouble), POINTER(GLdouble), POINTER(GLint), GLdouble, GLdouble, POINTER(GLdouble), POINTER(GLdouble), POINTER(GLdouble), POINTER(GLdouble)])
def gluUnProject4(winX, winY, winZ, clipW, model, proj, view, near, far, objX, objY, objZ, objW, _api_=None): 
    """gluUnProject4(winX, winY, winZ, clipW, model, proj, view, near, far, objX, objY, objZ, objW)
    
        winX : GLdouble
        winY : GLdouble
        winZ : GLdouble
        clipW : GLdouble
        model : POINTER(GLdouble)
        proj : POINTER(GLdouble)
        view : POINTER(GLint)
        near : GLdouble
        far : GLdouble
        objX : POINTER(GLdouble)
        objY : POINTER(GLdouble)
        objZ : POINTER(GLdouble)
        objW : POINTER(GLdouble)
    """
    return _api_(winX, winY, winZ, clipW, model, proj, view, near, far, objX, objY, objZ, objW)
    


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ End of code generated from:
#~   "inc/OpenGL/glu.h"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

