import common
from view import screen, images

temple_commands = "(F)ull Healing, (P)artial Healing, (L)eave Temple"


#  This function controls the interactions at the temple.
def enter_the_temple(our_hero):
    is_leaving_temple = False
    message = "Welcome to Wudang Five Immortals Temple, weary traveler. How can we help you?"
    left_pane = images.tall_temple

    while not is_leaving_temple:
        right_pane = draw_healing_list(our_hero)
        screen.paint(screen.State(
            common.get_stats(None, our_hero),
            temple_commands,
            message,
            left_pane,
            right_pane
        ))
        next_move = input("Next? ")
        if next_move.lower() == "f":
            if our_hero.hit_points != our_hero.max_hit_points:  # Make sure we need healing
                if our_hero.gold >= full_price(our_hero):
                    our_hero.gold = our_hero.gold - full_price(our_hero)
                    our_hero.hit_points = our_hero.max_hit_points
                    message = "The temple priests pray over you and you are fully healed!"
                else:
                    message = "You do not have enough gold!"
            else:
                message = "You are healthy! You don't need healing!"
        if next_move.lower() == "p":
            if our_hero.hit_points != our_hero.max_hit_points:  # Make sure we need healing
                if our_hero.gold >= half_price(our_hero):
                    our_hero.gold -= half_price(our_hero)
                    our_hero.hit_points += half_percent(our_hero)
                    message = "The temple priests pray over you and you feel much better!"
                else:
                    message = "You do not have enough gold!"
            else:
                message = "You are healthy! You don't need healing!"
        # Go back into the town
        if next_move.lower() == "l":
            is_leaving_temple = True


def full_price(our_hero):
    return round((our_hero.max_hit_points - our_hero.hit_points) / 2)


def half_price(our_hero):
    return round(full_price(our_hero) / 2)


def half_percent(our_hero):
    full_percent = round(our_hero.max_hit_points - our_hero.hit_points)
    return round(full_percent / 2)


# List out the various healing that our hero can have
def draw_healing_list(our_hero):
    border = "<================<o>================>\n"
    full_percent = round(our_hero.max_hit_points - our_hero.hit_points)

    response = border
    response += " Description     | % Healed | Cost" + '\n'
    response += border
    response += " Full Healing    | " + common.front_padding(str(full_percent), 7) + "% | " \
                + common.front_padding(str(full_price(our_hero)), 4) + '\n'
    response += " Partial Healing | " + common.front_padding(str(half_percent(our_hero)), 7) + "% | " \
                + common.front_padding(str(half_price(our_hero)), 4) + '\n'
    response += border
    return response
