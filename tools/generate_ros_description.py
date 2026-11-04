#!/usr/bin/env python3
"""Build ROS visual meshes and URDFs from the repository's SolidCraft designs.

Requires Python 3.9+ and xacro. Native export uses solidcraft-cli's stdio MCP mode.
SPDX-License-Identifier: CERN-OHL-P-2.0
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
import math
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import xml.etree.ElementTree as ET

REPO = Path(__file__).resolve().parents[1]
PACKAGE = REPO / 'ros/oh_my_mobilerobot_description'
XACRO_NS = 'http://www.ros.org/wiki/xacro'
ET.register_namespace('xacro', XACRO_NS)


class SolidCraftMCP:
    """A private read/export session with access limited to input and output roots."""

    def __init__(self, executable, source, output):
        command = [str(executable), 'mcp', '--headless', '--allow-path', str(REPO),
                   '--allow-path', str(output), '--in', str(source)]
        options = {'creationflags': subprocess.CREATE_NO_WINDOW} if hasattr(subprocess, 'CREATE_NO_WINDOW') else {}
        self.stderr = tempfile.TemporaryFile(mode='w+t', encoding='utf-8')
        self.process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=self.stderr, text=True, encoding='utf-8', **options)
        self.serial = 0
        self.rpc('initialize', {'protocolVersion': '2024-11-05', 'capabilities': {},
                              'clientInfo': {'name': 'oh_my_mobilerobot_description', 'version': '1.0'}})
        self.process.stdin.write(json.dumps({'jsonrpc': '2.0', 'method': 'notifications/initialized'}) + '\n')
        self.process.stdin.flush()

    def rpc(self, method, params):
        self.serial += 1
        self.process.stdin.write(json.dumps({'jsonrpc': '2.0', 'id': self.serial,
                                           'method': method, 'params': params}) + '\n')
        self.process.stdin.flush()
        for line in self.process.stdout:
            reply = json.loads(line)
            if reply.get('id') == self.serial:
                if 'error' in reply:
                    raise RuntimeError(reply['error'])
                return reply['result']
        self.stderr.seek(0)
        raise RuntimeError('SolidCraft export session ended: ' + self.stderr.read()[-2000:])

    def tool(self, name, arguments):
        reply = self.rpc('tools/call', {'name': name, 'arguments': arguments})
        text = '\n'.join(c['text'] for c in reply.get('content', []) if c['type'] == 'text')
        if reply.get('isError'):
            raise RuntimeError(text)
        return json.loads(text)

    def close(self):
        self.process.stdin.close()
        try:
            self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            self.process.wait(timeout=10)
        self.stderr.close()


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_bytes((json.dumps(value, indent=2) + '\n').encode('utf-8'))


def export_native(config, output, executable):
    for variant, relative in config['sources'].items():
        source = REPO / relative
        before = sha256(source)
        session = SolidCraftMCP(executable, source, output)
        try:
            state = session.tool('inspect_design', {'measure': True, 'sketches': False, 'joints': False})
            bodies = [b for b in state['bodies'] if b['visible']]
            if any(not b['closed'] for b in bodies) or any(f.get('error') for f in state['timeline']):
                raise RuntimeError(f'{variant}: native CAD contains a failed feature or open body')
            session.tool('export', {'path': str(output / f'{variant}.obj'), 'format': 'obj',
                                    'bodies': [b['name'] for b in bodies]})
            write_json(output / f'{variant}.json', {'source_sha256': before, 'bodies': bodies})
        finally:
            session.close()
        if sha256(source) != before:
            raise RuntimeError(f'{variant}: input CAD changed during export')
        print(f'Exported {variant}: {len(bodies)} visible bodies', flush=True)


def read_obj(path):
    vertices = []
    bodies = defaultdict(list)
    current = None
    with path.open(encoding='utf-8') as stream:
        for line in stream:
            if line.startswith('o '):
                current = line[2:].strip()
            elif line.startswith('v '):
                vertices.append(tuple(float(x) for x in line.split()[1:4]))
            elif line.startswith('f '):
                if current is None:
                    raise ValueError('OBJ face has no source body')
                indices = [int(token.split('/')[0]) for token in line.split()[1:]]
                points = [vertices[i - 1 if i > 0 else len(vertices) + i] for i in indices]
                for index in range(1, len(points) - 1):
                    bodies[current].append((points[0], points[index], points[index + 1]))
    return dict(bodies)


def bounds(triangles):
    points = (point for triangle in triangles for point in triangle)
    first = next(points)
    low, high = list(first), list(first)
    for point in points:
        for i in range(3):
            low[i] = min(low[i], point[i])
            high[i] = max(high[i], point[i])
    return {'min': low, 'max': high}


def combine_bounds(items):
    return {'min': [min(b['min'][i] for b in items) for i in range(3)],
            'max': [max(b['max'][i] for b in items) for i in range(3)]}


def to_local(point, origin):
    # Right-handed +90 degree yaw: CAD -Y -> ROS +X, CAD +X -> ROS +Y.
    return ((origin[1] - point[1]) * .001,
            (point[0] - origin[0]) * .001,
            (point[2] - origin[2]) * .001)


def body_link(name):
    for native, side in [('DW_R_', 'left'), ('DW_L_', 'right')]:
        if name.startswith(native) and name[len(native):] in ['Tyre', 'Rim', 'Coupler', 'Shaft']:
            return f'{side}_wheel_link'
    for native, side in [('CW_R_', 'left'), ('CW_L_', 'right')]:
        if name.startswith(native):
            suffix = name[len(native):]
            if suffix in ['Tyre', 'Hub']:
                return f'{side}_caster_wheel_link'
            if suffix in ['Swivel', 'Kingpin', 'Fork', 'Axle', 'Axle_Head', 'Axle_Nut']:
                return f'{side}_caster_swivel_link'
    if name.startswith('REF_A2M12_'):
        return 'lidar_link'
    if name == 'REF_D435i_Envelope' or name.startswith('REF_Optic_') or name.startswith('REF_Example_USB_') or name.startswith('REF_Example_Straight_USB_'):
        return 'camera_link'
    return 'base_link'


def write_stl(path, triangles):
    path.parent.mkdir(parents=True, exist_ok=True)
    records = bytearray()
    count = 0
    for a, b, c in triangles:
        u = tuple(b[i] - a[i] for i in range(3))
        v = tuple(c[i] - a[i] for i in range(3))
        normal = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
        length = math.sqrt(sum(x * x for x in normal))
        if length < 1e-20:
            continue
        normal = tuple(x / length for x in normal)
        records.extend(struct.pack('<12fH', *normal, *a, *b, *c, 0))
        count += 1
    header = b'Oh My MobileRobot ROS visual mesh; coordinates in metres'.ljust(80, b' ')
    path.write_bytes(header + struct.pack('<I', count) + records)
    return {'triangles': count, 'sha256': sha256(path), 'bbox_m': bounds(triangles)}


def scalar(value):
    return f'{value:.10g}' if abs(value) > 1e-12 else '0'


def vector(values):
    return ' '.join(scalar(x) for x in values)


def prefixed(name):
    return '${prefix}' + name


def add_joint(root, name, parent, child, xyz, joint_type='fixed', axis=None, rpy=None):
    joint = ET.SubElement(root, 'joint', name=prefixed(name), type=joint_type)
    ET.SubElement(joint, 'parent', link=prefixed(parent))
    ET.SubElement(joint, 'child', link=prefixed(child))
    ET.SubElement(joint, 'origin', xyz=vector(xyz), rpy=vector(rpy or [0, 0, 0]))
    if axis is not None:
        ET.SubElement(joint, 'axis', xyz=vector(axis))


def add_visual_link(root, name, group, groups, package_name, wheel=None, collisions=True):
    link = ET.SubElement(root, 'link', name=prefixed(name))
    for material, record in sorted(groups[group].items()):
        visual = ET.SubElement(link, 'visual', name=prefixed(name + '_' + material))
        geometry = ET.SubElement(visual, 'geometry')
        ET.SubElement(geometry, 'mesh', filename=f'package://{package_name}/{record["path"]}', scale='1 1 1')
        ET.SubElement(visual, 'material', name=prefixed('color_' + material))
    if collisions:
        collision = ET.SubElement(link, 'collision')
        geometry = ET.SubElement(collision, 'geometry')
        if wheel is not None:
            ET.SubElement(collision, 'origin', xyz='0 0 0', rpy=vector([math.pi / 2, 0, 0]))
            ET.SubElement(geometry, 'cylinder', radius=scalar(wheel[0]), length=scalar(wheel[1]))
        else:
            box = combine_bounds([r['bbox_m'] for r in groups[group].values()])
            center = [(box['min'][i] + box['max'][i]) / 2 for i in range(3)]
            size = [box['max'][i] - box['min'][i] for i in range(3)]
            ET.SubElement(collision, 'origin', xyz=vector(center), rpy='0 0 0')
            ET.SubElement(geometry, 'box', size=vector(size))


def make_xacro(config, groups):
    root = ET.Element('robot', name='oh_my_mobilerobot')
    root.append(ET.Comment('Generated by tools/generate_ros_description.py; SPDX-License-Identifier: CERN-OHL-P-2.0'))
    ET.SubElement(root, f'{{{XACRO_NS}}}arg', name='variant', default='base')
    ET.SubElement(root, f'{{{XACRO_NS}}}arg', name='prefix', default='')
    ET.SubElement(root, f'{{{XACRO_NS}}}property', name='variant', value='$(arg variant)')
    ET.SubElement(root, f'{{{XACRO_NS}}}property', name='prefix', value='$(arg prefix)')
    for material, color in sorted(config['materials'].items()):
        node = ET.SubElement(root, 'material', name=prefixed('color_' + material))
        rgba = [int(color[i:i + 2], 16) / 255 for i in [1, 3, 5]] + [1]
        ET.SubElement(node, 'color', rgba=vector(rgba))
    ET.SubElement(root, 'link', name=prefixed('base_footprint'))
    frames = config['frames_cad_mm']
    wheel = config['wheel_geometry_m']
    for link in ['base_link', 'left_wheel_link', 'right_wheel_link',
                 'left_caster_swivel_link', 'right_caster_swivel_link',
                 'left_caster_wheel_link', 'right_caster_wheel_link', 'lidar_link', 'camera_link']:
        shape = None
        if link in ['left_wheel_link', 'right_wheel_link']:
            shape = (wheel['drive_radius'], wheel['drive_width'])
        elif link.endswith('caster_wheel_link'):
            shape = (wheel['caster_radius'], wheel['caster_width'])
        add_visual_link(root, link, link, groups, config['package'], wheel=shape)
    ET.SubElement(root, 'link', name=prefixed('laser_frame'))
    ET.SubElement(root, 'link', name=prefixed('camera_optical_frame'))
    add_joint(root, 'base_footprint_joint', 'base_footprint', 'base_link',
              [0, 0, config['base_footprint_height_m']])
    for side in ['left', 'right']:
        add_joint(root, f'{side}_wheel_joint', 'base_link', f'{side}_wheel_link',
                  to_local(frames[f'{side}_wheel_link'], frames['base_link']), 'continuous', [0, 1, 0])
        add_joint(root, f'{side}_caster_swivel_joint', 'base_link', f'{side}_caster_swivel_link',
                  to_local(frames[f'{side}_caster_swivel_link'], frames['base_link']), 'continuous', [0, 0, 1])
        add_joint(root, f'{side}_caster_wheel_joint', f'{side}_caster_swivel_link', f'{side}_caster_wheel_link',
                  to_local(frames[f'{side}_caster_wheel_link'], frames[f'{side}_caster_swivel_link']), 'continuous', [0, 1, 0])
    add_joint(root, 'lidar_joint', 'base_link', 'lidar_link', to_local(frames['lidar_link'], frames['base_link']))
    add_joint(root, 'laser_frame_joint', 'lidar_link', 'laser_frame', to_local(frames['laser_frame'], frames['lidar_link']))
    add_joint(root, 'camera_joint', 'base_link', 'camera_link', to_local(frames['camera_link'], frames['base_link']))
    add_joint(root, 'camera_optical_joint', 'camera_link', 'camera_optical_frame', [0, 0, 0], rpy=[-math.pi / 2, 0, -math.pi / 2])
    for variant in ['cargo', 'arm', 'display']:
        condition = ET.SubElement(root, f'{{{XACRO_NS}}}if', value="${variant == '" + variant + "'}")
        add_visual_link(condition, 'module_link', variant + '_module', groups, config['package'], collisions=False)
        add_joint(condition, 'module_joint', 'base_link', 'module_link', to_local(frames['module_link'], frames['base_link']))
    ET.indent(root, space='  ')
    path = PACKAGE / 'urdf/oh_my_mobilerobot.urdf.xacro'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(ET.tostring(root, encoding='utf-8', xml_declaration=True) + b'\n')
    import xacro
    for variant in ['base', 'cargo', 'arm', 'display']:
        expanded = xacro.process_file(str(path), mappings={'variant': variant, 'prefix': ''})
        # Strip xacro's absolute-source banner before publishing generated assets.
        robot = ET.fromstring(expanded.toxml())
        ET.indent(robot, space='  ')
        target = path.parent / f'{variant}.urdf'
        target.write_bytes(ET.tostring(robot, encoding='utf-8', xml_declaration=True) + b'\n')


def build(config, native_dir):
    sources = {}
    groups = defaultdict(lambda: defaultdict(list))
    base_names = None
    base_body_records = None
    for variant, source in config['sources'].items():
        native = json.loads((native_dir / f'{variant}.json').read_text(encoding='utf-8'))
        if sha256(REPO / source) != native['source_sha256']:
            raise ValueError(f'{variant}: stale native export; export the modified CAD again')
        source_bodies = {b['name']: b for b in native['bodies']}
        bodies = read_obj(native_dir / f'{variant}.obj')
        if set(bodies) != set(source_bodies):
            raise ValueError(f'{variant}: mesh and native body sets differ')
        max_error = 0
        for name, triangles in bodies.items():
            bb = bounds(triangles)
            max_error = max(max_error, *(abs(bb[side][i] - source_bodies[name]['bbox'][side][i])
                                         for side in ['min', 'max'] for i in range(3)))
        if max_error > .05:
            raise ValueError(f'{variant}: mesh/native bounds differ by {max_error} mm')
        sources[variant] = {'cad': source, 'sha256': native['source_sha256'],
                            'visible_bodies': len(bodies), 'mesh_bbox_max_error_mm': max_error,
                            'bbox_cad_mm': combine_bounds([b['bbox'] for b in source_bodies.values()])}
        if variant == 'base':
            base_names = set(bodies)
            base_body_records = source_bodies
        elif not base_names.issubset(bodies):
            raise ValueError(f'{variant}: extension is missing base bodies')
        if variant != 'base':
            for name in base_names:
                for side in ['min', 'max']:
                    if max(abs(source_bodies[name]['bbox'][side][i] - base_body_records[name]['bbox'][side][i]) for i in range(3)) > .001:
                        raise ValueError(f'{variant}: shared base body {name} has changed')
        selected = bodies if variant == 'base' else {n: t for n, t in bodies.items() if n not in base_names}
        for name, triangles in selected.items():
            group = body_link(name) if variant == 'base' else variant + '_module'
            frame = group if variant == 'base' else 'module_link'
            origin = config['frames_cad_mm'][frame]
            material = config['body_categories'].get(name, 'metal')
            groups[group][material].extend(tuple(to_local(p, origin) for p in tri) for tri in triangles)
        print(f'Converted {variant}: {len(selected)} CAD bodies', flush=True)
    mesh_records = {}
    for group, materials in sorted(groups.items()):
        mesh_records[group] = {}
        for material, triangles in sorted(materials.items()):
            relative = f'meshes/visual/{group}/{material}.stl'
            record = write_stl(PACKAGE / relative, triangles)
            mesh_records[group][material] = {'path': relative, **record}
    make_xacro(config, mesh_records)
    conversion = {'cad_origin_mm': config['frames_cad_mm']['base_link'],
                  'rotation_rpy_rad': [0, 0, math.pi / 2], 'scale': .001,
                  'base_footprint_offset_m': config['base_footprint_height_m']}
    manifest = {'units': 'metres', 'package': config['package'], 'sources': sources,
                'cad_to_ros': conversion, 'frames_cad_mm': config['frames_cad_mm'],
                'wheel_geometry_m': config['wheel_geometry_m'], 'materials': config['materials'],
                'meshes': mesh_records}
    write_json(PACKAGE / 'config/mesh_manifest.json', manifest)
    mesh_count = sum(len(m) for m in mesh_records.values())
    print(f'Generated {mesh_count} metre-scale visual meshes, one Xacro, and four URDF variants.', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--solidcraft', help='Path to solidcraft-cli; otherwise use PATH')
    parser.add_argument('--native-dir', type=Path, help='Reuse a directory of matching native OBJ/JSON exports')
    args = parser.parse_args()
    config = json.loads((PACKAGE / 'config/cad_mapping.json').read_text(encoding='utf-8'))
    if args.native_dir:
        build(config, args.native_dir.resolve())
    else:
        executable = args.solidcraft or shutil.which('solidcraft-cli')
        if not executable:
            parser.error('Pass --solidcraft PATH or put solidcraft-cli on PATH')
        with tempfile.TemporaryDirectory(prefix='oh_my_mobilerobot_') as directory:
            native_dir = Path(directory)
            export_native(config, native_dir, executable)
            build(config, native_dir)


if __name__ == '__main__':
    main()
