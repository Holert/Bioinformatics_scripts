#usage python create.gene.db.from.contig.py <gene.fasta> <protein.fasta> <reads.mapping.from assembly> <output.pkl>
#        	0			        1		2		3			4

import sys, screed, pickle

out1=sys.argv[4]
fileout=open(out1,'w')


#1 create dictionary for nucleotide sequence

fastadict={}
for record in screed.open(sys.argv[1]):
   name=record.name			#get sequence name
   description=record.description	#get sequence description
   description=description.strip().split('#')
   start_position=float(description[1])
   end_position=float(description[2])
   orientation=float(description[3])
   nucleotide_sequence=record.sequence
   x=fastadict.get(name, [])
   x.append(start_position)
   x.append(end_position)
   x.append(orientation)
   x.append(nucleotide_sequence)
   fastadict[name]=x

#2 create dictionary for protein sequence

fastadict2={}
for record2 in screed.open(sys.argv[2]):
   name2=record2.name
   contig_numbers=name2.split('_')
   contig_number=contig_numbers[0]
   protein_sequence=record2.sequence
   y=fastadict2.get(name2,[])
   y.append(protein_sequence)    
   y.append(contig_number)
   fastadict2[name2]=y


#3 add protein and contig number to nucleotide dictionary

for key1 in fastadict.iterkeys():
#   print 'key is:'
#   print key1
   fastadict_values1=fastadict.get(key1)
#   print 'nucl.dict is'
#   print fastadict_values1
   fastadict_values2=fastadict2.get(key1)
#   print 'prot.dict is'
#   print fastadict_values2
   finalvalues=fastadict_values1+fastadict_values2
#   print 'mixed is :'
#   print finalvalues
   fastadict[key1]=finalvalues

#4. create dictionary from stats of assembly

contigsdict={}
for line in open (sys.argv[3]):
   line=line.split('\t')
   name3=line[0]
   contig_length=line[1]
   contig_gc=line[2]
   contig_fold=line[3]
   contig_fold_sd=line[4]
   contig_base_coverage=line[5]
   contig_base_coverage=contig_base_coverage.strip('\n')
   z=contigsdict.get(name3,[])
   z.append(contig_length)
   z.append(contig_gc)
   z.append(contig_length)
   z.append(contig_fold)
   z.append(contig_fold_sd)
   z.append(contig_base_coverage)
   contigsdict[name3]=z


for key in fastadict.iterkeys():
   z2=fastadict.get(key)	#get all values
   print z2
   z3=z2[5]			#get contig number
   print z3
   z4=contigsdict.get(z3)	#get all values from contig dictionary
   print z4
   new_value=z2+z4		#add vakyes from fasta dictionary and contig dictionary together 
   fastadict[key]=new_value	#update dictionary

pickle.dump(fastadict,fileout)