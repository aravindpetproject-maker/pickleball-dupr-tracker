from services.rating_service import RatingService

RatingService.add_rating_history({
    "playerId": 1,
    "previousRating": 3.5,
    "newRating": 3.6,
    "ratingChange": 0.1
})

print(RatingService.get_history())