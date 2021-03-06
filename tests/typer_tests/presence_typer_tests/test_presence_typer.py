from unittest import TestCase
from mykatlas.typing import ProbeCoverage
from mykatlas.typing import SequenceProbeCoverage
from mykatlas.typing import PresenceTyper


class PresenceTyperTest(TestCase):

    def setUp(self):
        self.pt = PresenceTyper(expected_depths=[100])
        self.pt_10 = PresenceTyper(expected_depths=[10])

    def teardown(self):
        pass

    def test_base_case_no_coverage(self):
        pc = ProbeCoverage(min_depth=0,
                           percent_coverage=0,
                           median_depth=0)
        s1 = SequenceProbeCoverage(name="A123T",
                                   probe_coverage=pc
                                   )
        call = self.pt.type(s1)
        assert call.genotype == [0, 0]

    def test_genotyping_gene_11(self):

        pc = ProbeCoverage(min_depth=100,
                           percent_coverage=100,
                           median_depth=100)
        s = SequenceProbeCoverage(name="A123T",
                                  probe_coverage=pc,
                                  percent_coverage_threshold=80

                                  )
        call = self.pt.type(s)
        assert call.genotype == [1, 1]

    def test_genotyping_gene_01(self):

        pc = ProbeCoverage(min_depth=100,
                           percent_coverage=82,
                           median_depth=2)
        s = SequenceProbeCoverage(name="A123T",
                                  probe_coverage=pc,
                                  percent_coverage_threshold=80

                                  )
        call = self.pt.type(s)
        assert call.genotype == [0, 1]

    def test_resistotype_gene_at_high_CN(self):

        pc = ProbeCoverage(min_depth=100,
                           percent_coverage=100,
                           median_depth=1000)
        s = SequenceProbeCoverage(name="A123T",
                                  probe_coverage=pc,
                                  percent_coverage_threshold=80

                                  )
        call = self.pt.type(s)
        assert call.genotype == [1, 1]

    def test_low_coverage(self):

        pc = ProbeCoverage(min_depth=100,
                           percent_coverage=16,
                           median_depth=16)
        s = SequenceProbeCoverage(name="A123T",
                                  probe_coverage=pc,
                                  percent_coverage_threshold=80

                                  )
        call = self.pt_10.type(s)
        assert call.genotype == [0, 0]

        pc = ProbeCoverage(min_depth=100,
                           percent_coverage=80,
                           median_depth=16)
        s = SequenceProbeCoverage(name="A123T",
                                  probe_coverage=pc,
                                  percent_coverage_threshold=80

                                  )
        call = self.pt_10.type(s)
        assert call.genotype == [1, 1]


class PresenceTyperTestWithContaim(TestCase):

    def setUp(self):
        self.pt_no_contaim = PresenceTyper(expected_depths=[100])
        self.pt_contaim = PresenceTyper(
            expected_depths=[100],
            contamination_depths=[10])

    def teardown(self):
        pass

    def test_genotyping_gene_01(self):

        pc = ProbeCoverage(min_depth=10,
                           percent_coverage=100,
                           median_depth=10)
        s = SequenceProbeCoverage(name="A123T",
                                  probe_coverage=pc,
                                  percent_coverage_threshold=80

                                  )
        call = self.pt_no_contaim.type(s)
        assert call.genotype == [0, 1]
        call = self.pt_contaim.type(s)
        assert call.genotype == [0, 0]

    def test_genotyping_gene_11(self):
        pt_no_contaim = PresenceTyper(expected_depths=[20])
        pt_contaim = PresenceTyper(
            expected_depths=[20],
            contamination_depths=[10])

        pc = ProbeCoverage(min_depth=10,
                           percent_coverage=100,
                           median_depth=10)
        s = SequenceProbeCoverage(name="A123T",
                                  probe_coverage=pc,
                                  percent_coverage_threshold=80

                                  )
        call = pt_no_contaim.type(s)
        assert call.genotype == [1, 1]

        call = pt_contaim.type(s)
        assert call.genotype == [0, 0]

        pc = ProbeCoverage(min_depth=10,
                           percent_coverage=100,
                           median_depth=30)
        s = SequenceProbeCoverage(name="A123T",
                                  probe_coverage=pc,
                                  percent_coverage_threshold=80

                                  )
        call = pt_no_contaim.type(s)
        assert call.genotype == [1, 1]

        call = pt_contaim.type(s)
        assert call.genotype == [1, 1]

        pc = ProbeCoverage(min_depth=10,
                           percent_coverage=100,
                           median_depth=20)
        s = SequenceProbeCoverage(name="A123T",
                                  probe_coverage=pc,
                                  percent_coverage_threshold=80

                                  )
        call = pt_no_contaim.type(s)
        assert call.genotype == [1, 1]

        call = pt_contaim.type(s)
        assert call.genotype == [1, 1]
