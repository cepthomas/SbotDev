
local M = {}

-- Only 4/4 time supported.
M.BEATS_PER_BAR = 4

-- Our resolution = 32nd note. aka midi DeltaTicksPerQuarterNote.
M.SUBBEATS_PER_BEAT = 8
M.SUBBEATS_PER_BAR = M.SUBBEATS_PER_BEAT * M.BEATS_PER_BAR

M.MAX_BAR = 1000
M.MAX_BEAT = M.MAX_BAR * M.BEATS_PER_BAR
M.MAX_TICK = M.MAX_BAR * M.SUBBEATS_PER_BAR


-----------------------------------------------------------------------------
function M.mt_to_tick(bar, beat, sub)
    local tick = bar * M.SUBBEATS_PER_BAR + beat * M.SUBBEATS_PER_BEAT + sub
    return tick
end

-----------------------------------------------------------------------------
function M.beats_to_tick(beats, sub)
    local tick = beats * M.SUBBEATS_PER_BEAT + sub
    return tick
end


-----------------------------------------------------------------------------
function M.tick_to_mt(tick)
    local bar = math.floor(tick / M.SUBBEATS_PER_BAR)
    local beat = math.floor(tick / M.SUBBEATS_PER_BEAT % M.BEATS_PER_BAR)
    local sub = math.floor(tick % M.SUBBEATS_PER_BEAT)
    return bar, beat, sub
end

-----------------------------------------------------------------------------
function M.tick_to_str(tick)
    local bar, beat, sub = M.tick_to_mt(tick)
    return string.format("%d.%d.%d", bar, beat, sub)
end


-- Do something with M. TODO-CFIG
-- return M
