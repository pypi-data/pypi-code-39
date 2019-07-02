class GenericWorklog:
    def __init__(self, projectKey=None, issueKey=None, dateTime=None, durationInSeconds=None, description=None):
        self.projectKey = projectKey
        self.issueKey = issueKey
        self.durationInSeconds = durationInSeconds
        self.description = description
        self.dateTime = dateTime

    def __format__(self, format):
        if format == 'human':
            value = "{}\n{}\n{}\n{}\n{}".format(
                self.projectKey,
                self.issueKey,
                self.dateTime,
                self.durationInSeconds,
                self.description,
            )

            return value

        return "{} {} {} {} {}".format(
            self.projectKey,
            self.issueKey,
            self.dateTime.strftime('%d-%m-%Y'),
            self.durationInSeconds,
            self.description,
        )
