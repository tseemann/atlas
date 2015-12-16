import os
import json
from atlas.utils import unique
from atlas.utils import flatten
from pprint import pprint
class BasePredictor(object):

    def __init__(self, typed_variants, called_genes, sample = ""):
        self.typed_variants = typed_variants
        self.called_genes = called_genes
        self.drugs = self._get_drug_list_from_variant_to_resistance_drug()
        self.resistance_prediction = self._create_initial_resistance_prediction()
        self.sample = sample
        self.out_json = {sample : {}}  
        self.out_json[self.sample]["typed_variants"] = {} 
        out_json = self.out_json[self.sample]["typed_variants"]
        for name, tvs in typed_variants.iteritems():
            for tv in tvs:
                try:
                    out_json[name].append(tv.to_dict())
                except KeyError:
                    out_json[name] = tv.to_dict()              

    def _create_initial_resistance_prediction(self):
        self.resistance_predictions =  dict((k,"I") for k in self.drugs)

    def _get_drug_list_from_variant_to_resistance_drug(self):
        return unique(flatten(self.variant_to_resistance_drug.values()))

    def predict_antibiogram(self):
        for name, variants in self.typed_variants.iteritems():
            for variant in variants: 
                self._update_resistance_prediction(variant)
        for name, gene in self.called_genes.iteritems():
            self._update_resistance_prediction(gene)

    def _update_resistance_prediction(self, variant_or_gene):
        try:
            drugs = self.variant_to_resistance_drug[variant_or_gene.alt_name]
        except KeyError:
            talt_name = list(variant_or_gene.alt_name)
            talt_name[-1] = "X"
            drugs = self.variant_to_resistance_drug["".join(talt_name)]
        resistance_prediction = self._resistance_prediction(variant_or_gene)
        for drug in drugs:
            current_resistance_prediction = self.resistance_predictions.get(drug)
            assert resistance_prediction is not None
            if current_resistance_prediction in ["I", "N"]:
                self.resistance_predictions[drug] = resistance_prediction
            elif current_resistance_prediction == "S":
                if resistance_prediction  in ["r", "R"]:
                    self.resistance_predictions[drug] = resistance_prediction
            elif current_resistance_prediction == "r":
                if resistance_prediction == "R":
                    self.resistance_predictions[drug] = resistance_prediction

    def _resistance_prediction(self, variant_or_gene):
        if variant_or_gene.gt == "1/1":
            return "R"
        elif variant_or_gene.gt == "0/1":
            return "r"
        elif variant_or_gene.gt == "0/0":
            return "S"
        else:
            return "I"

    def run(self):
        self.predict_antibiogram()
        self.out_json[self.sample]["susceptibility"] = self.resistance_predictions
        pprint(self.out_json)
  

class TBPredictor(BasePredictor):

    def __init__(self, typed_variants, called_genes, sample = ""):
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/predict/tb/' ))
        print os.path.join(self.data_dir, "variant_to_resistance_drug.json")
        self.variant_to_resistance_drug = load_json(os.path.join(self.data_dir, "variant_to_resistance_drug.json"))
        super(TBPredictor, self).__init__(typed_variants, called_genes, sample)

def load_json(f):
    with open(f, 'r') as infile:
        return json.load(infile)




