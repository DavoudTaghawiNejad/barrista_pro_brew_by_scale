import machine


def substitute_coffee_name_with_reset_cause(coffee_name, filter=[2, 3, 4, 5, 6]):
    reset_cause = machine.reset_cause()

    # Map integer return values to human-readable strings
    reset_cause_map = {
        0: "SOFT_RESET",
        1: "HARD_RESET",
        2: "WDT_RESET",
        3: "BROWN_OUT_RESET",
        4: "EXT_RESET\nDEEPSLEEP_RESET",
        5: "PANIC_RESET",
        6: "SWDT_RESET"
    }

    if reset_cause in filter:
        return coffee_name
    else:
        return reset_cause_map.get(reset_cause, str(reset_cause))
