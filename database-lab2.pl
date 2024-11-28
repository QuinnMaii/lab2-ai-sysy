% Houses at Hogwarts and their characteristics
house(gryffindor, ['brave','courageous', 'adventurous', 'determined']).
house(hufflepuff, ['loyalty','hardworking', 'patient', 'fair']).
house(ravenclaw, ['wisdom','intelligent', 'creative', 'curious']).
house(slytherin, ['ambition','resourceful', 'cunning', 'ambitious']).

% Subjects available at Hogwarts
subject(potions).
subject(transfiguration).
subject(defense_against_the_dark_arts).
subject(herbology).
subject(astronomy).
subject(charms).
subject(history_of_magic).
subject(divination).
subject(care_of_magical_creatures).
subject(alchemy).

% Careers and required subjects
career(auror, [defense_against_the_dark_arts, potions, transfiguration, charms]).
career(healer, [herbology, potions, charms, alchemy]).
career(teacher, [transfiguration, herbology, history_of_magic]).
career(astronomer, [astronomy, divination]).
career(magizoologist, [care_of_magical_creatures, herbology, potions]).
career(alchemist, [alchemy, potions, transfiguration]).
career(curse_breaker, [defense_against_the_dark_arts, charms, history_of_magic]).
career(enchanter, [charms, alchemy, transfiguration]).
career(historian, [history_of_magic, divination]).
career(ministry_official, [history_of_magic, charms, defense_against_the_dark_arts]).

% Rule for house classification based on traits
classify_by_traits(Traits, gryffindor) :-
    house(gryffindor, GryffindorTraits),
    intersection(Traits, GryffindorTraits, CommonTraits),
    CommonTraits \= []. % Ensure there is at least one matching trait

classify_by_traits(Traits, hufflepuff) :-
    house(hufflepuff, HufflepuffTraits),
    intersection(Traits, HufflepuffTraits, CommonTraits),
    CommonTraits \= [].

classify_by_traits(Traits, ravenclaw) :-
    house(ravenclaw, RavenclawTraits),
    intersection(Traits, RavenclawTraits, CommonTraits),
    CommonTraits \= [].

classify_by_traits(Traits, slytherin) :-
    house(slytherin, SlytherinTraits),
    intersection(Traits, SlytherinTraits, CommonTraits),
    CommonTraits \= [].

% Utility rule: intersection
intersection([], _, []).
intersection([H|T], List, [H|Result]) :- member(H, List), intersection(T, List, Result).
intersection([_|T], List, Result) :- intersection(T, List, Result).

% Rule for checking age eligibility for Hogwarts
eligible_age(Age) :- Age >= 11, Age =< 18.

% Suggest careers based on favorite subjects
suggest_career(Subjects, Career) :-
    career(Career, RequiredSubjects),
    intersection(RequiredSubjects, Subjects, CommonSubjects),
    CommonSubjects \= [].

