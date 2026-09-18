from aegistwin.mutation import evaluate_mutations


def test_mutations_expose_missing_security_test_requirements():
    results = evaluate_mutations()
    assert len(results) == 2
    assert all(result.survived for result in results)
    assert all("403" in result.generated_test for result in results)

