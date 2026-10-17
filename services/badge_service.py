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

        wins = player.get(
            "wins",
            0
        )

        matches_played = player.get(
            "matchesPlayed",
            0
        )

        win_percentage = player.get(
            "winPercentage",
            0
        )

        # Match Badges

        if wins >= 10:
            badges.append("🏅 10 Wins Club")

        if wins >= 25:
            badges.append("🥈 25 Wins Club")

        if wins >= 50:
            badges.append("🥇 50 Wins Club")

        # Experience Badges

        if matches_played >= 25:
            badges.append("🏓 Active Player")

        if matches_played >= 50:
            badges.append("💪 Veteran")

        if matches_played >= 100:
            badges.append("👑 Club Legend")

        # Win Percentage Badges

        if (
            matches_played >= 10
            and
            win_percentage >= 60
        ):
            badges.append("🔥 Consistent Winner")

        if (
            matches_played >= 10
            and
            win_percentage >= 75
        ):
            badges.append("🚀 Elite Performer")

        # DUPR Badges

        if highest_dupr >= 3.5:
            badges.append("⭐ Intermediate")

        if highest_dupr >= 4.0:
            badges.append("🌟 Advanced")

        if highest_dupr >= 4.5:
            badges.append("💎 Expert")

        if highest_dupr >= 5.0:
            badges.append("🏆 Pro Level")

        if (
            highest_dupr -
            previous_dupr
        ) >= 0.10:
            badges.append("📈 Rising Star")

        return badges