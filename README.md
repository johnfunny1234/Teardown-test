# Teardown City Map

This repository contains a compact custom city map for Teardown along with a small tool that procedurally generates the voxel asset used by the level.

## Contents
- `mods/city-map/level.xml` — scene layout pointing to the voxel map and a simple lighting setup.
- `mods/city-map/main.lua` — lightweight script that shows a short hint when the level starts.
- `mods/city-map/vox/` — output folder for the generated `city.vox` map that includes roads, parks, and several mid-rise buildings. A `.gitkeep` placeholder is committed because the binary voxel file itself is generated.
- `tools/generate_city_vox.py` — utility for regenerating the voxel asset if you want to tweak the layout or palette.

## Regenerating the voxel map
Binary assets are not stored in this repository. If you make changes to the layout logic or want to experiment with different palettes, run:

```bash
python tools/generate_city_vox.py
```

The script writes `mods/city-map/vox/city.vox` (ignored by git) and reports how many voxels are included.

## Using the map in Teardown
1. Run the generator above to create `mods/city-map/vox/city.vox`.
2. Copy the `mods/city-map` directory into your Teardown `Documents/Teardown/mods` folder (or symlink it during development).
3. Launch Teardown and open the mod in the sandbox menu. The player spawn is centered at the intersection of two main streets.
4. Use the provided hint text as guidance: the parks occupy opposite corners and buildings of varying heights surround the cross streets.

Feel free to customize building heights, palette colors, or spawn position in `tools/generate_city_vox.py` and `mods/city-map/level.xml` to create different city moods.
