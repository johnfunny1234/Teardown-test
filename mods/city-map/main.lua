local hintTimer = 16
local voxPath = "mods/city-map/vox/twin_towers.vox"
local voxBase64Path = "mods/city-map/vox/twin_towers.vox.b64"

local towerSpawned = false
local towerBody = nil

local function ensure_dir(path)
    local dir = path:match("^(.*)/[^/]+$")
    if dir then os.execute("mkdir -p " .. dir) end
end

local function base64_decode(data)
    local b = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    data = data:gsub("[^" .. b .. "=]", "")
    local out = {}
    local n = 0
    for i = 1, #data, 4 do
        local a = b:find(data:sub(i, i), 1, true)
        local c = b:find(data:sub(i + 1, i + 1), 1, true)
        local d = b:find(data:sub(i + 2, i + 2), 1, true)
        local e = b:find(data:sub(i + 3, i + 3), 1, true)
        if not a or not c then break end
        a, c = a - 1, c - 1
        d = d and (d - 1) or 0
        e = e and (e - 1) or 0
        local byte1 = (a << 2) | (c >> 4)
        out[#out + 1] = string.char(byte1)
        if data:sub(i + 2, i + 2) ~= '=' then
            local byte2 = ((c & 15) << 4) | (d >> 2)
            out[#out + 1] = string.char(byte2)
        end
        if data:sub(i + 3, i + 3) ~= '=' then
            local byte3 = ((d & 3) << 6) | e
            out[#out + 1] = string.char(byte3)
        end
        n = n + 3
    end
    return table.concat(out)
end

local function ensure_vox()
    local f = io.open(voxPath, "rb")
    if f then
        f:close()
        return
    end

    local b64 = assert(io.open(voxBase64Path, "rb")):read("*a")
    local raw = base64_decode(b64)
    ensure_dir(voxPath)
    local out = assert(io.open(voxPath, "wb"))
    out:write(raw)
    out:close()
end

local function spawn_city()
    if towerSpawned then return end
    towerSpawned = true
    ensure_vox()
    towerBody = Spawn("vox/twin_towers.vox", Transform(Vec(0, 0, 0)))
end

function init()
    SetFloat("level.weather", 0.12)
    SetFloat("level.gravity", 1)
    spawn_city()
    SetPlayerTransform(Transform(Vec(96, 6, 96)))
end

function tick(dt)
    if not towerSpawned then
        spawn_city()
    end

    hintTimer = math.max(0, hintTimer - dt)
    if hintTimer > 0 then
        UiPush()
        UiTranslate(24, 24)
        UiFont("bold", 22)
        UiText("Twin Towers City: detailed towers, plaza pools, skyline blocks, and lit avenues ready to reshape.")
        UiTranslate(0, 26)
        UiText("Files stay text-only: the voxel asset unpacks automatically, no external tools needed.")
        UiPop()
    end
end
