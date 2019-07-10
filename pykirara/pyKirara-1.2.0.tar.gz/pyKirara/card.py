from .idol import Idol
from .skills import Skill, LeadSkill
from .enums import enum, attributes
from .errors import CategoryNotFound

class Card:
    """
    Represents a Card and its data

    Attributes
    ----------
    card_id : int
        The card's card id

    album_id : int
        The card's album id

    type : str
        The card's type (Cool, Cute, Passion, Office)

    image : str
        The card's image API link

    has_spread : bool
        True if the card has a spread image, otherwise false

    icon : str
        The card's icon link    

    chara_id : int
        The card's character id
    
    chara : Idol
        An Idol object using the card's idol data

    evo_id : int
        The card's evolution id of transformed card

    evo_type : int
        The card's evolution rarity type (From R to SSR)

    grow_type : int
        An integer that represents a boolean value, checks if card can grow or not

    name : str
        The card's name

    title : str
        The card's untranslated title

    open_dress_id : int
        The card's model id

    place : int
        The card's place value

    pose : int
        The card's sprite number

    series_id : int
        The evolution chain id of the card

    skill : Skill
        The card's skill info in a Skill object

    lead_skill : LeadSkill
        The card's lead skill info in a Lead Skill object

    rarity : Rarity
        Represents the card's rarity data in a Rarity object

    min_vocal : int
        The card's minimum vocal value

    max_vocal : int
        The card's maximum vocal value

    bonus_vocal : int
        The card's bonus vocal value

    min_dance : int
        The card's minimum dance value

    max_dance : int
        The card's maximum dance value

    bonus_dance : int
        The card's bonus dance value

    min_visual : int
        The card's minimum visual value

    max_visual : int
        The card's maximum visual value

    bonus_visual : int
        The card's bonus visual value

    min_hp : int
        The card's minimum health value

    max_hp : int
        The card's maximum health value

    bonus_hp : int
        The card's bonus health value

    """
    def __init__(self, card_data: dict):
        self.card_id = card_data['id']
        self.album_id = card_data['album_id']
        self.type = card_data['attribute']

        self.image = card_data['card_image_ref']
        self.has_spread = card_data['has_spread']
        self.icon = card_data['icon_image_ref']
        self.sprite = card_data['sprite_image_ref']
        self.spread = card_data['spread_image_ref']
        self.sign = card_data['sign_image_ref']

        self.chara_id = card_data['chara_id']
        self.chara = Idol(card_data['chara'])
        self.evo_id = card_data['evolution_id']
        self.evo_type = card_data['evolution_type']
        self.grow_type = card_data['grow_type']
        self.name = card_data['name']
        self.title = card_data['title']
        self.open_dress_id = card_data['open_dress_id']
        self.place = card_data['place']
        self.pose = card_data['pose']
        self.series_id = card_data['series_id']
        self.lead_skill = LeadSkill(card_data['lead_skill'])
        self.skill = Skill(card_data['skill'])
        self.rarity = Rarity(card_data['rarity'])

        self.min_vocal = card_data['vocal_min']
        self.max_vocal = card_data['vocal_max']
        self.bonus_dance = card_data['bonus_dance']

        self.min_dance = card_data['dance_min']
        self.max_dance = card_data['dance_max']
        self.bonus_dance = card_data['bonus_dance']

        self.min_visual = card_data['visual_min']
        self.max_visual = card_data['visual_max']
        self.bonus_visual = card_data['bonus_visual']

        self.min_hp = card_data['hp_min']
        self.max_hp = card_data['hp_max']
        self.bonus_hp = card_data['bonus_hp']

    def min_max_stats(self, stat: str, level: int):
        """Calculates the value of a stat in a specific level
    
        Returns
        -------
        int
            Value of stat in specified level
        """
        if stat == 'dance':
            dance_formula = self.min_dance + (self.max_dance - self.min_dance) * (level/self.rarity.base_max_level)

            return round(dance_formula)

        elif stat == 'visual':
            visual_formula = self.min_visual + (self.max_visual - self.min_visual) * (level/self.rarity.base_max_level)

            return round(visual_formula)

        elif stat == 'vocal':
            vocal_formula = self.min_vocal + (self.max_vocal - self.min_vocal) * (level/self.rarity.base_max_level)

            return round(vocal_formula)

class Rarity:
    """Represent a Card's rarity data
    
    Attributes
    ----------
    rarity : int
        An int representing how rare the card is
    base_max_level : int
        A number that is the level cap of the card
    add_max_level : int
        A number that is how many levels the card can possibly have
    max_love : int
        The max amount of love that can be obtained
    base_give_money : int
        The amount of money the card gives if the card is retired
    base_give_exp : int
        The amount of exp the card give if they are used as exp fodder
    add_param : int
        ???
    max_star_rank : int
        The cap that the card can get by increasing star rank
    """
    def __init__(self, rarity_data: dict):
        self.rarity = rarity_data['rarity']
        self.base_max_level = rarity_data['base_max_level']
        self.add_max_level = rarity_data['add_max_level']
        self.max_love = rarity_data['max_love']
        self.base_give_money = rarity_data['base_give_money']
        self.base_give_exp = rarity_data['base_give_exp']
        self.add_param = rarity_data['add_param']
        self.max_star_rank = rarity_data['max_star_rank']
        