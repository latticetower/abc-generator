import typing
import numpy as np


class Vertex(typing.NamedTuple):
    x: float
    y: float
    z: float
    
    @classmethod
    def load(cls, s):
        vertices = [np.float(x) for x in s.strip().split()[1:]]
        return cls(*vertices)

    def __repr__(self):
        return f"v {self.x} {self.y} {self.z}"


class Face(typing.NamedTuple):
    vertices: typing.List[int] = []
    
    @classmethod
    def load(cls, line):
        vertice_ids = []
        for i in line[line.find("f")+1:].strip().split():
            vertice_ids.append(np.int(i) - 1)
        return cls(vertice_ids)

    def to_triangles(self):
        if len(self.vertices) < 4:
            return [tuple(self.vertices)]
        all_tuples = []
        for i in range(1, len(self.vertices) - 1):
            all_tuples.append((self.vertices[0], self.vertices[i], self.vertices[i + 1]))
        return all_tuples
    
    def __repr__(self):
        return "f " + " ".join([str(x + 1) for x in self.vertice_ids])
        

class Mesh(typing.NamedTuple):
    vertices: typing.List[Vertex] = []
    faces: typing.List[Face] = []

    @classmethod
    def load(cls, filename):
        vertices = []
        faces = []
        with open(filename) as file:
            for line in file:
                line = line.strip()
                if len(line) < 1 or line[0] not in ("v", "f"):
                    continue
                if line.startswith("v"):
                    vertices.append(Vertex.load(line))
                if line.startswith("f"):
                    faces.append(Face.load(line))
        return  cls(vertices, faces)

    def to_lines(self):
        for v in self.vertices:
            yield str(v)
        for f in self.faces:
            yield str(f)

    def __repr__(self):
        return "Mesh with %s vertices and %s faces"%(len(self.vertices), len(self.faces)) 

    def vertices_tuples(self):
        return [tuple(x) for x in self.vertices]
    def get_coords(self):
        vertices = np.asarray(self.vertices_tuples())
        return [vertices[:, i] for i in (0, 1, 2)]
    def faces_tuples(self):
        return [tuple(x.vertices) for x in self.faces]

    def faces_triangles(self):
        all_triangles = []
        for f in self.faces:
            all_triangles.extend(f.to_triangles())
        return all_triangles