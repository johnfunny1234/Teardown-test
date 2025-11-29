local hintTimer = 10

function init()
    SetFloat("level.weather", 0.1)
    SetFloat("level.gravity", 1)
end

function tick(dt)
    hintTimer = math.max(0, hintTimer - dt)
    if hintTimer > 0 then
        UiPush()
        UiTranslate(24, 24)
        UiFont("bold", 22)
        UiText("Explore the compact city. The cross streets form the center of the map.")
        UiTranslate(0, 26)
        UiText("Try reshaping buildings or paving new routes with your tools.")
        UiPop()
    end
end
