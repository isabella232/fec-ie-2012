#!/usr/bin/env python

import argparse
import sys

import csvkit

class FEC(object):
    """
    Process FEC data dumps.
    """
    def __init__(self):
        self.argparser = argparse.ArgumentParser(
            description='A command line utility for processing FEC data dumps.'
        )

        self.argparser.add_argument(
            dest='input', action='store',
            help='Path to input CSV.'
        )

        self.argparser.add_argument(
            dest='output', action='store',
            help='Path to output CSV.'
        )

        self.argparser.add_argument(
            '-a', '--amendments',
            dest='keep_amendments', action='store_true',
            help='Keep amendments (instead of filtering them out).'
        )

        self.argparser.add_argument(
            '-o', '--office',
            dest='office', action='store',
            help='Filter output only a certain office.'
        )

        self.args = self.argparser.parse_args()

        self.amended_ids = set()

        # Read input data
        with open(self.args.input) as f:
            reader = csvkit.reader(f)
            self.header = reader.next()
            rows = list(reader)

        sys.stdout.write('Read %i rows\n' % len(rows))

        # Discover amendments
        if not self.args.keep_amendments:
            for row in rows:
                if row[self.header.index('amn_ind')] != 'N':
                    self.amended_ids.add(row[self.header.index('prev_file_num')])

        # Filter data
        output_rows = filter(self.filter_row, rows)

        sys.stdout.write('Saving %i rows\n' % len(output_rows))

        # Write output
        with open(self.args.output, 'w') as f:
            writer = csvkit.writer(f)
            writer.writerow(self.header)

            writer.writerows(output_rows)

    def filter_row(self, row):
        """
        Filter an individual row based on arguments.
        """
        if self.args.office:
            if row[self.header.index('can_off')] != self.args.office:
                return False

        if not self.args.keep_amendments:
            if row[self.header.index('file_num')] in self.amended_ids:
                return False

        return True

if __name__ == '__main__':
    FEC()
