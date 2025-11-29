# Teardown Twin Towers City

This repository ships a ready-to-play Teardown sandbox: a detailed Twin Towers-inspired plaza surrounded by city blocks, memorial pools, and skyline silhouettes. Everything needed to spawn the map is text-only—no binary assets or external tools required.

## Contents
- `mods/city-map/level.xml` — slim scene definition that boots the scripted spawn and lighting.
- `mods/city-map/main.lua` — unpacks the voxel asset from its Base64 text and spawns the full plaza and city skyline.
- `mods/city-map/vox/twin_towers.vox.b64` — text-encoded voxel data for the entire map (towers, plaza, streets, trees, surrounding buildings).

## Using the map in Teardown
1. Copy the `mods/city-map` directory into your Teardown `Documents/Teardown/mods` folder (or symlink it during development).
2. Launch Teardown and open the mod in the sandbox menu. The script automatically decodes the bundled Base64 file to `vox/twin_towers.vox` on first load, then spawns the city.
3. You start in the central plaza, framed by the twin towers, skybridge, memorial pools, tree rows, and multi-block skyline—ready to reshape without running any generators.

## Notes
- Because the voxel data is stored as text, there are no binary files in the repository. The mod writes the binary `.vox` file at runtime before spawning the scene.
- If you ever delete `vox/twin_towers.vox`, it will be recreated automatically on the next launch.
