filelist=$(ls /home/mbtrec/trec/time_kde/rank_kde)
for file in $filelist
do
    trec_eval -q -c /home/mbtrec/trec/api/twitter-tools-core/data/qrels.microblog2011_new.txt /home/mbtrec/trec/time_kde/rank_kde/$file > /home/mbtrec/trec/time_kde/eval/$file
done


# combine
