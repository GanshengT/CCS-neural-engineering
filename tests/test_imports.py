def test_imports():
    import CCSNE
    import CCSNE.illustration

    assert hasattr(CCSNE, "illustration")


def test_expected_api():
    from CCSNE.illustration import plot_distribution_by_category, plot_rayleigh_by_polarity

    assert callable(plot_rayleigh_by_polarity)
    assert callable(plot_distribution_by_category)
