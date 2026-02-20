#! /bin/sh

for i in `cat File_list`; do echo $i; cut -f 1 ${i}.txt | grep -v geneName | sort | uniq | wc -l; done | sed 'N;s/\n/\t/g' > Final_GeneNumber_GOTerm
sort Final_GeneNumber_GOTerm | uniq > Final_GeneNumber_GOTerm1

join -1 1 -2 1 Final_GeneNumber_GOTerm1 Final_PearsonCor_GOTerm1 > total_Info_Dataset_sgdtransformed_biological_process_negset1_withholdimp.txt
