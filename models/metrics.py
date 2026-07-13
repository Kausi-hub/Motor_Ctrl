# models/metrics.py

import numpy as np


# ==========================================================
# OVERSHOOT
# ==========================================================

def calculate_overshoot(
    response,
    setpoint
):
    """
    Overshoot (%)

    OS =
    ((Peak - Setpoint) / Setpoint) * 100
    """

    if len(response) == 0:
        return 0.0

    peak = max(response)

    if setpoint == 0:
        return 0.0

    overshoot = max(
        0.0,
        ((peak - setpoint) / abs(setpoint))
        * 100.0
    )

    return round(
        overshoot,
        3
    )


# ==========================================================
# PEAK VALUE
# ==========================================================

def calculate_peak_value(
    response
):
    """
    Maximum response value.
    """

    if len(response) == 0:
        return 0.0

    return round(
        max(response),
        3
    )


# ==========================================================
# STEADY STATE ERROR
# ==========================================================

def calculate_steady_state_error(
    response,
    setpoint
):
    """
    Final setpoint tracking error.
    """

    if len(response) == 0:
        return setpoint

    final_value = response[-1]

    error = (
        setpoint
        - final_value
    )

    return round(
        error,
        3
    )


# ==========================================================
# RISE TIME
# ==========================================================

def calculate_rise_time(
    time_data,
    response,
    setpoint
):
    """
    Rise Time:
    Time from 10% to 90% of setpoint.
    """

    if (
        len(time_data) == 0
        or len(response) == 0
    ):
        return None

    lower = 0.1 * setpoint
    upper = 0.9 * setpoint

    t10 = None
    t90 = None

    for t, y in zip(
        time_data,
        response
    ):

        if (
            t10 is None
            and y >= lower
        ):
            t10 = t

        if (
            t90 is None
            and y >= upper
        ):
            t90 = t
            break

    if (
        t10 is not None
        and t90 is not None
    ):
        return round(
            t90 - t10,
            3
        )

    return None


# ==========================================================
# SETTLING TIME
# ==========================================================

def calculate_settling_time(
    time_data,
    response,
    setpoint,
    tolerance=0.02
):
    """
    Settling Time

    Default:
    ±2% band
    """

    if (
        len(time_data) == 0
        or len(response) == 0
    ):
        return None

    band = (
        abs(setpoint)
        * tolerance
    )

    for i in range(
        len(response)
    ):

        remaining = response[i:]

        if all(

            abs(x - setpoint)
            <= band

            for x in remaining
        ):

            return round(
                time_data[i],
                3
            )

    return None


# ==========================================================
# ROOT MEAN SQUARE ERROR
# ==========================================================

def calculate_rmse(
    response,
    setpoint
):
    """
    Root Mean Square Error
    """

    if len(response) == 0:
        return 0.0

    errors = [
        setpoint - r
        for r in response
    ]

    rmse = np.sqrt(
        np.mean(
            np.square(errors)
        )
    )

    return round(
        float(rmse),
        3
    )


# ==========================================================
# INTEGRAL ABSOLUTE ERROR
# ==========================================================

def calculate_iae(
    response,
    setpoint,
    dt
):
    """
    Integral Absolute Error
    """

    if len(response) == 0:
        return 0.0

    iae = sum(
        abs(setpoint - r)
        * dt
        for r in response
    )

    return round(
        iae,
        3
    )


# ==========================================================
# INTEGRAL SQUARED ERROR
# ==========================================================

def calculate_ise(
    response,
    setpoint,
    dt
):
    """
    Integral Squared Error
    """

    if len(response) == 0:
        return 0.0

    ise = sum(
        (setpoint - r) ** 2
        * dt
        for r in response
    )

    return round(
        ise,
        3
    )


# ==========================================================
# COMPLETE METRICS
# ==========================================================

def calculate_metrics(
    time_data,
    response_data,
    setpoint,
    dt=None
):
    """
    Master metric calculation routine.
    """

    metrics = {

        "Overshoot":
            calculate_overshoot(
                response_data,
                setpoint
            ),

        "Peak Value":
            calculate_peak_value(
                response_data
            ),

        "Rise Time":
            calculate_rise_time(
                time_data,
                response_data,
                setpoint
            ),

        "Settling Time":
            calculate_settling_time(
                time_data,
                response_data,
                setpoint
            ),

        "Steady State Error":
            calculate_steady_state_error(
                response_data,
                setpoint
            ),

        "RMSE":
            calculate_rmse(
                response_data,
                setpoint
            )
    }

    if dt is not None:

        metrics["IAE"] = (
            calculate_iae(
                response_data,
                setpoint,
                dt
            )
        )

        metrics["ISE"] = (
            calculate_ise(
                response_data,
                setpoint,
                dt
            )
        )

    return metrics


# ==========================================================
# REQUIREMENT SCORE
# ==========================================================

def calculate_requirement_score(
    metrics,
    max_overshoot,
    max_settling_time,
    max_ss_error
):
    """
    Returns:

    {
        "score": 100,
        "results": [...]
    }
    """

    results = []

    passed = 0

    # Overshoot

    if (
        metrics["Overshoot"]
        <= max_overshoot
    ):

        results.append(
            "PASS - Overshoot Requirement"
        )

        passed += 1

    else:

        results.append(
            "FAIL - Overshoot Requirement"
        )

    # Settling Time

    settling_time = metrics.get(
        "Settling Time"
    )

    if (
        settling_time is not None
        and settling_time
        <= max_settling_time
    ):

        results.append(
            "PASS - Settling Time Requirement"
        )

        passed += 1

    else:

        results.append(
            "FAIL - Settling Time Requirement"
        )

    # Steady State Error

    if (
        abs(
            metrics[
                "Steady State Error"
            ]
        )
        <= max_ss_error
    ):

        results.append(
            "PASS - Steady State Error Requirement"
        )

        passed += 1

    else:

        results.append(
            "FAIL - Steady State Error Requirement"
        )

    score = round(
        (passed / 3) * 100,
        1
    )

    return {
        "score": score,
        "results": results
    }