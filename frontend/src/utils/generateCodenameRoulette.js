const THEMES = {
    "🛰️ Space Explorer": {
        prefix: ["Star", "Void", "Nova", "Quantum", "Solar", "Galactic"],
        core: ["Ranger", "Sentinel", "Pilot", "Beacon", "Comet", "Cruiser"],
        suffix: ["01", "Zeta", "LX", "Prime", "Delta", "Eclipse"]
    },
    "🎮 80s Arcade": {
        prefix: ["Turbo", "Pixel", "Neon", "Mega", "Blitz", "Robo"],
        core: ["Blaster", "Runner", "Bomber", "Combo", "Strike", "Dash"],
        suffix: ["XP", "3000", "X", "99", "Deluxe", "Prime"]
    },
    "🧠 Cyber-Hacker": {
        prefix: ["Null", "Byte", "Crypto", "Syntax", "Root", "Echo"],
        core: ["Breaker", "Phantom", "Protocol", "Script", "Daemon", "Logic"],
        suffix: ["404", "0x7F", "V2", "Inject", "Core", "Σ"]
    },
    "🧛 Gothic Supernatural": {
        prefix: ["Ash", "Thorn", "Crimson", "Dark", "Raven", "Blood"],
        core: ["Warden", "Shade", "Grimoire", "Howler", "Fang", "Specter"],
        suffix: ["XIII", "Nocturne", "Bane", "Hex", "V", "Ω"]
    }
};

const themes = Object.values(THEMES);

export function generateCodename() {
    const getRandom = (list) => list[Math.floor(Math.random() * list.length)];
    const theme = getRandom(themes);

    const prefix = getRandom(theme.prefix);
    const core = getRandom(theme.core);
    const suffix = getRandom(theme.suffix);

    return `${prefix}${core}-${suffix}`;
}
