import math


class DuprService:

    K = 32

    @staticmethod
    def calculate_rating_change(
        player_rating,
        opponent_rating,
        won,
        score_difference
    ):

        expected = 1 / (
            1 +
            10 ** (
                (
                    opponent_rating -
                    player_rating
                ) / 400
            )
        )

        actual = 1 if won else 0

        rating_change = (
            DuprService.K *
            (
                actual -
                expected
            )
        )

        margin_adjustment = math.log(
            score_difference + 1
        )

        return round(
            rating_change *
            margin_adjustment,
            2
        )