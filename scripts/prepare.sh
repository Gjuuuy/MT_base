####
### Preparation script for preprocessing work
### 1. Filter 2. sentencepiece model training. 3. subwording
### ./scripts/prepare.sh src_file trg_file vocab_size model_type[bpe, word, unigram, char]
####

cwd=$(pwd)
swd="$(pwd)/scripts"

osrc=$1 # Original Train Source
otrg=$2 # original Train Target
vocab=$3 # 
model_type=$4
daba=$5

echo "Filter the dataset and cleaning it up..."
python3.9 "${swd}/filter.py" $osrc $otrg

echo "Building the vocab and creating sentencepiece model"
python3.9 "${swd}/preprocess.py" "$osrc.fil.txt" "$otrg.fil.txt" $vocab $model_type $daba

# Make sure you are executing from root directory
mv *.model *.vocab data/

python3.9 "${swd}/de_subword.py" 1 data/source.model data/target.model $osrc.fil.txt $otrg.fil.txt
#mv $osrc.bam.fil.txt.subword $osrc.bam.txt
#mv $otrg.bam.fil.txt.subword $otrg.bam.txt

for cp in dev test;
do
    echo $cp;
    python3.9 "${swd}/de_subword.py" 1 data/source.model data/target.model data/$cp.bam data/$cp.fr
    #mv data/$cp.bam.subword data/$cp.bam.txt
    #mv data/$cp.fr.subword data/$cp.fr.txt
done
