import logging

log = logging.getLogger('portiaitempipelineutils.PortiaItemsPipelineUtils')

class ReplaceDashesFields(object):
    """A pipeline to replece item field starting with dashes."""
    def process_item(self, item, spider):
        log.info('ReplaceDashesFields, process_item started...')
        for field in item:
            if field.startswith("_"):
                newfield=field.replace('_', '')
                item[newfield]=item[field]
                del item[field]
                log.info('ReplaceDashesFields, process_item: field %s = %r' % (field,str(newfield)))
        return item

