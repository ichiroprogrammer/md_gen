import unittest

from plant_uml_encode import get_args, gen_str
from md_lib.file_container import FileContainer


class TestPlantUmlEncode(unittest.TestCase):
    def test_args(self):
        act0 = get_args("a.pu".split(" "))
        exp0 = {"pu": "a.pu", "o": None}
        self.assertEqual(exp0, act0)

    def test_gen_str(self):
        args = get_args("test/data_pu/rectangle_square.pu".split(" "))
        pu_enc_act = gen_str(args)

        pu_enc_exp = (
            "http://www.plantuml.com/plantuml/img/"
            "SoWkIImgAStDuU9ApaaiBbO8IaqkISnBpqbLgEPI00BjuDII20rDE3iIojOjJYs9hq3cL08vjJ1ZWWjB4ujWPk1KYx3CfaOt9RyyJnUgaOlB8JKl1UGi00=="
        )

        self.assertEqual(pu_enc_exp, pu_enc_act)
