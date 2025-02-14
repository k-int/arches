"""
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import os
from tests.base_test import ArchesTestCase
from django.test.utils import captured_stdout
from arches.app.models.models import Language, TileModel
from arches.app.utils.betterJSONSerializer import JSONDeserializer
from arches.app.utils.skos import SKOSReader
from arches.app.utils.data_management.resource_graphs.importer import (
    import_graph as ResourceGraphImporter,
)
from arches.app.utils.data_management.resources.importer import BusinessDataImporter


# these tests can be run from the command line via
# python manage.py test tests.models.mapped_csv_import_tests --settings="tests.test_settings"


class mappedCSVFileImportTests(ArchesTestCase):
    graph_fixtures = ["Cardinality Test Model"]

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        skos = SKOSReader()
        rdf = skos.read_file("tests/fixtures/data/concept_label_test_scheme.xml")
        ret = skos.save_concepts_from_skos(rdf)

        skos = SKOSReader()
        rdf = skos.read_file("tests/fixtures/data/concept_label_test_collection.xml")
        ret = skos.save_concepts_from_skos(rdf)

        with open(
            os.path.join("tests/fixtures/data/json/cardinality_test_data/target.json"),
            "r",
        ) as f:
            archesfile = JSONDeserializer().deserialize(f)
        ResourceGraphImporter(archesfile["graph"])

        with open(
            os.path.join(
                "tests/fixtures/data/json/cardinality_test_data/file-list.json"
            ),
            "r",
        ) as f:
            archesfile = JSONDeserializer().deserialize(f)
        ResourceGraphImporter(archesfile["graph"])

    def test_nonexistent_language_check(self):
        new_languages = BusinessDataImporter(
            "tests/fixtures/data/csv/required_node_import_new_languages.csv"
        ).scan_for_new_languages()
        self.assertNotEqual(new_languages, None)
        self.assertEqual(len(new_languages), 2)

    def test_language_differs_only_in_case(self):
        Language.objects.get_or_create(code="en-US")  # see header in test file
        new_languages = BusinessDataImporter(
            "tests/fixtures/data/csv/mixed_case_language_codes.csv"
        ).scan_for_new_languages()
        self.assertEqual(new_languages, ["en-ZA"])

    def test_single_1(self):
        og_tile_count = TileModel.objects.count()
        with captured_stdout():
            BusinessDataImporter(
                "tests/fixtures/data/csv/cardinality_test_data/single-1_to_1.csv"
            ).import_business_data()
        new_tile_count = TileModel.objects.count()
        tile_difference = new_tile_count - og_tile_count
        self.assertEqual(tile_difference, 1)

    def test_single_n_to_n(self):
        og_tile_count = TileModel.objects.count()
        with captured_stdout():
            BusinessDataImporter(
                "tests/fixtures/data/csv/cardinality_test_data/single-n_to_n.csv"
            ).import_business_data()
        new_tile_count = TileModel.objects.count()
        tile_difference = new_tile_count - og_tile_count
        self.assertEqual(tile_difference, 2)

    def test_single_n_to_1(self):
        og_tile_count = TileModel.objects.count()
        with captured_stdout():
            BusinessDataImporter(
                "tests/fixtures/data/csv/cardinality_test_data/single-n_to_1.csv"
            ).import_business_data()
        new_tile_count = TileModel.objects.count()
        tile_difference = new_tile_count - og_tile_count
        self.assertEqual(tile_difference, 1)

    def test_1_1(self):
        og_tile_count = TileModel.objects.count()
        with captured_stdout():
            BusinessDataImporter(
                "tests/fixtures/data/csv/cardinality_test_data/1-1.csv"
            ).import_business_data()
        new_tile_count = TileModel.objects.count()
        tile_difference = new_tile_count - og_tile_count
        self.assertEqual(tile_difference, 2)

    def test_1_n(self):
        og_tile_count = TileModel.objects.count()
        with captured_stdout():
            BusinessDataImporter(
                "tests/fixtures/data/csv/cardinality_test_data/1-n.csv"
            ).import_business_data()
        new_tile_count = TileModel.objects.count()
        tile_difference = new_tile_count - og_tile_count
        self.assertEqual(tile_difference, 3)

    def test_n_1(self):
        og_tile_count = TileModel.objects.count()
        with captured_stdout():
            BusinessDataImporter(
                "tests/fixtures/data/csv/cardinality_test_data/n-1.csv"
            ).import_business_data()
        new_tile_count = TileModel.objects.count()
        tile_difference = new_tile_count - og_tile_count
        self.assertEqual(tile_difference, 4)

    def test_n_n(self):
        og_tile_count = TileModel.objects.count()
        with captured_stdout():
            BusinessDataImporter(
                "tests/fixtures/data/csv/cardinality_test_data/n-n.csv"
            ).import_business_data()
        new_tile_count = TileModel.objects.count()
        tile_difference = new_tile_count - og_tile_count
        self.assertEqual(tile_difference, 6)

    def test_domain_label_import(self):
        og_tile_count = TileModel.objects.count()
        with captured_stdout():
            BusinessDataImporter(
                "tests/fixtures/data/csv/domain_label_import.csv"
            ).import_business_data()
        new_tile_count = TileModel.objects.count()
        tile_difference = new_tile_count - og_tile_count
        self.assertEqual(tile_difference, 1)

    def test_concept_label_import(self):
        og_tile_count = TileModel.objects.count()
        with captured_stdout():
            BusinessDataImporter(
                "tests/fixtures/data/csv/concept_label_import.csv"
            ).import_business_data()
        new_tile_count = TileModel.objects.count()
        tile_difference = new_tile_count - og_tile_count
        self.assertEqual(tile_difference, 1)

    def test_required_node_import(self):
        og_tile_count = TileModel.objects.count()
        with captured_stdout():
            BusinessDataImporter(
                "tests/fixtures/data/csv/required_node_import.csv"
            ).import_business_data()
        new_tile_count = TileModel.objects.count()
        tile_difference = new_tile_count - og_tile_count
        self.assertEqual(tile_difference, 0)

    def test_required_child_node_import(self):
        og_tile_count = TileModel.objects.count()
        with captured_stdout():
            BusinessDataImporter(
                "tests/fixtures/data/csv/required_child_node_import.csv"
            ).import_business_data()
        new_tile_count = TileModel.objects.count()
        tile_difference = new_tile_count - og_tile_count
        self.assertEqual(tile_difference, 0)

    def test_file_list_datatype_import(self):
        og_tile_count = TileModel.objects.count()
        with captured_stdout():
            BusinessDataImporter(
                "tests/fixtures/data/csv/file_list_datatype_import.csv"
            ).import_business_data()
        new_tile_count = TileModel.objects.count()
        tile_difference = new_tile_count - og_tile_count
        self.assertEqual(tile_difference, 1)
