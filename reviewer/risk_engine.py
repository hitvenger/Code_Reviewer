def calculate_risk(summary):

    return (
        summary["High"] * 5 +
        summary["Medium"] * 3 +
        summary["Low"] * 1
    )
