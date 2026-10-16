class RoundRobinService:

    @staticmethod
    def generate_schedule(
        players
    ):

        matches = []

        for i in range(
            len(players)
        ):

            for j in range(
                i + 1,
                len(players)
            ):

                matches.append({

                    "player1":
                    players[i],

                    "player2":
                    players[j]

                })

        return matches
