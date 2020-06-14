SELECT DISTINCT(name) FROM people WHERE name IS NOT "Kevin Bacon" AND id IN
(SELECT person_id FROM stars WHERE movie_id IN
(SELECT movie_id FROM stars WHERE person_id IN
(SELECT id FROM people WHERE name = "Kevin Bacon" AND birth = 1958)));


--The person is in: (list of stars that their movies are in (list of movies that has the person of (kevin bacon)))--