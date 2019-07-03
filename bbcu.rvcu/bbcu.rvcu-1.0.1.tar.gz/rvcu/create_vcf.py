import os

MIN_RATIO_MUTATION_OTHER = 1


class MutationClassifier(object):
    """Select UMI with maximum mutations Classify the mutation of the to groups, and create csv files.

    Args:
        locations                   (OrderedDict of int: Location objects):
                                        keys - sorted locations of the mutation on the reference genome.
                                        values - Location object that contain information on the mutations in specific
                                        location on the genome. Accepted from LocationsWithMutations object
        chr                         (str): name of the chromosome. For example: chr1
        chr_start                   (int): start coordinate on chromosome, run only from this coordinate
        chr_end                     (int): end coordinate on chromosome, run only until this coordinate
        classifier_output_file_name (str): prefix of file name (for example sample name)
        classes_stat                (dict of str: int):  number of mutation in each class
                                        keys - class of mutation (I.e. A,B,C,D,E,EB,EB_star etc.)
                                        values - number of mutations
        print_header                (bool): print header only in the first iteration
        eb_star_class_threshold     (float): threshold of EB_star class
        serial_file_number          (int): each batch of chromosome creates separate file. In the end we concatenates
                                        them with the method cat_classifications_files

    Attributes:
        classifier_output_file_name_temp    (str): file name with serial file number
        rows                                (list of str): list of output lines. Including header if print_header==True
        total_mutation                      (int): total number of reads with specific mutation
        total_non_mutation                  (int): total number of reads without mutation
        total_other_mutations               (int): total number of reads with other mutation

    """

    def __init__(self, locations, chr, chr_start, chr_end, classifier_output_file_name, classes_stat,
                 print_header, eb_star_class_threshold, serial_file_number):
        self.locations = locations
        self.chr = chr
        self.chr_start = chr_start
        self.chr_end = chr_end
        self.eb_star_class_threshold = eb_star_class_threshold
        self.classifier_output_file_name = classifier_output_file_name + '_classification_Crom_'
        file_name = os.path.basename(self.classifier_output_file_name)
        dirname = os.path.dirname(self.classifier_output_file_name)
        self.classifier_output_file_name_temp = os.path.join(dirname, str(serial_file_number) + "_" + file_name)
        if 'ABC_EB-star_mut_types' not in classes_stat:
            classes_stat['ABC_EB-star_mut_types'] = {}
        self.classes_stat = classes_stat
        self.rows = self.get_row_header(print_header)
        self.total_mutation, self.total_non_mutation, self.total_other_mutations = (0, 0, 0)

    def get_row_header(self, print_header):
        rows_header = []
        if print_header:  # print header only in the first iteration
            rows_header = [
                ['chr', 'start', 'reference', 'mutation', 'mutation type',
                 '# of UMI fragments that are "pure" (whose reads contain the same mutation)',
                 '# of reads in "pure" fragments',
                 '# of UMI fragments that are "dirty" (some reads do not contain the same mutation)',
                 'Within UMI fragments mean fractions (without mutation vs with mutation)',
                 '# of UMIs that do not contain the mutation',
                 '# of reads in the UMIs that do not contain the mutation',
                 '# of additional UMIs with mutation (the same mutation or other)',
                 'Means of means of fractions per group (with mutation vs without mutation) for all UMIs',
                 '# of reads with mutation', '# of reads with a different mutation', '# of reads without mutation',
                 'Only in EB-star class: # of UMIs with more than one break with the same mutation in all reads (purely), only if the the fraction of this number from the number of the other UMIs without mutation is lower than 0.02']]
        return rows_header

    def print_classes(self):
        # append to file, this function print separately for each chr
        with open('%s_%s_%s_%s' % (self.classifier_output_file_name_temp, self.chr, self.chr_start, self.chr_end),
                  'w') as fo:
            for line in self.rows:
                fo.write('\t'.join(line) + "\n")

    def output_files(self):
        file_to_remove = '%s_%s_%s_%s' % (self.classifier_output_file_name_temp, self.chr, self.chr_start, self.chr_end)
        return file_to_remove

    @staticmethod
    def print_mute_type_stat(sample_name, mute_stat_output_name, classes_stat, norm=False):
        # for class_type in classes_stat.keys() + ['ABC_EB-star_mut_types']:
        for class_type in classes_stat.keys():
            filename = mute_stat_output_name + '_mute_type_stat_' + sample_name + '_' + class_type
            with open(filename, 'w') as fo:
                for mute in ['A_C', 'A_G', 'A_T', 'C_A', 'C_G', 'C_T', 'G_A', 'G_C', 'G_T', 'T_A', 'T_C', 'T_G']:
                    if mute not in classes_stat[class_type]:
                        classes_stat[class_type][mute] = str(0)
                sorted_mut_types = sorted(classes_stat[class_type].keys())
                header_line = '\t'.join([''] + sorted_mut_types)
                fo.write(header_line + "\n")
                str_values = [str(classes_stat[class_type][v]) for v in sorted_mut_types]
                line = '\t'.join([sample_name] + str_values)
                fo.write(line + "\n")

    @staticmethod
    def cat_classifications_files(classifier_output_file_name):
        os.system("cd %s; ls *%s_classification_Crom_* | sort -n | xargs cat > %s_classification.tsv" % (
            os.path.dirname(classifier_output_file_name), os.path.basename(classifier_output_file_name),
            classifier_output_file_name))
        os.system("cd %s; rm *_%s_classification_Crom_*" % (
            os.path.dirname(classifier_output_file_name), os.path.basename(classifier_output_file_name)))

    def max_mutation_rate_umi(self, location_obj, mutation):
        """Select the cleanest UMI that will used as point of reference to other UMIs.
        The criteria are: 1) most pure fragments
                          2) most of the mutated reads
                          3) most of the total reads

        Args:
            location_obj    (Location object): object with all UMIs on specific location
            mutation        (str): mutation A/C/G/T

        Returns:
            max_umi         (str): UMI that selected to be point of reference to other UMIs (the cleanest UMI)
        """
        return max(location_obj.umis.keys(),
                   key=lambda umi: (
                       location_obj.umis[umi].pure_fragments_per_mut[mutation][0] if mutation in location_obj.umis[
                           umi].pure_fragments_per_mut else 0,
                       location_obj.umis[umi].mutated_reads_num_per_mut[mutation] if mutation in location_obj.umis[
                           umi].mutated_reads_num_per_mut else 0, location_obj.umis[umi].total_reads))
        # old criterion in previous version - only accoding total number of mutated reads
        # return max(location_obj.umis.keys(),
        #            key=lambda umi: location_obj.umis[umi].mutated_reads_num_per_mut[mutation] if mutation in
        #                                                                                    location_obj.umis[
        #                                                                                        umi].mutated_reads_num_per_mut else 0)

    def update_total_reads(self, location_obj, umi, mutation):
        tot_mutation = 0
        if mutation in location_obj.umis[umi].mutated_reads_num_per_mut:
            tot_mutation = location_obj.umis[umi].mutated_reads_num_per_mut[mutation]
            self.total_mutation += tot_mutation
        tot_non_mutation = location_obj.umis[umi].no_mutated_reads_num
        self.total_non_mutation += tot_non_mutation
        self.total_other_mutations += (location_obj.umis[umi].total_reads - tot_mutation - tot_non_mutation)

    def classify_mutations(self):
        for loc in self.locations:
            all_mutations = self.locations[loc].all_mutations
            location_obj = self.locations[loc]
            for mutation in all_mutations:
                row = [location_obj.chr, str(location_obj.loc), location_obj.ref_letter,
                       mutation]  # chr, pos, ref_letter
                max_umi = self.max_mutation_rate_umi(location_obj, mutation)
                self.total_mutation, self.total_non_mutation, self.total_other_mutations = (0, 0, 0)
                pure_pos_num, pure_counts_total, dirty_pos_num, dirty_pos_ratio_mean = self.mutation_stat_on_max_umi(
                    location_obj, max_umi, mutation)
                o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_pos_num = self.mutation_stat_on_other_umis(
                    location_obj, max_umi, mutation)
                class_type = self.get_mutations_type(pure_pos_num, dirty_pos_num, o_umi_non_mut_num,
                                                     o_umi_mut_num,
                                                     o_umi_same_mut_more_than_one_fragment_pure_pos_num)
                self.update_mute_stat(location_obj, mutation, class_type)
                row += [class_type, str(pure_pos_num), str(pure_counts_total), str(dirty_pos_num),
                        str(dirty_pos_ratio_mean),
                        str(o_umi_non_mut_num), str(o_umi_non_mut_counts_total), str(o_umi_mut_num),
                        str(o_umi_mut_ratio_mean), str(self.total_mutation), str(self.total_other_mutations),
                        str(self.total_non_mutation),
                        str(o_umi_same_mut_more_than_one_fragment_pure_pos_num) if class_type == 'EB-star' else '']
                self.rows.append(row)

    def update_mute_stat(self, location_obj, mutation, class_type):
        ref_to_mut = location_obj.ref_letter + '_' + mutation
        if class_type not in self.classes_stat:
            self.classes_stat[class_type] = {}
        if ref_to_mut not in self.classes_stat[class_type]:
            self.classes_stat[class_type][ref_to_mut] = 0
        if ref_to_mut not in self.classes_stat['ABC_EB-star_mut_types']:
            self.classes_stat['ABC_EB-star_mut_types'][ref_to_mut] = 0
        self.classes_stat[class_type][ref_to_mut] += 1  # self.total_mutation
        if class_type == 'A' or class_type == 'B' or class_type == 'C' or class_type == 'EB-star':
            self.classes_stat['ABC_EB-star_mut_types'][ref_to_mut] += 1  # self.total_mutation

    def get_mutations_type(self, pure_pos_num, dirty_pos_num, o_umi_non_mut_num, o_umi_mut_num,
                           o_umi_same_mut_more_than_one_fragment_pure_pos_num):
        class_type = 'NotRecognize'
        if pure_pos_num > 1:
            if o_umi_non_mut_num > 0:
                if dirty_pos_num == 0:
                    if o_umi_mut_num == 0:
                        class_type = 'A'
                    elif o_umi_mut_num > 0:
                        class_type = 'EB'
                        if o_umi_same_mut_more_than_one_fragment_pure_pos_num and float(
                                o_umi_same_mut_more_than_one_fragment_pure_pos_num) / o_umi_non_mut_num < self.eb_star_class_threshold:
                            class_type = 'EB-star'
                elif dirty_pos_num > 0:
                    if o_umi_mut_num == 0:
                        class_type = 'EA'
                    elif o_umi_mut_num > 0:
                        class_type = 'EC'
            elif o_umi_non_mut_num == 0:
                if dirty_pos_num == 0:
                    if o_umi_mut_num == 0:
                        class_type = 'C'
                    elif o_umi_mut_num > 0:
                        class_type = 'GB'
                elif dirty_pos_num > 0:
                    if o_umi_mut_num == 0:
                        class_type = 'GA'
                    elif o_umi_mut_num > 0:
                        class_type = 'GC'

        elif pure_pos_num == 1:
            if o_umi_non_mut_num > 0:
                if dirty_pos_num == 0:
                    if o_umi_mut_num == 0:
                        class_type = 'B'
                    elif o_umi_mut_num > 0:
                        class_type = 'FB'
                elif dirty_pos_num > 0:
                    if o_umi_mut_num == 0:
                        class_type = 'FA'
                    elif o_umi_mut_num > 0:
                        class_type = 'FC'
            elif o_umi_non_mut_num == 0:
                if dirty_pos_num == 0:
                    if o_umi_mut_num == 0:
                        class_type = 'D'
                    elif o_umi_mut_num > 0:
                        class_type = 'HB'
                elif dirty_pos_num > 0:
                    if o_umi_mut_num == 0:
                        class_type = 'HA'
                    elif o_umi_mut_num > 0:
                        class_type = 'HC'
        elif pure_pos_num == 0:
            class_type = 'I'
        return class_type

    def mutation_stat_on_max_umi(self, location_obj, max_umi, mutation):
        # We output only mutations in this umi, and comare other umis to this.
        self.update_total_reads(location_obj, max_umi, mutation)
        max_umi_obj = location_obj.umis[max_umi]
        pure_frags_num = max_umi_obj.pure_fragments_per_mut[mutation][
            0] if mutation in max_umi_obj.pure_fragments_per_mut else 0
        pure_counts_total = max_umi_obj.pure_fragments_per_mut[mutation][
            1] if mutation in max_umi_obj.pure_fragments_per_mut else 0

        dirty_frags_num = len(max_umi_obj.dirty_fragments) + sum(
            [frags_num for mut, (frags_num, reads_num) in max_umi_obj.pure_fragments_per_mut.items() if
             mut != mutation])

        # dirty_frags_num = len(max_umi_obj.dirty_fragments) + sum(
        #     [frags_num for frags_num, reads_num in max_umi_obj.pure_fragments_per_mut]) - (
        #                       max_umi_obj.pure_fragments_per_mut[mutation][
        #                           0] if mutation in max_umi_obj.pure_fragments_per_mut else 0)

        # Old version:
        # print max_umi_obj.dirty_fragments, max_umi_obj.pure_fragments_per_mut
        # dirty_frags_num = len(max_umi_obj.dirty_fragments) + len(max_umi_obj.pure_fragments_per_mut) - (
        #     1 if mutation in max_umi_obj.pure_fragments_per_mut else 0)
        dirty_pos_ratio_mean = self.calculate_dirty_pos_ratio_mean(max_umi_obj, mutation)
        return pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean

    def mutation_stat_on_other_umis(self, location_obj, max_umi, mutation):
        o_umi_non_mut_num = 0
        o_umi_non_mut_counts_total = 0
        o_umi_mut_num = 0
        o_umi_same_mut_more_than_one_fragment_pure_pos_num = 0  # for EB-star class. number of other umis that contains the same mutation purely on more than one fragment.
        o_umi_mut_ratio_means_of_umis = []
        for umi in location_obj.umis:
            if umi == max_umi:
                continue
            self.update_total_reads(location_obj, umi, mutation)
            # Version 1: Only occurrence of this mutation in other umis is bad. proof of DNA mutation
            # if mutation not in location_obj.umis[umi].mutated_reads_num_per_mut:
            # Version 2: also other mutation in other umi is bad, Because it is proof to existing of different homolog so we cannot know from which our mutation came.
            umi_obj = location_obj.umis[umi]
            if not umi_obj.mutated_reads_num_per_mut:  # No mutation at all
                o_umi_non_mut_num += 1
                o_umi_non_mut_counts_total += location_obj.umis[umi].total_reads
            else:  # We have any mutation (the same or other)
                pure_frags_num = umi_obj.pure_fragments_per_mut[mutation][
                    0] if mutation in umi_obj.pure_fragments_per_mut else 0
                if pure_frags_num > 1:
                    o_umi_same_mut_more_than_one_fragment_pure_pos_num += 1
                o_umi_mut_num += 1
                o_umi_mut_ratio_means_of_umis.append(self.calculate_o_umi_mut_ratio_mean(umi_obj, mutation))
        o_umi_mut_ratio_mean = float(sum(o_umi_mut_ratio_means_of_umis)) / len(
            o_umi_mut_ratio_means_of_umis) if o_umi_mut_ratio_means_of_umis else 0
        return o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_pos_num

    def calculate_o_umi_mut_ratio_mean(self, o_umi_obj, mutation):
        pos_ratios = []
        for pos in o_umi_obj.fragments:
            pos_obj = o_umi_obj.fragments[pos]
            if not pos_obj.qry_letter_counts:
                pos_ratios.append(0.0)
                continue  # This position have no mutation
            # Version 1: Only occurrence of this mutation in other umis is bad. proof of DNA mutation
            # if mutation not in pos_obj.qry_letter_counts:
            #     continue  # This position have no mutation
            # mutation_counts = pos_obj.qry_letter_counts[mutation]
            # no_mutation_counts = pos_obj.no_mutation + pos_obj.qry_letter_counts_total - mutation_counts
            # Version 2: also other mutation in other umi is bad, Because it is proof to existing of different homolog so we cannot know from which our mutation came.
            mutation_counts = pos_obj.qry_letter_counts_total
            no_mutation_counts = pos_obj.no_mutation
            no_mutation_counts_fixed = max(no_mutation_counts, 0.5)  # To deny divide by zero
            pos_ratios.append(float(mutation_counts) / no_mutation_counts_fixed)  # ratio of position
        return float(sum(pos_ratios)) / len(pos_ratios) if pos_ratios else 0

    def calculate_dirty_pos_ratio_mean(self, max_umi_obj, mutation):
        dirty_pos_ratios = []
        for pos in max_umi_obj.fragments:
            if mutation in max_umi_obj.fragments[pos].qry_letter_counts and max_umi_obj.fragments[pos].frag_type == 1:
                continue  # It is pure postion of this mutation
            pos_obj = max_umi_obj.fragments[pos]
            mutation_counts = pos_obj.qry_letter_counts[mutation] if mutation in pos_obj.qry_letter_counts else 0
            mutation_counts_fixed = max(mutation_counts, 0.5)  # To deny divide by zero
            no_mutation_counts = pos_obj.no_mutation + pos_obj.qry_letter_counts_total - mutation_counts
            dirty_pos_ratios.append(float(no_mutation_counts) / mutation_counts_fixed)  # ratio of one position
        return float(sum(dirty_pos_ratios)) / len(
            dirty_pos_ratios) if dirty_pos_ratios else 0  # mean of ratios of fragments


class CreateVCF(object):
    """Collect the information about the mutations and create VCF file.

    Args:
        locations               (OrderedDict of int: Location objects):
                                    keys - sorted locations of the mutation on the reference genome.
                                    values - Location object that contain information on the mutations in specific
                                    location on the genome. Accepted from LocationsWithMutations object
        chr                     (str): name of the chromosome. For example: chr1
        chr_start               (int): start coordinate on chromosome, run only from this coordinate
        chr_end                 (int): end coordinate on chromosome, run only until this coordinate
        vcf_output_file_name    (str): output file name
        print_header            (bool): yes or not print header line (true only in first batch of chromosome)

    Attributes:
    """

    def __init__(self, locations, chr, chr_start, chr_end, vcf_output_file_name, print_header, serial_file_number):
        self.locations = locations
        self.chr = chr
        self.chr_start = chr_start
        self.chr_end = chr_end

        self.vcf_output_file_name = vcf_output_file_name + '_vcf_Crom_'
        file_name = os.path.basename(self.vcf_output_file_name)
        dirname = os.path.dirname(self.vcf_output_file_name)
        self.vcf_output_file_name_temp = os.path.join(dirname, str(serial_file_number) + "_" + file_name)

        # self.vcf_output_file_name = vcf_output_file_name
        self.vcf_rows_header = []
        if print_header:
            self.vcf_rows_header = [['chr', 'position', 'reference', 'mutation)',
                                     'umi1-fragment1:fragment2;umi2-fragment1:fragment2|umi1-fragment1:fragment2;umi2-fragment1:fragment2']]
        self.vcf_rows = self.vcf_rows_header

    def summar_mutations(self):
        for loc in self.locations:
            vcf_row = [self.chr, str(self.locations[loc].loc),
                       self.locations[loc].umis.values()[0].fragments.values()[0].ref_letter]  # chr, pos, ref_letter
            summary_counts = ''
            all_mutations = self.locations[loc].all_mutations
            # print loc, all_mutations
            vcf_row += '|'.join(all_mutations)
            mutations_counts = {}
            for mutation in all_mutations:
                mutations_counts[mutation] = {}
                for umi in self.locations[loc].umis:  # umi
                    mutations_counts[mutation][umi] = {}
                    for mapping_start in self.locations[loc].umis[umi].fragments:  # mapping group
                        mutations_counts[mutation][umi][mapping_start] = ''
                        # Group of the same umi's and the same mapping start
                        umi_mapping_start_group = self.locations[loc].umis[umi].fragments[mapping_start]
                        if mutation in umi_mapping_start_group.qry_letter_counts:
                            counts = umi_mapping_start_group.qry_letter_counts[mutation]
                            # Number of records with this specific location / all other records without mutation or with ohter mutation
                            mutations_counts[mutation][umi][mapping_start] += str(counts) + "/" + str(
                                umi_mapping_start_group.qry_letter_counts_total + umi_mapping_start_group.no_mutation - counts) + ":"
                            # print loc, umi, mutation, mapping_start, counts, umi_mapping_start_group.qry_letter_counts_total, umi_mapping_start_group.no_mutation
                        else:
                            mutations_counts[mutation][umi][mapping_start] += str(0) + "/" + str(
                                umi_mapping_start_group.qry_letter_counts_total + umi_mapping_start_group.no_mutation) + ":"
                            # print loc, umi, mutation, mapping_start, 0, umi_mapping_start_group.qry_letter_counts_total, umi_mapping_start_group.no_mutation

            for mutation in mutations_counts:
                for umi in mutations_counts[mutation]:
                    summary_counts += umi + "-"
                    for mapping_start in mutations_counts[mutation][umi]:
                        summary_counts += mutations_counts[mutation][umi][mapping_start]
                    summary_counts += ";"
                summary_counts += "|"

            vcf_row.append(summary_counts)
            self.vcf_rows.append(vcf_row)

            for mutation in mutations_counts:
                for umi in mutations_counts[mutation]:
                    summary_counts += umi + "-"
                    for mapping_start in mutations_counts[mutation][umi]:
                        summary_counts += mutations_counts[mutation][umi][mapping_start]
                    summary_counts += ";"
                summary_counts += "|"

    def print_vcf(self):
        # append to file, this function print separately for each chr
        with open('%s_%s_%s_%s' % (self.vcf_output_file_name_temp, self.chr, self.chr_start, self.chr_end),
                  'w') as fo:
            for line in self.vcf_rows:
                fo.write('\t'.join(line) + "\n")

    def output_files(self):
        file_to_remove = '%s_%s_%s_%s' % (
            self.vcf_output_file_name_temp, self.chr, self.chr_start, self.chr_end)
        return file_to_remove

    @staticmethod
    def cat_vcf_files(vcf_output_file_name):
        os.system("cd %s; ls *%s_vcf_Crom_* | sort -n | xargs cat > %s_vcf.tsv" % (
            os.path.dirname(vcf_output_file_name), os.path.basename(vcf_output_file_name),
            vcf_output_file_name))
        os.system("cd %s; rm *_%s_vcf_Crom_*" % (
        os.path.dirname(vcf_output_file_name), os.path.basename(vcf_output_file_name)))
