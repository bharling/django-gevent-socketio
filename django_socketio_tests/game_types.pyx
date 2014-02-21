import random, math

from libc.math cimport sqrt

cdef class Vector3:
    cdef double x
    cdef double y
    cdef double z
    
    @classmethod
    def random(cls):
        return cls(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))
    
    def cinit(self, double x, double y, double z):
        self.x = x
        self.y = y
        self.z = z
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    property x:
        def __get__(self):
            return self.x
        def __set__(self, double value):
            self.x = value
        
    property y:
        def __get__(self):
            return self.y
        def __set__(self, double value):
            self.y = value
            
    property z:
        def __get__(self):
            return self.z
        def __set__(self, double value):
            self.z = value
            
    def __add__(self, Vector3 other):
        return Vector3( self.x + other.x, self.y + other.y, self.z + other.z )
    
    def __iadd__(self, Vector3 other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self
    
    def __sub__(self, Vector3 other):
        return Vector3( self.x - other.x, self.y - other.y, self.z - other.z )
    
    def __isub__(self, Vector3 other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self
        
    def __mul__(self, Vector3 other):
        return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
    
    def __imul__(self, Vector3 other):
        self.x *= other.x
        self.y *= other.y
        self.z *= other.z
        return self
    
    cpdef Vector3 mulScalar(self, double other):
        return Vector3( self.x * other, self.y * other, self.z * other)
    
    def __div__(self, Vector3 other):
        return Vector3( self.x / other.x, self.y / other.y, self.z / other.z)
    
    def __idiv__(self, Vector3 other):
        self.x /= other.x
        self.y /= other.y
        self.z /= other.z
        return self
    
    cpdef Vector3 divScalar( self, double other ):
        return Vector3( self.x / other, self.y / other, self.z / other )
    
    cpdef normalize( self ):
        self /= self.length()
        return self
    
    cdef inline double length(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)
    
    property length:
        def __get__(self):
            return self.length()
        def __set__(self, double value):
            self.normalize().mulScalar(value)
            
            
    cpdef double squaredLength(self):
        return self.x**2+self.y**2+self.z**2
    
    cpdef double dot(self, Vector3 other):
        return self.x*other.x+self.y*other.y+self.z*other.z
    
    cpdef Vector3 lerp(self, Vector3 final, double percent):
        return self + ((final-self).mulScalar(percent))


cdef class Vector2:
    cdef double x
    cdef double y
    
    @classmethod
    def random(cls):
        return cls(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))
    
    def __cinit__(self, double x, double y):
        self.x = x
        self.y = y
        
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    property x:
        def __get__(self):
            return self.x
        def __set__(self, value):
            self.x = value
            
    property y:
        def __get__(self):
            return self.y
        def __set__(self, value):
            self.y = value
    
    def __add__(self, Vector2 other):
        return Vector2(self.x+other.x, self.y+other.y)
    
    def __iadd__(self, Vector2 other):
        self.x+=other.x
        self.y+=other.y
        return self
        
    def __sub__(self, Vector2 other):
        return Vector2(self.x-other.x, self.y-other.y)
    
    def __isub__(self, Vector2 other):
        self.x-=other.x
        self.y-=other.y
        return self
        
    def __mul__(self, Vector2 other):
        return Vector2(self.x*other.x, self.y*other.y)
    
    cpdef Vector2 mulScalar(self, double other):
        return Vector2(self.x*other, self.y*other)

    def __imul__(self, other):
        if hasattr(other, 'x'):
            self.x*=other.x
            self.y*=other.y
        else:
            self.x *= float(other)
            self.y *= float(other)
        return self
            
    def __div__(self, other):
        if hasattr(other, 'x'):
            return Vector2(self.x/other.x, self.y/other.y)
        else:
            return Vector2(self.x/float(other), self.y/float(other))
        
    def __idiv__(self, other):
        if hasattr(other, 'x'):
            self.x/=other.x
            self.y/=other.y
        else:
            self.x /= float(other)
            self.y /= float(other)
        return self
            
    cdef double length(self):
        return sqrt(self.x**2+self.y**2)
    
    property length:
        def __get__(self):
            return self.length()
        def __set__(self, double other):
            self.normalize()
            self.mulScalar(other)
    
    cpdef double squaredLength(self):
        return self.x**2+self.y**2
        
    cpdef Vector2 copy(self):
        return Vector2(self.x, self.y)
        
    cpdef Vector2 normalizedCopy(self):
        return self.copy() / self.length()
    
    cpdef Vector2 normalize(self):
        self /= self.length()
        return self
        
    cpdef double dot(self, Vector2 other):
        return self.x*other.x+self.y*other.y
        
    cpdef Vector2 lerp(self,Vector2 final, double percent):
        return self + ((final-self).mulScalar(percent))
    
class OctreeNode:
    def __init__(self, position, id):
        self.position = position
        self.id = id


#    +z
#    |   +y
#    |  /
#    | /
#     /_________+x


cdef class Octree:
    cdef int depth
    cdef Vector3 center
    cdef double size
    cdef double halfSize
    
    # children
    cdef Octree lfu
    cdef Octree lfd
    cdef Octree lbu
    cdef Octree lbd
    cdef Octree rfu
    cdef Octree rfd
    cdef Octree rbu
    cdef Octree rbd
    
    def __cinit__(self, Vector3 center, double size, int depth = 0):
        self.depth = depth
        self.center = center
        self.size = size
        self.halfSize = size / 2
        self.nodes = []
        
    property depth:
        def __get__(self):
            return self.depth
        
    def add(self, node):
        self.nodes.append(node)
        if len(self.nodes) > 8:
            self.split()
            
    cdef inline Octree find_branch(self, Vector3 pos):
        return self.lfu
            
    cdef inline split(self):
        cdef Vector3 temp
        
        cdef int newdepth = self.depth + 1
        cdef double qsize = self.halfSize / 2.0
        
        #left front up
        temp = Vector3(self.center.x - qsize, self.center.y - qsize, self.center.z + qsize)
        self.lfu = Octree(temp.copy(), self.halfSize, newdepth)
        
        #left front down
        temp = Vector3(self.center.x - qsize, self.center.y - qsize, self.center.z - qsize )
        self.lfd = Octree(temp.copy(), self.halfSize, newdepth)
        
        #left back up
        temp = Vector3(self.center.x - qsize, self.center.y + qsize, self.center.z + qsize)
        self.lbu = Octree(temp.copy(), self.halfSize, newdepth)
        
        #left back down
        temp = Vector3(self.center.x - qsize, self.center.y + qsize, self.center.z - qsize)
        self.lbd = Octree(temp.copy(), self.halfSize, newdepth)
        
        #right front up
        temp = Vector3(self.center.x + qsize, self.center.y - qsize, self.center.z + qsize )
        self.rfu = Octree(temp.copy(), self.halfSize, newdepth)
        
        #right front down
        temp = Vector3(self.center.x + qsize, self.center.y - qsize, self.center.z - qsize )
        self.rfd = Octree(temp.copy(), self.halfSize, newdepth)
        
        #right back up
        temp = Vector3(self.center.x + qsize, self.center.y + qsize, self.center.z + qsize )
        self.rbu = Octree(temp.copy(), self.halfSize, newdepth)
        
        #right back down
        temp = Vector3(self.center.x + qsize, self.center.y + qsize, self.center.z - qsize )
        self.rbd = Octree(temp.copy(), self.halfSize, newdepth)
    
        
    
        
    
        
    
        
        
    
    
    
    
