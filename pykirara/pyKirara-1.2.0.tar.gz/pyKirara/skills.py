class Skill:
    """Represents a Skill and its Data

    Attributes
    ----------
    id : int
        The Skill's ID
    name : str
        The Skill's name
    explain : str
        An untranslated explanation of the skill
    en_explain : str
        A machine translated explanation of the skill
    skill_type : str
        The Skill's type
    judge_type : int
        ????
    trigger_type : int
        ????
    trigger_value : int
        ????
    cutin_type : int
        ????
    condition : int
        ????
    value : int
        ????
    value_2 : int
        ????
    max_chance : int
        percent stuff
    max_duration : int
        The max duration of how long the skill last in milliseconds
    skill_type_id : int
        The skill type's id
    effect_length : dict
        A dict of the minimum and max value of the how long the skill's effect
        last
    proc_chance : dict
        A dict of the minimum and max value of the probability the skill will
        take effect
    """
    def __init__(self, skill_data: dict):
        self.id = skill_data['id']
        self.name = skill_data['skill_name']
        self.explain = skill_data['explain']
        self.en_explain = skill_data['explain_en']

        self.skill_type = skill_data['skill_type']
        self.judge_type = skill_data['judge_type']
        self.trigger_type = skill_data['skill_trigger_type']
        self.trigger_value = skill_data['skill_trigger_value']

        self.cutin_type = skill_data['cutin_type']
        self.condition = skill_data['condition']

        self.value = skill_data['value']
        self.value_2 = skill_data['value_2']

        self.max_chance = skill_data['max_chance']
        self.max_duration = skill_data['max_duration']
        self.skill_type_id = skill_data['skill_type_id']
        self.effect_length = skill_data['effect_length']
        self.proc_chance = skill_data['proc_chance']


class LeadSkill:
    """Represents a Lead Skill and it's data

    Attributes
    ----------
    id : int
        The Skill's ID
    name : str
        The Skill's name
    explain : str
        An untranslated explanation of the skill
    en_explain : str
        A machine translated explanation of the skill
    need_cute : bool
        A bool value if the skill requires a Cute Idol
    need_cool : bool
        A bool value if the skill requires a Cool Idol
    need_passion : bool
        A bool value if the skill requires a Passion Idol
    target_attribute : str
        What attribute the skill affects
    target_attribute_2 : str
        Another attribute the skill affects
    target_param : str
        What parameter the skill affects (Visual, Vocal, etc.)
    target_param : str
        Another parameter the skill affects
    up_type : int
        ???
    up_type_2 : int
        ???
    up_value : int
        ???
    up_value_2 : int
        ???
    special_id : int
        The skill's special ID
    need_chara : str
        If the skill needs a specific character
    """
    def __init__(self, skill_data: dict):
        self.id = skill_data['id']
        self.name = skill_data['name']
        self.explain = skill_data['explain']
        self.en_explain = skill_data['explain_en']
        self.type = skill_data['type']

        self.need_cute = bool(skill_data['need_cute'])
        self.need_cool = bool(skill_data['need_cool'])
        self.need_passion = bool(skill_data['need_passion'])

        self.target_attribute = skill_data['target_attribute']
        self.target_attribute_2 = skill_data['target_attribute_2']
        self.target_param = skill_data['target_param']
        self.target_param_2 = skill_data['target_param_2']

        self.up_type = skill_data['up_type']
        self.up_type_2 = skill_data['up_type_2']
        self.up_value = skill_data['up_value']
        self.up_value_2 = skill_data['up_value_2']

        self.special_id = skill_data['special_id']
        self.need_chara = skill_data['need_chara']
