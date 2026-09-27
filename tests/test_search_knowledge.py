from src.tools.search_knowledge import _score


def test_score_matches_terms():
    score, matched = _score(
        "ZMM_IMX_0004 genera documentos SNC y utiliza K4",
        ["zmm_imx_0004", "snc"],
    )

    assert score == 1.0
    assert matched == ("zmm_imx_0004", "snc")


def test_score_ignores_missing_terms():
    score, matched = _score(
        "Documento funcional de SNC",
        ["snc", "zmm_imx_0004"],
    )

    assert score == 0.5
    assert matched == ("snc",)
