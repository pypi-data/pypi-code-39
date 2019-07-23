import termcolor

from .abstract_validator import AbstractValidator


class FillRateValidator(AbstractValidator):
    """
    Checks the percentage of each columns which is null or blank and warns if it's greater than some cutoff.
    To add a new fill rate check, just define a boolean mask and pass to `checkFillRateInner`
    """
    PERC_CUTOFF = 40

    def __init__(self, data):
        self.data = data

    def announce(self):
        print(termcolor.colored("Checking for fill rate issues...", "blue"))

    def validate(self):
        percNullDf = self.data.isna().mean() * 100
        percBlankDf = self.data.astype(str).apply(lambda x: x == "", axis=0).mean() * 100
        FillRateValidator.validateInner(percNullDf, "null")
        FillRateValidator.validateInner(percBlankDf, "blanks")

    @staticmethod
    def validateInner(mask, desc):
        concerningColsWithPercentages = mask[mask > FillRateValidator.PERC_CUTOFF]
        if len(concerningColsWithPercentages) > 0:
            message = "WARNING: {} columns have a high percentage (> {}%) of {}. " \
                      "Are you sure you scraped correctly?\n{}\n"\
                .format(len(concerningColsWithPercentages), FillRateValidator.PERC_CUTOFF, desc,
                        concerningColsWithPercentages)
            print(termcolor.colored(message, "yellow"))
        return concerningColsWithPercentages
