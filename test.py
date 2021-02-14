#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spacy
import pytextrank
import traceback
import unittest


class TestPTR (unittest.TestCase):
    def setUp (self):
        """set up a spaCy pipeline"""
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe("textrank", last=True)


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

        with self.nlp.select_pipes(disable=["textrank"]):
            doc = self.nlp(text)
            assert len(doc._.phrases) == 0


    def test_noun_chunk_fails (self):
        text = "everything you need to know about student loan interest rates variable and fixed rates capitalization amortization student loan refinancing and more."
        doc = self.nlp(text)
        phrases = [ p.text for p in doc._.phrases ]

        print("\nUSING: |{}|\n  =>{}".format(text, phrases))
        self.assertTrue(len(doc._.phrases) >= 0)


if __name__ == "__main__":
    unittest.main()
