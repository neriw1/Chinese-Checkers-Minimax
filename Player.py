class Player:
    def __init__(self, number, type=0):
        """

        :param type: 0 for human 1 for computer
        """
        self.type = type
        self.number = number
        if type == 0:
            self.name = f"regular-player{number}"
        elif type == 1:
            self.name = f"computer-player{number}"
        elif type == 2:
            self.name ==f"random-player{number}"
        self.color = None