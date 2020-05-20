#!/usr/bin/env python
# encoding: utf-8

import spacy
import pytextrank
import traceback
import unittest
import warnings


class TestRCGraph (unittest.TestCase):
    def setUp (self):
        """set up a spaCy pipeline"""
        self.nlp = spacy.load("en_core_web_sm")
        self.tr = pytextrank.TextRank(logger=None)
        self.nlp.add_pipe(self.tr.PipelineComponent, name="textrank", last=True)


    def test_minimal (self):
        text = "linear constraints over the"
        doc = self.nlp(text)
        phrases = [ p.text for p in doc._.phrases ]

        print("\nUSING: |{}|\n  =>{}".format(text, phrases))
        self.assertTrue(any(map(lambda x: "constraints" in x, phrases)))


    def test_py35_dict_keyerror (self):
        text = "linear constraints over the set of natural numbers"
        doc = self.nlp(text)
        phrases = [ p.text for p in doc._.phrases ]

        print("\nUSING: |{}|\n  =>{}".format(text, phrases))
        self.assertTrue(any(map(lambda x: "constraints" in x, phrases)))


    def test_enable_disable_pipeline (self):
        text = "linear constraints over the set of natural numbers"
        doc = self.nlp(text)

        with self.nlp.disable_pipes("textrank"):
            doc = self.nlp(text)
            assert len(doc._.phrases) == 0


if __name__ == "__main__":
    unittest.main()
