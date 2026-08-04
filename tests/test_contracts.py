from __future__ import annotations

import unittest

from ordivon_world import ContractError, load_schema, validate_contract


class ContractTests(unittest.TestCase):
    def test_all_published_contracts_are_valid_draft_2020_12(self) -> None:
        names = (
            "browser-request",
            "edge-capabilities",
            "edge-receipt",
            "fetch-request",
            "network-observation",
            "world-observation",
            "world-prepared-dispatch",
        )
        for name in names:
            with self.subTest(name=name):
                self.assertEqual(
                    load_schema(name)["$schema"],
                    "https://json-schema.org/draft/2020-12/schema",
                )

    def test_fetch_contract_rejects_unowned_options(self) -> None:
        with self.assertRaises(ContractError):
            validate_contract(
                "fetch-request",
                {
                    "url": "https://example.com/",
                    "maximum_bytes": 1024,
                    "timeout_ms": 1000,
                    "accept": "*/*",
                    "authorization": "forbidden",
                },
            )


if __name__ == "__main__":
    unittest.main()
