from kgtools.preprocessing import Pipeline
from kgtools.func import parallel
from kgtools.saver import Saver

if __name__ == "__main__":
    conf = {
        "cleaner": {
            "rules": [{"type": "root_node", "attr": "class", "value": "devsite-article-body"}]
        }
    }
    pipeline = Pipeline(conf=conf)
    data = Saver.load("testdata/guide.bin")
    docs, sentences = pipeline.process(data)

    Saver.dump(docs, "testdata/docs.bin")
    Saver.dump(sentences, "testdata/sentences.bin")

    with Path("testdata/sentences.txt").open("w", encoding="utf-8") as f:
        f.write("\n".join([str(sent) for sent in sentences]))
    with Path("testdata/tokens.txt").open("w", encoding="utf-8") as f:
        f.write("\n".join([str(sent) + "\n" + sent.tokenized_text + "\n" + sent.lemma_text + "\n" for sent in sentences]))
    with Path("testdata/vocab.txt").open("w", encoding="utf-8") as f:
        f.write("\n".join(sorted(vocab.words, key=lambda x: x)))
    print(vocab.get_emb("-PRON-"))
