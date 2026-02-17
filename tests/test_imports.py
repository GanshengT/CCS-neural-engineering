def test_imports():
    import CCSNE
    import CCSNE.analysis
    import CCSNE.illustration

    assert hasattr(CCSNE, "analysis")
    assert hasattr(CCSNE, "illustration")
