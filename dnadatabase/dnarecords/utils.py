
from models import Sequence

class SequenceCreator:

    def __init__(self, id) -> None:
        self.sequence = Sequence.objects.create(id=id)
