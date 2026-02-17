def test_imports():
    import CCSNE
    import CCSNE.analysis
    import CCSNE.illustration

    assert hasattr(CCSNE, "analysis")
    assert hasattr(CCSNE, "illustration")


def test_expected_api():
    from CCSNE.illustration import plot_rayleigh_by_polarity
    from CCSNE.analysis import circ_mardia_watson_wheeler

    assert callable(plot_rayleigh_by_polarity)
    assert callable(circ_mardia_watson_wheeler)
