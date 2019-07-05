SPACY_TRAINING_FORMAT = """

spaCy's json format for training data can be a pain to work with. The reason the
format is so hard is because it represents paragraphs, and allows multiple documents
to be in one file. These extra layers make the format pretty unwieldy.

The easiest way to produce data to use with the `spacy train` command is the
`spacy.gold.docs_to_json` function:

    import spacy.gold
    import spacy

    nlp = spacy.blank("en")
    doc1 = nlp("We are in Berlin.")
    doc2 = nlp("July 2019.")
    doc1.ents = [Span(nlp.vocab, 3, 4, label="GPE")]
    doc2.ents = [Span(nlp.vocab, 0, 2, label="DATE")]
    print(spacy.gold.docs_to_json(docs, id=0))

The nice thing about this is you can set up the annotations on the Doc object.
The only time this gets tricky is when you're setting the dependency parse. You
can't write to the `token.head` attribute one-by-one, as we want to make sure the
parse stays valid and consistent. So to set the parse, you need to use
doc.from_array.
"""
