from app.schemas import enums

stage_level_t = {
    1: "أول",
    2: "ثاني",
    3: "ثالث",
    4: "رابع",
    5: "خامس",
}

stage_shift_t = {
    enums.CollageShifts.morning: "صباحي",
    enums.CollageShifts.evening: "مسائي",
}
