#!/usr/bin/env python

import csvkit

header = []
rows = []
amended_ids = []

def filter_func(row):
    if row[header.index('can_off')] != 'P':
        return False

    if row[header.index('file_num')] in amended_ids:
        return False

    return True

def main():
    global header

    with open('data.csv') as f:
        reader = csvkit.reader(f)
        header = reader.next()
        rows = list(reader)

    for row in rows:
        if row[header.index('amn_ind')] != 'N':
            amended_ids.append(row[header.index('prev_file_num')])

    output_rows = filter(filter_func, rows)

    with open('output.csv', 'w') as f:
        writer = csvkit.writer(f)
        writer.writerow(header)

        writer.writerows(output_rows)

if __name__ == '__main__':
    main()
