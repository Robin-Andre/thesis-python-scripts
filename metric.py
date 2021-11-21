import evaluation

default_path = "output/calibration/throwaway/"


class Metric:

    def __init__(self, raw_data):
        self.data_frame = None

    def draw(self, resolution=1):
        pass

    def difference(self, metric, resolution=1):
        pass

    def verify(self):
        return True


class TrafficDemand(Metric):

    def __init__(self, raw_data):
        super().data_frame = evaluation.evaluate_modal()

    def draw(self, resolution=1):
        pass

    def difference(self, metric, resolution=1):
        pass

    def verify(self):
        pass


class TravelTime(Metric):
    def __init__(self, raw_data):
        pass

    def draw(self, resolution=1):
        pass

    def difference(self, metric, resolution=1):
        pass

    def verify(self):
        pass


class TravelDistance(Metric):
    def __init__(self, raw_data):
        pass

    def draw(self, resolution=1):
        pass

    def difference(self, metric, resolution=1):
        pass

    def verify(self):
        pass
