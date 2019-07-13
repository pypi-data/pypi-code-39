
from thisamericanlife.html.base import BaseHtmlParser


def all_text_of_first_item(el):
    txt = None

    try:
        txt = ' '.join([eli.text_content().strip() for eli in el])
    except:
        pass

    return txt or None


class EpisodeHtml(BaseHtmlParser):
    METADATA_PATH = '//div[@id="content"]//header[@class="episode-header"]'
    ACT_PATH = '//div[@id="content"]//div[contains(@class, "field-acts")]//article[@data-type="act"]'

    def _parse_ep_number_and_date(self, el):
        res = dict.fromkeys(['episode_number', 'date_on_air'])

        el_text = all_text_of_first_item(el) or ''

        split_parts = el_text.split(' ')
        if split_parts:
            if split_parts[0].strip().isdigit():
                res['episode_number'] = int(split_parts[0].strip())

            if len(split_parts) > 1:
                res['date_on_air'] = ' '.join(split_parts[1:])

        return res

    def _parse_act(self, act_el):
        return dict(
            episode_id=act_el.get('data-episode-id'),
            act_name=all_text_of_first_item(act_el.xpath('.//h2[@class="act-header"]')),
            act_summary=all_text_of_first_item(act_el.xpath('.//p')),
        )


    def extract_episode_metadata(self):
        header_element = self.document_tree.xpath(EpisodeHtml.METADATA_PATH)[0]

        return dict(
            self._parse_ep_number_and_date(header_element.xpath('.//div[@class="meta"]')),
            title=all_text_of_first_item(header_element.xpath('.//div[@class="episode-title"]')),
            description=all_text_of_first_item(header_element.xpath('.//div[contains(@class,"field-name-body")]'))
        )

    def extract_acts(self):
        return [self._parse_act(act) for act in self.document_tree.xpath(EpisodeHtml.ACT_PATH)]

    def to_json(self):
        return dict(
            episode_metadata=self.extract_episode_metadata(),
            act_summaries=self.extract_acts()
        )
