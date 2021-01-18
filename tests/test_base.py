import spacy

from pytextrank.base import BaseTextRank


def test_base_text_rank():
    # given
    text = """
    roger martínez given second chance, may start against pumas.

    roger martínez has become a real headache for the entire club américa time as there has been a debate for well over a month now about what the club should do with the player.
    martínez had been holding out for a european move but when did not come, he turned down a pair of mls deals (rumoured to be in the range of $15m) to inter miami and los angeles galaxy – much to the chagrin of the américa heirarchy.
    while there are many who support the notion to keep the colombian attacker frozen out of the squad, other fans say he should be forgiven – especially because up to nine other players could miss out due to injury or suspension.
    on wednesday, it appears there was a change of heart in the américa camp as various sources, including espn, fox sports, and other major sports media, say that roger’s punishment has been lifted.
    if this is true, the fact is that he would very likely start in the match against pumas this friday.
    in training on wednesday, manager miguel herrera rehearsed with martínez as part of the starting squad, so everything that he will lead the line in the clásico capitalino.
    since joining américa from villarreal, the 25-year-old has scored 17 goals and contributed 11 assists in 67 matches.
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    base_text_rank = BaseTextRank()

    # when
    processed_doc = base_text_rank(doc)
    phrases = processed_doc._.phrases

    # then
    assert len(phrases)
    assert len(set(p.text for p in phrases)) == len(phrases)
    assert phrases[0].rank == max(p.rank for p in phrases)
