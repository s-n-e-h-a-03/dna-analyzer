import sys
CODONS ={
    "UUU": "F", "UUC": "F",
    "UUA": "L", "UUG": "L",
    "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",

    "AUU": "I", "AUC": "I", "AUA": "I",
    "AUG": "M",

    "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",

    "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
    "AGU": "S", "AGC": "S",

    "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",

    "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",

    "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",

    "UAU": "Y", "UAC": "Y",

    "UAA": "*", "UAG": "*", "UGA": "*",

    "CAU": "H", "CAC": "H",
    "CAA": "Q", "CAG": "Q",

    "AAU": "N", "AAC": "N",

    "AAA": "K", "AAG": "K",

    "GAU": "D", "GAC": "D",
    "GAA": "E", "GAG": "E",

    "UGU": "C", "UGC": "C",
    "UGG": "W",

    "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGA": "R", "AGG": "R",

    "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G"
    }
def main():
    sequences={}
    current_header =""
    if len(sys.argv) != 2:
        print("Usage: python main.py <fasta_file>")
        return

    filename = sys.argv[1]
    try: 
        with open(filename, "r") as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                if line.startswith(">"):
                    current_header=line[1:]
                    sequences[current_header]=""
                else:
                    if current_header!= "":
                    # if the header is empty then it will continue past this if statement
                        sequences[current_header]+=line.upper()

    except FileNotFoundError:
        print("Sorry there is no file")
        return
    for sequence in sequences:
        print()
        print(f"Analyzing sequence: {sequence}")
        print("="*122)
        # total length of the sequence
        print("Total length of the sequence =", len(sequences[sequence]))
        GC_calculator(sequences[sequence])
        complementary_strand(sequences[sequence])
        rna_seq =rna_producer(sequences[sequence])
        print()
        print_sequence("RNA sequence: ", rna_seq)
        print()
        aa_seq=aa_generator(rna_seq)
        print_sequence("Amino acid sequence: ",aa_seq )
        ORF_generator(aa_seq)

def print_sequence(title, sequence, width=70):
    print(title)
    for i in range(0, len(sequence), width):
        print(sequence[i:i+width])

def GC_calculator(seq):
    if len(seq)==0:
        print("Sequence is empty")
        return
    counts = {'A': 0, 'T': 0, 'G': 0, 'C': 0, 'N': 0}
    # GC content is calculated
    for i in seq:
        if i in counts:
            counts[i]+=1
        else:
            print(f"Invalid character {i} found in the sequence. Please enter a valid DNA sequence.")
            return
    gc = ((counts['G']+counts['C'])/len(seq))*100
    print(f"Percentage GC content in the sequence = {gc:.2f}%")
    # number of each nucleotide is calculated
    for i in counts:
        print(f"{i} count = {counts[i]}")

def complementary_strand(seq):
    reverse = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N'}
    base=""
    # complementary DNA starnd is formed
    for i in seq:
        if i in reverse:
            base += reverse[i]    
    print_sequence("Reverse complement: ",base[::-1])

def rna_producer(seq):
    rna_seq= seq.replace("T", "U")
    return rna_seq

def aa_generator(rna_seq):
    codon=""
    aa_seq=""
    for i in rna_seq:
        codon+=i
        if len(codon)==3:
            if codon in CODONS:
                aa_seq+=CODONS[codon]
            codon=""
    return aa_seq
    

def ORF_generator(aa_seq):
    orfs = {}
    orf_id = 1
    current_orf= ""
    in_orf = False  

    for aa in aa_seq:
        if not in_orf:
            if aa == "M":
                in_orf = True
                current_orf = "M"
        else:
            current_orf += aa
            if aa == "*":
                orfs[orf_id] = current_orf
                orf_id += 1
                in_orf = False
                current_orf = ""
    if in_orf:
        orfs[orf_id] = current_orf
    print()
    if orfs:
        max_orf = max(orfs, key=lambda k: len(orfs[k]))
        longest_seq = orfs[max_orf]
        print(f"Longest ORF: ORF{max_orf}\nLength: {len(longest_seq)} aa")
        print_sequence("ORF Sequence: ", longest_seq)
    else:
        print("No valid ORFs found")
if __name__ == "__main__":
    main()