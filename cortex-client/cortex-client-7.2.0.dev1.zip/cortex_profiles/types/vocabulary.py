import attr
import pydash


__all__ = [
    "OptionalDescriber",
    "Subject",
    "Verb",
]

@attr.s(frozen=True)
class OptionalDescriber(object):
    id = attr.ib(type=str)
    adjective = attr.ib(type=str)
    adverb = attr.ib(type=str)
    include = attr.ib(type=bool)
    optionalAdjective = attr.ib(type=str)
    optionalAdverb = attr.ib(type=str)

    @optionalAdjective.default
    def defaultOptionalAdjective(self):
        if self.include:
            return self.adjective
        return ""

    @optionalAdverb.default
    def defaultOptionalAdverb(self):
        if self.include:
            return self.adverb
        return ""


@attr.s(frozen=True)
class Subject(object):
    id = attr.ib(type=str, default="")
    singular = attr.ib(type=str, default="")
    Singular = attr.ib(type=str)
    plural = attr.ib(type=str, default="")
    Plural = attr.ib(type=str)
    acronym = attr.ib(type=str, default="")

    @Singular.default
    def defaultSingular(self):
        return pydash.title_case(self.singular)

    @Plural.default
    def defaultPlural(self):
        return pydash.title_case(self.plural)


@attr.s(frozen=True)
class Verb(object):
    id = attr.ib(type=str)
    verb = attr.ib(type=str)
    past = attr.ib(type=str, default="")
    verbInitiatedBySubject = attr.ib(type=bool, default=True)
    Verb = attr.ib(type=str)
    verbStatement = attr.ib(type=str)
    Past = attr.ib(type=str)

    @Verb.default
    def defaultVerb(self):
        return pydash.title_case(self.verb)

    @Past.default
    def defaultPast(self):
        return pydash.title_case(self.past)

    @verbStatement.default
    def defaultVerbStatement(self):
        return "{} to".format(self.verb) if not self.verbInitiatedBySubject else "{} by".format(self.verb)
