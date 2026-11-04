"""Validate the portable ROS description without a running ROS installation.

Run: python -m unittest discover -s tests -v
SPDX-License-Identifier: CERN-OHL-P-2.0
"""
from itertools import product
import hashlib
import json
import math
from pathlib import Path
import struct
import unittest
import xml.etree.ElementTree as ET

from catkin_pkg.package import parse_package
from urdf_parser_py.urdf import URDF
import xacro

REPO = Path(__file__).resolve().parents[1]
PACKAGE = REPO / 'ros/oh_my_mobilerobot_description'
VARIANTS = ('base', 'cargo', 'arm', 'display')


def numbers(text):
    return [float(x) for x in text.split()]


def identity():
    return [[float(i == j) for j in range(4)] for i in range(4)]


def multiply(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def transform(xyz=(0, 0, 0), rpy=(0, 0, 0)):
    roll, pitch, yaw = rpy
    cr, sr = math.cos(roll), math.sin(roll)
    cp, sp = math.cos(pitch), math.sin(pitch)
    cy, sy = math.cos(yaw), math.sin(yaw)
    return [[cy*cp, cy*sp*sr-sy*cr, cy*sp*cr+sy*sr, xyz[0]],
            [sy*cp, sy*sp*sr+cy*cr, sy*sp*cr-cy*sr, xyz[1]],
            [-sp, cp*sr, cp*cr, xyz[2]], [0, 0, 0, 1]]


def point(matrix, p):
    return [sum(matrix[i][k] * p[k] for k in range(3)) + matrix[i][3] for i in range(3)]


def link_poses(robot, positions=None):
    positions = positions or {}
    poses = {'base_footprint': identity()}
    remaining = list(robot.findall('joint'))
    while remaining:
        ready = [j for j in remaining if j.find('parent').get('link') in poses]
        if not ready:
            raise AssertionError('Disconnected or cyclic link tree')
        for joint in ready:
            origin = joint.find('origin')
            pose = transform(numbers(origin.get('xyz', '0 0 0')), numbers(origin.get('rpy', '0 0 0')))
            angle = positions.get(joint.get('name'), 0)
            if angle:
                axis = numbers(joint.find('axis').get('xyz'))
                # The model has +Y wheel and +Z swivel axes.
                pose = multiply(pose, transform(rpy=[angle*x for x in axis]))
            poses[joint.find('child').get('link')] = multiply(poses[joint.find('parent').get('link')], pose)
            remaining.remove(joint)
    return poses


def semantic(element):
    return (element.tag, tuple(sorted(element.attrib.items())),
            tuple(semantic(child) for child in element))


class RobotDescriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((PACKAGE / 'config/mesh_manifest.json').read_text(encoding='utf-8'))
        cls.robots = {v: ET.parse(PACKAGE / 'urdf' / f'{v}.urdf').getroot() for v in VARIANTS}

    def assertVector(self, actual, expected, tolerance=1e-8):
        self.assertEqual(len(actual), len(expected))
        for a, b in zip(actual, expected):
            self.assertAlmostEqual(a, b, delta=tolerance)

    def test_source_cad_provenance(self):
        for variant, source in self.manifest['sources'].items():
            with self.subTest(variant=variant):
                self.assertEqual(hashlib.sha256((REPO / source['cad']).read_bytes()).hexdigest(), source['sha256'])
                self.assertLess(source['mesh_bbox_max_error_mm'], .05)
        self.assertEqual(self.manifest['units'], 'metres')

    def test_stl_integrity_and_scale(self):
        referenced = set()
        for materials in self.manifest['meshes'].values():
            for record in materials.values():
                path = PACKAGE / record['path']
                referenced.add(path)
                data = path.read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), record['sha256'], path)
                count, = struct.unpack_from('<I', data, 80)
                self.assertEqual(count, record['triangles'])
                self.assertEqual(len(data), 84 + 50 * count, path)
                self.assertGreater(count, 0)
                low, high = [math.inf] * 3, [-math.inf] * 3
                for triangle in struct.iter_unpack('<12fH', data[84:]):
                    self.assertTrue(all(math.isfinite(x) for x in triangle[:12]), path)
                    self.assertAlmostEqual(sum(x*x for x in triangle[:3]), 1, delta=2e-5)
                    for i in range(3):
                        low[i] = min(low[i], *triangle[3+i:12:3])
                        high[i] = max(high[i], *triangle[3+i:12:3])
                self.assertVector(low, record['bbox_m']['min'], 2e-7)
                self.assertVector(high, record['bbox_m']['max'], 2e-7)
                self.assertLess(max(abs(x) for x in low + high), 2, 'Mesh appears to use mm instead of metres')
        self.assertEqual(referenced, set((PACKAGE / 'meshes/visual').rglob('*.stl')))

    def test_urdf_trees_and_package_uris(self):
        for variant, robot in self.robots.items():
            with self.subTest(variant=variant):
                parsed = URDF.from_xml_string(ET.tostring(robot, encoding='unicode'))
                self.assertEqual(parsed.get_root(), 'base_footprint')
                self.assertEqual(len(parsed.links), 12 if variant == 'base' else 13)
                self.assertEqual(len(parsed.joints), len(parsed.links) - 1)
                self.assertEqual(len(link_poses(robot)), len(parsed.links))
                self.assertEqual(sum(j.type == 'continuous' for j in parsed.joints), 6)
                for mesh in robot.findall('.//mesh'):
                    self.assertVector(numbers(mesh.get('scale')), [1, 1, 1])
                    prefix = 'package://oh_my_mobilerobot_description/'
                    self.assertTrue(mesh.get('filename').startswith(prefix))
                    self.assertTrue((PACKAGE / mesh.get('filename')[len(prefix):]).is_file())
                for material in robot.findall('.//visual/material'):
                    self.assertIsNotNone(robot.find(f"material[@name='{material.get('name')}']/color"))

    def test_assembly_bounds_match_native_cad(self):
        for variant, robot in self.robots.items():
            poses = link_poses(robot)
            points = []
            for link in robot.findall('link'):
                for visual in link.findall('visual'):
                    filename = visual.find('geometry/mesh').get('filename').split('/', 3)[-1]
                    record = next(r for materials in self.manifest['meshes'].values()
                                  for r in materials.values() if r['path'] == filename)
                    box = record['bbox_m']
                    for corner in product(*zip(box['min'], box['max'])):
                        points.append(point(poses[link.get('name')], corner))
            actual = [[fn(p[i] for p in points) for i in range(3)] for fn in (min, max)]
            native = self.manifest['sources'][variant]['bbox_cad_mm']
            expected = [[(60-native['max'][1])*.001, (native['min'][0]-220)*.001, (native['min'][2]+101)*.001],
                        [(60-native['min'][1])*.001, (native['max'][0]-220)*.001, (native['max'][2]+101)*.001]]
            self.assertVector(actual[0], expected[0], .00005)
            self.assertVector(actual[1], expected[1], .00005)

    def test_wheel_positions_ground_contact_and_handedness(self):
        robot = self.robots['base']
        poses = link_poses(robot)
        self.assertVector(point(poses['base_link'], [0, 0, 0]), [0, 0, .101])
        self.assertVector(point(poses['left_wheel_link'], [0, 0, 0]), [0, .240, .068])
        self.assertVector(point(poses['right_wheel_link'], [0, 0, 0]), [0, -.240, .068])
        for side, y in [('left', .155), ('right', -.155)]:
            self.assertVector(point(poses[side+'_caster_wheel_link'], [0, 0, 0]), [-.34175, y, .038])
            for name in [side+'_wheel_link', side+'_caster_wheel_link']:
                radius = float(robot.find(f"link[@name='{name}']/collision/geometry/cylinder").get('radius'))
                self.assertAlmostEqual(poses[name][2][3] - radius, 0, delta=1e-9)
        # +90 degree wheel rotation sends the original bottom point toward the rear.
        moved = link_poses(robot, {'left_wheel_joint': math.pi/2})
        self.assertVector(point(moved['left_wheel_link'], [0, 0, -.068]), [-.068, .240, .068])

    def test_caster_swivel_keeps_trail_and_ground_height(self):
        moved = link_poses(self.robots['base'], {'left_caster_swivel_joint': math.pi/2})
        self.assertVector(point(moved['left_caster_wheel_link'], [0, 0, 0]), [-.30775, .121, .038])
        self.assertVector(point(moved['right_caster_wheel_link'], [0, 0, 0]), [-.34175, -.155, .038])

    def test_sensor_axes(self):
        poses = link_poses(self.robots['base'])
        optical = poses['camera_optical_frame']
        origin = point(optical, [0, 0, 0])
        for local, expected in [([1, 0, 0], [0, -1, 0]), ([0, 1, 0], [0, 0, -1]), ([0, 0, 1], [1, 0, 0])]:
            self.assertVector([a-b for a, b in zip(point(optical, local), origin)], expected)
        self.assertVector(point(poses['laser_frame'], [0, 0, 0]), [-.140, 0, .2743])

    def test_xacro_variants_and_prefix(self):
        path = PACKAGE / 'urdf/oh_my_mobilerobot.urdf.xacro'
        for variant in VARIANTS:
            plain = ET.fromstring(xacro.process_file(str(path), mappings={'variant': variant}).toxml())
            self.assertEqual(semantic(plain), semantic(self.robots[variant]))
            prefixed = ET.fromstring(xacro.process_file(str(path), mappings={'variant': variant, 'prefix': 'robot1_'}).toxml())
            for node in prefixed.findall('link') + prefixed.findall('joint') + prefixed.findall('material'):
                self.assertTrue(node.get('name').startswith('robot1_'))
            for node in prefixed.findall('joint/parent') + prefixed.findall('joint/child'):
                self.assertTrue(node.get('link').startswith('robot1_'))

    def test_extension_is_fixed_to_unchanged_base(self):
        base = self.robots['base']
        for variant in VARIANTS[1:]:
            robot = self.robots[variant]
            for node in base.findall('link') + base.findall('joint'):
                self.assertEqual(semantic(node), semantic(robot.find(f"{node.tag}[@name='{node.get('name')}']")))
            self.assertEqual(robot.find("joint[@name='module_joint']").get('type'), 'fixed')
            self.assertIsNone(robot.find("link[@name='module_link']/collision"))

    def test_conditional_ros_package_and_launch_files(self):
        for version, build_type in [('1', 'catkin'), ('2', 'ament_cmake')]:
            package = parse_package(str(PACKAGE), warnings=[])
            package.evaluate_conditions({'ROS_VERSION': version})
            self.assertEqual(package.get_build_type(), build_type)
            active = [d.name for d in package.buildtool_depends if d.evaluated_condition is not False]
            self.assertEqual(active, [build_type])
        ros1 = ET.parse(PACKAGE / 'launch/display.launch').getroot()
        self.assertEqual(ros1.tag, 'launch')
        self.assertEqual(ros1.find("param[@name='robot_description']").get('textfile'), '$(arg model)')
        path = PACKAGE / 'launch/display.launch.py'
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        self.assertEqual((PACKAGE / 'LICENSE').read_bytes(), (REPO / 'LICENSE').read_bytes())
        for path in (PACKAGE / 'urdf').glob('*'):
            content = path.read_text(encoding='utf-8')
            self.assertNotIn('C:/Users/', content)
            self.assertNotIn('/home/', content)


if __name__ == '__main__':
    unittest.main()
