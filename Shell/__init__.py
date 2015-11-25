filelist = $(ls /home/mbtrec/trec/bwang_combine/2013)
for file in $filelist
do
    trec_eval -q -c /home/mbtrec/trec/api/twitter-tools-core/data/qrels.microblog2013.txt /home/mbtrec/trec/bwang_combine/2013/$file > /home/mbtrec/trec/eval/bwang_eval/$file
done
