# Standard library
from textwrap import (
    dedent,
)
from typing import (
    Any,
)
# Local libraries
from metaloaders.model import (
    Node,
    Type,
)
from metaloaders.cloudformation import (
    load,
)


def test_load_1() -> None:
    stream = dedent("""
        Resources:
            rTest:
                Type: 'AWS::RDS::OptionGroup'
                Properties:
                EngineName: mysql
                OptionGroupDescription: !Ref 'AWS::StackName'
                Tags:
                    -   Key: Name
                        Value: !Join ["", [!Ref 'AWS::StackName' , "-option-group"]]
                X: true
                Y: null
                # Z: !GetAtt logicalNameOfResource.attributeName
                # Fn::GetAtt: [ logicalNameOfResource, attributeName ]
    """)

    template = load(stream, 'yaml')

    assert template.inner['Resources'] == Node(
        data={
            Node(
                data='rTest',
                data_type=Type.STRING,
                end_column=9,
                end_line=3,
                start_column=4,
                start_line=3,
            ): Node(
                data={
                    Node(
                        data='Type',
                        data_type=Type.STRING,
                        end_column=12,
                        end_line=4,
                        start_column=8,
                        start_line=4,
                    ): Node(
                        data='AWS::RDS::OptionGroup',
                        data_type=Type.STRING,
                        end_column=37,
                        end_line=4,
                        start_column=14,
                        start_line=4,
                    ),
                    Node(
                        data='Properties',
                        data_type=Type.STRING,
                        end_column=18,
                        end_line=5,
                        start_column=8,
                        start_line=5,
                    ): Node(
                        data=None,
                        data_type=Type.NULL,
                        end_column=8,
                        end_line=6,
                        start_column=8,
                        start_line=6,
                    ),
                    Node(
                        data='EngineName',
                        data_type=Type.STRING,
                        end_column=18,
                        end_line=6,
                        start_column=8,
                        start_line=6,
                    ): Node(
                        data='mysql',
                        data_type=Type.STRING,
                        end_column=25,
                        end_line=6,
                        start_column=20,
                        start_line=6,
                    ),
                    Node(
                        data='OptionGroupDescription',
                        data_type=Type.STRING,
                        end_column=30,
                        end_line=7,
                        start_column=8,
                        start_line=7,
                    ): Node(
                        data={'Ref': 'AWS::StackName'},
                        data_type=Type.OBJECT,
                        end_column=53,
                        end_line=7,
                        start_column=32,
                        start_line=7,
                    ),
                    Node(
                        data='Tags',
                        data_type=Type.STRING,
                        end_column=12,
                        end_line=8,
                        start_column=8,
                        start_line=8,
                    ): Node(
                        data=[
                            Node(
                                data={
                                    Node(
                                        data='Key',
                                        data_type=Type.STRING,
                                        end_column=19,
                                        end_line=9,
                                        start_column=16,
                                        start_line=9,
                                    ): Node(
                                        data='Name',
                                        data_type=Type.STRING,
                                        end_column=25,
                                        end_line=9,
                                        start_column=21,
                                        start_line=9,
                                    ),
                                    Node(
                                        data='Value',
                                        data_type=Type.STRING,
                                        end_column=21,
                                        end_line=10,
                                        start_column=16,
                                        start_line=10,
                                    ): Node(
                                        data={
                                            'Fn::Join': [
                                                Node(
                                                    data='',
                                                    data_type=Type.STRING,
                                                    end_column=32,
                                                    end_line=10,
                                                    start_column=30,
                                                    start_line=10,
                                                ),
                                                Node(
                                                    data=[
                                                        Node(
                                                            data={'Ref': 'AWS::StackName'},
                                                            data_type=Type.OBJECT,
                                                            end_column=56,
                                                            end_line=10,
                                                            start_column=35,
                                                            start_line=10,
                                                        ),
                                                        Node(
                                                            data='-option-group',
                                                            data_type=Type.STRING,
                                                            end_column=74,
                                                            end_line=10,
                                                            start_column=59,
                                                            start_line=10,
                                                        ),
                                                    ],
                                                    data_type=Type.ARRAY,
                                                    end_column=75,
                                                    end_line=10,
                                                    start_column=34,
                                                    start_line=10,
                                                ),
                                            ],
                                        },
                                        data_type=Type.OBJECT,
                                        end_column=76,
                                        end_line=10,
                                        start_column=23,
                                        start_line=10,
                                    ),
                                },
                                data_type=Type.OBJECT,
                                end_column=8,
                                end_line=11,
                                start_column=16,
                                start_line=9,
                            ),
                        ],
                        data_type=Type.ARRAY,
                        end_column=8,
                        end_line=11,
                        start_column=12,
                        start_line=9,
                    ),
                    Node(
                        data='X',
                        data_type=Type.STRING,
                        end_column=9,
                        end_line=11,
                        start_column=8,
                        start_line=11,
                    ): Node(
                        data=True,
                        data_type=Type.BOOLEAN,
                        end_column=15,
                        end_line=11,
                        start_column=11,
                        start_line=11,
                    ),
                    Node(
                        data='Y',
                        data_type=Type.STRING,
                        end_column=9,
                        end_line=12,
                        start_column=8,
                        start_line=12,
                    ): Node(
                        data=None,
                        data_type=Type.NULL,
                        end_column=15,
                        end_line=12,
                        start_column=11,
                        start_line=12,
                    ),
                },
                data_type=Type.OBJECT,
                end_column=0,
                end_line=15,
                start_column=8,
                start_line=4,
            ),
        },
        data_type=Type.OBJECT,
        end_column=0,
        end_line=15,
        start_column=4,
        start_line=3,
    )
