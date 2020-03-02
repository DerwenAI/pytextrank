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

        print(f"\nUSING: |{text}|\n  =>{phrases}")
        self.assertTrue("linear constraints" in phrases)


    def test_py35_dict_keyerror (self):
        text = "linear constraints over the set of natural numbers"
        doc = self.nlp(text)
        phrases = [ p.text for p in doc._.phrases ]

        print(f"\nUSING: |{text}|\n  =>{phrases}")
        self.assertTrue("linear constraints" in phrases)


if __name__ == "__main__":
    unittest.main()
