import json


class Parameters:
    def __init__(self):
        self.file_path = None
        self.parameters = None
        self.circolari_name = None
        self.circolari_rows = None
        self.comunicazioni_name = None
        self.comunicazioni_rows = None
        self.not_to_add = None
        self.all_class = None
        self.all_classes_db = None
        self.all_dest = None
        self.circ_type = None
        self.connection_string = None
        self.db_api_key_hash = None

    def init(self, file_path):
        self.file_path = file_path
        self.parameters = self.load_parameters()

        self.circolari_name = self.get_parameter('circolari_name')
        self.circolari_rows = self.get_parameter('circolari_rows')
        self.comunicazioni_name = self.get_parameter('comunicazioni_name')
        self.comunicazioni_rows = self.get_parameter('comunicazioni_rows')
        self.not_to_add = self.get_parameter('not_to_add')
        self.all_class = self.get_parameter('all_class')
        self.all_classes_db = self.get_parameter('all_classes_db')
        self.all_dest = self.get_parameter('all_dest')
        self.circ_type = self.get_parameter('circ_type')
        self.db_api_key_hash = self.get_parameter('db_api_key_hash')

    def load_parameters(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def get_parameter(self, parameter_name):
        return self.parameters.get(parameter_name)


parameters = Parameters()
