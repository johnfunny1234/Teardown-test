import struct
from pathlib import Path

WIDTH, HEIGHT, DEPTH = 64, 32, 64


def add_box(voxels, x0, x1, y0, y1, z0, z1, color):
    for x in range(x0, x1):
        for y in range(y0, y1):
            for z in range(z0, z1):
                voxels.append((x, y, z, color))


def build_city_layout():
    voxels = []

    # Base ground layer
    add_box(voxels, 0, WIDTH, 0, 1, 0, DEPTH, 1)

    # Roads forming a cross through the map
    add_box(voxels, WIDTH // 2 - 2, WIDTH // 2 + 2, 0, 1, 0, DEPTH, 2)
    add_box(voxels, 0, WIDTH, 0, 1, DEPTH // 2 - 2, DEPTH // 2 + 2, 2)

    # Sidewalks alongside the roads
    add_box(voxels, WIDTH // 2 - 3, WIDTH // 2 - 2, 1, 2, 0, DEPTH, 3)
    add_box(voxels, WIDTH // 2 + 2, WIDTH // 2 + 3, 1, 2, 0, DEPTH, 3)
    add_box(voxels, 0, WIDTH, 1, 2, DEPTH // 2 - 3, DEPTH // 2 - 2, 3)
    add_box(voxels, 0, WIDTH, 1, 2, DEPTH // 2 + 2, DEPTH // 2 + 3, 3)

    # Parks in the corners
    add_box(voxels, 4, 12, 1, 2, DEPTH - 12, DEPTH - 4, 4)
    add_box(voxels, WIDTH - 12, WIDTH - 4, 1, 2, 4, 12, 4)

    # Buildings of varied heights
    add_box(voxels, 8, 18, 1, 12, 8, 18, 5)
    add_box(voxels, 22, 32, 1, 16, 12, 22, 6)
    add_box(voxels, 40, 52, 1, 10, 10, 22, 7)
    add_box(voxels, 12, 20, 1, 14, 36, 48, 8)
    add_box(voxels, 36, 48, 1, 18, 38, 52, 9)

    # Rooftop details on a couple of buildings
    add_box(voxels, 10, 16, 12, 14, 10, 16, 10)
    add_box(voxels, 24, 30, 16, 18, 16, 20, 11)

    return voxels


def build_palette():
    palette = [(0, 0, 0, 0)]
    palette.append((110, 180, 110, 255))  # 1 ground
    palette.append((40, 40, 40, 255))     # 2 road asphalt
    palette.append((170, 170, 170, 255))  # 3 sidewalk
    palette.append((50, 160, 90, 255))    # 4 park
    palette.append((200, 210, 220, 255))  # 5 building 1
    palette.append((180, 200, 220, 255))  # 6 building 2
    palette.append((170, 170, 195, 255))  # 7 building 3
    palette.append((210, 190, 170, 255))  # 8 building 4
    palette.append((220, 200, 150, 255))  # 9 building 5
    palette.append((255, 120, 80, 255))   # 10 rooftop accent 1
    palette.append((240, 200, 80, 255))   # 11 rooftop accent 2

    # Fill the rest of the palette with a neutral grey
    while len(palette) < 256:
        palette.append((128, 128, 128, 255))
    return palette


def write_chunk(fid, chunk_id, content, children=b""):
    fid.write(chunk_id)
    fid.write(struct.pack("<II", len(content), len(children)))
    fid.write(content)
    fid.write(children)


def write_vox_file(path: Path, voxels, palette):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        # Header
        f.write(b"VOX ")
        f.write(struct.pack("<I", 150))

        # SIZE chunk
        size_content = struct.pack("<III", WIDTH, HEIGHT, DEPTH)
        size_chunk = b""
        size_buffer = struct.pack("<II", len(size_content), 0) + size_content
        size_chunk = b"SIZE" + size_buffer

        # XYZI chunk
        xyzi_content = struct.pack("<I", len(voxels))
        for x, y, z, c in voxels:
            xyzi_content += struct.pack("<BBBB", x, y, z, c)
        xyzi_buffer = struct.pack("<II", len(xyzi_content), 0) + xyzi_content
        xyzi_chunk = b"XYZI" + xyzi_buffer

        # RGBA chunk
        rgba_content = b"".join(struct.pack("<BBBB", *rgba) for rgba in palette)
        rgba_buffer = struct.pack("<II", len(rgba_content), 0) + rgba_content
        rgba_chunk = b"RGBA" + rgba_buffer

        children = size_chunk + xyzi_chunk + rgba_chunk

        # MAIN chunk header with children length
        f.write(b"MAIN")
        f.write(struct.pack("<II", 0, len(children)))
        f.write(children)


def main():
    voxels = build_city_layout()
    palette = build_palette()
    target = Path(__file__).parent.parent / "mods" / "city-map" / "vox" / "city.vox"
    write_vox_file(target, voxels, palette)
    print(f"Wrote {target} with {len(voxels)} voxels")


if __name__ == "__main__":
    main()
