import sys

def update_headers(fasta_file, tsv_file, mode):
    # Ladda rubrikmappen från TSV-filen
    header_map = {}
    with open(tsv_file, 'r') as tsv:
        for line in tsv:
            short, full = line.strip().split('\t')
            header_map[short.lstrip('>')] = full.lstrip('>')

    # Skapa en temporär fil för att uppdatera FASTA-innehållet
    with open(fasta_file, 'r') as fasta, open(f"{fasta_file}.tmp", 'w') as output:
        for line in fasta:
            if line.startswith('>'):
                original_header = line[1:].strip()  # Ta bort '>'
                if mode == "short":
                    new_header = next((key for key, value in header_map.items() if value == original_header), None)
                elif mode == "full":
                    new_header = header_map.get(original_header)
                else:
                    print("Mode must be 'short' or 'full'")
                    return

                if new_header:
                    output.write(f">{new_header}\n")
                else:
                    print(f"Header not found in TSV: {original_header}")
                    output.write(line)  # Behåll originalrubriken om ingen matchning hittas
            else:
                output.write(line)  # Behåll sekvensen oförändrad

    # Ersätt originalfilen med den uppdaterade filen
    import os
    os.replace(f"{fasta_file}.tmp", fasta_file)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python rename_headers.py <fasta_file> <tsv_file> <mode>")
        print("<mode>: 'short' to use short headers, 'full' to use full headers")
    else:
        fasta_file = sys.argv[1]
        tsv_file = sys.argv[2]
        mode = sys.argv[3]
        update_headers(fasta_file, tsv_file, mode)
