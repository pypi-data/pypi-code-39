import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_apigateway
import aws_cdk.aws_dynamodb
import aws_cdk.aws_lambda
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("cdk-dynamo-table-viewer", "3.0.1", __name__, "cdk-dynamo-table-viewer@3.0.1.jsii.tgz")
class TableViewer(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk-dynamo-table-viewer.TableViewer"):
    """Installs an endpoint in your stack that allows users to view the contents of a DynamoDB table through their browser."""
    def __init__(self, parent: aws_cdk.core.Construct, id: str, *, table: aws_cdk.aws_dynamodb.Table, sort_by: typing.Optional[str]=None, title: typing.Optional[str]=None) -> None:
        """
        :param parent: -
        :param id: -
        :param props: -
        :param table: The DynamoDB table to view. Note that all contents of this table will be visible to the public.
        :param sort_by: Name of the column to sort by, prefix with "-" for descending order. Default: - No sort
        :param title: The web page title. Default: - No title
        """
        props = TableViewerProps(table=table, sort_by=sort_by, title=title)

        jsii.create(TableViewer, self, [parent, id, props])

    @property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> str:
        return jsii.get(self, "endpoint")


@jsii.data_type(jsii_type="cdk-dynamo-table-viewer.TableViewerProps", jsii_struct_bases=[], name_mapping={'table': 'table', 'sort_by': 'sortBy', 'title': 'title'})
class TableViewerProps():
    def __init__(self, *, table: aws_cdk.aws_dynamodb.Table, sort_by: typing.Optional[str]=None, title: typing.Optional[str]=None):
        """
        :param table: The DynamoDB table to view. Note that all contents of this table will be visible to the public.
        :param sort_by: Name of the column to sort by, prefix with "-" for descending order. Default: - No sort
        :param title: The web page title. Default: - No title
        """
        self._values = {
            'table': table,
        }
        if sort_by is not None: self._values["sort_by"] = sort_by
        if title is not None: self._values["title"] = title

    @property
    def table(self) -> aws_cdk.aws_dynamodb.Table:
        """The DynamoDB table to view.

        Note that all contents of this table will be
        visible to the public.
        """
        return self._values.get('table')

    @property
    def sort_by(self) -> typing.Optional[str]:
        """Name of the column to sort by, prefix with "-" for descending order.

        default
        :default: - No sort
        """
        return self._values.get('sort_by')

    @property
    def title(self) -> typing.Optional[str]:
        """The web page title.

        default
        :default: - No title
        """
        return self._values.get('title')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TableViewerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["TableViewer", "TableViewerProps", "__jsii_assembly__"]

publication.publish()
