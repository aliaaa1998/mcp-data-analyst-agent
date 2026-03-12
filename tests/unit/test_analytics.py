from mcp_servers.analytics_server.analytics import (
    calculate_growth,
    compare_periods,
    detect_anomalies,
)


def test_calculate_growth():
    result = calculate_growth([100, 120, 150])
    assert round(result["growth_pct"], 2) == 50.0


def test_compare_periods():
    result = compare_periods(200, 100)
    assert result["delta"] == 100
    assert result["delta_pct"] == 100


def test_detect_anomalies():
    result = detect_anomalies([10, 10, 10, 200], threshold_std=1.4)
    assert 3 in result["anomaly_indices"]
