class BadgeService:

    @staticmethod
    def get_badges(player):

        badges = []

        highest_dupr = max(
            player.get(
                "currentDuprSingles",
                3.5
            ),
            player.get(
                "currentDuprDoubles",
                3.5
            )
        )

        previous_dupr = max(
            player.get(
                "previousDuprSingles",
                highest_dupr
            ),
            player.get(
                "previousDuprDoubles",
                highest_dupr
            )
        )

        #
        # Match Badges
        #

        if player["wins"] >= 10:
            badges.append("🏅 10 Wins Club")

        if player["wins"] >= 25:
            badges.append("🥈 25 Wins Club")

        if player["wins"] >= 50:
            badges.append("🥇 50 Wins Club")

        #
        # Experience Badges
        #

        if player["matchesPlayed"] >= 25:
            badges.append("🏓 Active Player")

        if player["matchesPlayed"] >= 50:
            badges.append("💪 Veteran")

        if player["matchesPlayed"] >= 100:
            badges.append("👑 Club Legend")

        #
        # Win Percentage Badges
        #

        if (
            player["matchesPlayed"] >= 10
            and player["winPercentage"] >= 60
        ):
            badges.append("🔥 Consistent Winner")

        if (
            player["matchesPlayed"] >= 10
            and player["winPercentage"] >= 75
        ):
            badges.append("🚀 Elite Performer")

        #
        # DUPR Badges
        #

        if highest_dupr >= 3.5:
            badges.append("⭐ Intermediate")

        if highest_dupr >= 4.0:
            badges.append("🌟 Advanced")

        if highest_dupr >= 4.5:
            badges.append("💎 Expert")

        if highest_dupr >= 5.0:
            badges.append("🏆 Pro Level")

        if (
            highest_dupr
            - previous_dupr
        ) >= 0.10:
            badges.append("📈 Rising Star")

        return badges