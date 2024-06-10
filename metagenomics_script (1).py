import argparse
from pathlib import Path
import numpy as np

def parse_arguments():
    #Create the arguments and the help menssage to introduce data to the program
    desc = "Generate random number of SNPs in FASTA sequences with a specific mutation rate"
    parser = argparse.ArgumentParser(description=desc)

    help_fasta_file = "File in format FASTA with sequencies"
    parser.add_argument("--fasta" ,
                        "-f", type=str,
                        help=help_fasta_file,
                        required=True)
    
    help_rate_mutation= "Percentage that we want that our sequences will be mutated"
    parser.add_argument("--mutation",
                        "-m", type=float,
                        help=help_rate_mutation,
                        required=True)
    
    help_output = "Name that our output files want to have"
    parser.add_argument("--out" ,
                        "-o", type=str,
                        help=help_output,
                        required = False,
                        default = "Mutated")
    
    return parser

def get_options():
    #Use arguments in order to introduce the necessary data to the program
    parser = parse_arguments()
    options = parser.parse_args()
    file = Path(options.fasta)
    rate = options.mutation
    out = options.out

    return {"file" : file,
            "rate" : rate,
            "out" : out}




def get_fasta_sequences(file):
    fasta_dictionary = {}
    with open(file, 'r') as fasta:
        a = False
        for line in fasta:
            if '>' in line:
                if a == True:
                    fasta_dictionary[name] = seq
                name = line
                seq = ""
            else:
                a = True
                line = line.strip()
                seq += line
        fasta_dictionary[name] = seq
        print(len(seq))
    return fasta_dictionary 

def get_changes (fasta_dictionary, rate = 60):
    bases = ["A","C", "G", "T"]
    changes_dict = {}
    for key, seq in fasta_dictionary.items():
      number = int(np.floor(rate/100 *len(seq)))
      if number == 0:
          changes_dict[key] = 0
          continue
      length = len(seq)
      changes = []
      random_number = np.random.choice(np.arange(0,length), size=number, replace=False)
      random_number = np.sort(random_number)
      #print(random_number)

      for i in random_number:
          new_base_dict = [x for x in bases if x != seq[i]] #make new list not with the base that we change
          new_base = np.random.choice(new_base_dict)
          changes.append([i,seq[i],new_base])


      changes_dict[key] = changes
    return changes_dict

#changes_dict = get_changes(fasta_dictionary)
def get_modied_sequences(changes_dict, fasta_dictionary):
    new_sequences = {}
    #print(changes_dict.items())
    for key, changes in changes_dict.items():
        #print(changes)

        seq = fasta_dictionary[key]
        if changes == 0:
            new_sequences[key] = seq
            continue
        new_seq = [seq[:changes[0][0]]] #adding the sequence before the change
        count = len(changes)



        if count == 1:
            new_seq.append(changes[0][2]) #adding the new base name
            new_seq.append(seq[changes[0][0]+1:]) #adding the rest of the sequence
            new_fasta = ''.join(new_seq)
            new_sequences[key] = new_fasta
            continue

      #bliver resten her ikke nødt til at være under et else:
        for i in range((count - 1)):
            base = changes[i][2] #base is not the base it needs to be changed to
            start = changes[i][0] + 1 #where the base needs to be inserted
            end = changes[i+1][0] #the place the next change needs to be
            new_seq.append(base)
            new_seq.append(seq[start:(end)])


        #det her skal nemlig ikke ske for det første

        new_seq.append(changes[-1][2])
        #print(changes[-1][2])
        new_seq.append(seq[(changes[-1][0]+1):])


        new_fasta = ''.join(new_seq)
        new_sequences[key] = new_fasta
    return new_sequences

def write_output_fasta(out,new_sequences):
    file_name = "{}.fasta".format(out)
    with open(file_name, 'w') as fasta:
        for name, seq in new_sequences.items():
            line = "{}{}\n".format(name,seq)
            fasta.write(line)
        fasta.flush()

def write_output_positios(out,changes_dict):
    file_name = "{}.tsv".format(out)
    with open(file_name, 'w') as tsv:
        upper_line = "Sequence\tPosition\tOriginal\tChange\n"
        tsv.write(upper_line)
        for name, changes in changes_dict.items():
            if changes == 0:
                continue
            name = name[1:-1]
            for change in changes:
                line = "{}\t{}\t{}\t{}\n".format(name,change[0],change[1],change[2])
                tsv.write(line)        
        tsv.flush()

def main():
    options = get_options()
    file = options["file"]
    rate = options["rate"]
    out = options["out"]

    fasta_dictionary = get_fasta_sequences(file)
    #print(fasta_dictionary)
    changes_dict = get_changes(fasta_dictionary, rate)
    #print(changes_dict)
    new_sequences = get_modied_sequences(changes_dict, fasta_dictionary)
    #print(fasta_dictionary,changes_dict,new_sequences)
    write_output_fasta(out,new_sequences)
    write_output_positios(out,changes_dict)

if __name__ == '__main__':
    main()

        


    


    


