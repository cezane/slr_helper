import sys, csv, os, json

def first_phase(args):
    in_filename = str(args[1]) # if len(args) != 0 else ""
    newfilename = str(args[2]) # if len(args) > 1 else ""
    rw_filename = str(args[3])
    files = [newfilename, rw_filename]
    file_exists = [os.path.isfile(newfilename), os.path.isfile(rw_filename)]
    #TODO add Decision title
    header = ["Decision", "Title", "Authors", "Year", "Abstract", "Keywords"]

    print("Enter the exact field names in the exact following order: \n")
    print('"Title", "Authors", "Year", "Abstract", "Keywords"')

    field_names = list()
    field_values = list()
    relatedworks_values = list()
    for i in range(1, len(header)):
        field_name = input("Enter the exact name of {} field in the file: ".format(header[i]))
        field_names.append(field_name)

    try:
        with open(in_filename, 'r', encoding='utf-8-sig') as infile:
            rowsreader = csv.DictReader(infile, delimiter=",")
            outrowsreader = list()
            if file_exists:
                with open(newfilename, 'r') as outfile:
                    outrowsreader = list(csv.DictReader(outfile))
            count = 0;
            for row in rowsreader:
                dict_row = {}
                for i in range(0, len(field_names)):
                    field = field_names[i]
                    dict_row[header[i]] = row[field] if field in row else ""

                if not any(r["Title"] == dict_row["Title"] for r in outrowsreader) \
                   or not file_exists:
                    if any (s in dict_row["Title"].lower() for s in ["survey", "review"]):
                        relatedworks_values.append(dict_row)
                    else:
                        field_values.append(dict_row)
                        count += 1
            print(count)
    except IOError:
        print("Could not open csv file: {}.".format(in_filename))

    fields = [field_values, relatedworks_values]

    for i in range(0, len(files)):
        try:
            with open(files[i], 'a') as outfile:
                rowswriter = csv.DictWriter(outfile, header)
                if not file_exists[i]:
                    rowswriter.writeheader()
                for row in fields[i]:
                    rowswriter.writerow(row)
        except IOError:
            print("Could not convert to csv file: {}.".format(files[i]))

def second_phase(args):
    reviewer1_in = str(args[1])
    reviewer2_in = str(args[2])
    outfiles = [str(args[3]), str(args[4]), str(args[5])]
    file_exists = [os.path.isfile(str(args[3])), os.path.isfile(str(args[4])), os.path.isfile(str(args[5]))]
    relevant = list()
    irrelevant = list()
    undefined = list()

    try:
        with open(reviewer1_in, 'r', encoding='utf-8-sig') as r1_file, \
             open(reviewer2_in, 'r', encoding='utf-8-sig') as r2_file:
            r1_reader = csv.DictReader(r1_file, delimiter=",")
            r2_reader = csv.DictReader(r2_file, delimiter=",")

            r = i = u = 0;
            for (row1, row2) in zip(r1_reader, r2_reader):
                if (row1["Decision"].lower() == "r" and row2["Decision"].lower() == "r"):
                    relevant.append(row1)
                    r += 1
                elif (row1["Decision"].lower() == "i" and row2["Decision"].lower() == "i"):
                        irrelevant.append(row1)
                        i += 1
                else:
                    undefined.append(row1)
                    u += 1
            print("#relevant: {}, \#irrelevant: {} and \#undefined: {}".format(r, i, u))
    except IOError:
        print("Could not open csv file: {} or {}.".format(reviewer1_in, reviewer2_in))

    results = [relevant, irrelevant, undefined]
    for i in range(0, len(outfiles)):
        try:
            with open(outfiles[i], 'a') as outfile:
                header = ["Decision", "Title", "Authors", "Year", "Abstract", "Keywords"]
                rowswriter = csv.DictWriter(outfile, header)
                if not file_exists[i]:
                    rowswriter.writeheader()
                for row in results[i]:
                    rowswriter.writerow(row)
        except IOError:
            print("Could not convert to csv file: {}.".format(outfiles[i]))


def main():
    #TODO add a usage guide: filter results (input --> output)
    #                 remove duplicated entries (input --> output)
    # --> when excluding reviews/surveys --> get titles for "related works"
    print("This is a Tabajara SLR helper script which aims to " \
          "remove duplicated entries and, maybe, do some more good stuff.")
    args = sys.argv[1:]
    if not len(args) > 2:
        sys.exit("Usage: python3 slr_helper.py 1 input_file.csv output_file.csv related_works_file.csv \n" \
                 "Usage: python3 slr_helper.py 2 input_file1.csv input_file2.csv relevants.csv irrelevants.csv undefined.csv")
    command = args[0]
    print(command)
    if command == "1":
        if not len(args) == 4:
            sys.exit("You should specify three .csv files: one input and two outputs.")
        first_phase(args)
    elif command == "2":
        if not len(args) == 6:
            sys.exit("You should specify five .csv files: two inputs and three outputs.")
        second_phase(args)
    else: 
        print("You have to specify 1 for first phase or 2 for second phase.")

if __name__ == "__main__":
    main()
