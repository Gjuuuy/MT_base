import sys
import sentencepiece as spm


def subword(source_model,target_model,source_raw,target_raw) :

    source_subworded = source_raw.split(".")[0] + ".sub-src.txt"
    target_subworded = target_raw.split(".")[0] + ".sub-trg.txt"

    sp = spm.SentencePieceProcessor()

    sp.load(source_model)
    with open(source_raw) as source, open(source_subworded, "w+") as source_subword:
        for line in source:
            line = line.strip()
            line = sp.encode_as_pieces(line)
            # line = ['<s>'] + line + ['</s>']    # add start & end tokens; optional
            line = " ".join([token for token in line])
            source_subword.write(line + "\n")

    print("Done subwording the source file! Output:", source_subworded)


    # Subwording the train target

    sp.load(target_model)

    with open(target_raw) as target, open(target_subworded, "w+") as target_subword:
        for line in target:
            line = line.strip()
            line = sp.encode_as_pieces(line)
            # line = ['<s>'] + line + ['</s>']    # add start & end tokens; unrequired for OpenNMT
            line = " ".join([token for token in line])
            target_subword.write(line + "\n")

    print("Done subwording the target file! Output:", target_subworded)

def desubword(target_model, target_pred) :

    target_decodeded = target_pred + ".desub.txt"


    sp = spm.SentencePieceProcessor()
    sp.load(target_model)


    with open(target_pred) as pred, open(target_decodeded, "w+") as pred_decoded:
        for line in pred:
            line = line.strip().split(" ")
            line = sp.decode_pieces(line)
        pred_decoded.write(line + "\n")
            
    print("Done desubwording! Output:", target_decodeded)



if __name__ == '__main__' :

    mode = int(sys.argv[1])

    if mode == 1 :

        source_model = sys.argv[2]
        target_model = sys.argv[3]
        source_raw = sys.argv[4]
        target_raw = sys.argv[5]

        subword(source_model,target_model,source_raw, target_raw)

    elif mode == 2 :

        target_model = sys.argv[2]
        target_pred = sys.argv[3]

        desubword(target_model, target_pred)
