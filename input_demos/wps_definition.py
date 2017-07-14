from pywps import Format
from pywps import EO4AProcess
from pywps import LiteralInput, LiteralOutput, ComplexInput
from pywps.app.Common import Metadata
from pywps.validator.mode import MODE
from pywps.inout.literaltypes import AllowedValue
from pywps.validator.allowed_value import ALLOWEDVALUETYPE

__author__ = 'dvagg'


class InputDemos(EO4AProcess):
    
    def __init__(self):
        """Sample."""
        inputs = [
            LiteralInput(
                'sentinel_products',
                'Sentine Product IDs',
                data_type='string',
                abstract="""
                helper:sentinel_product_select
                """,
            ),
            ComplexInput(
                'geojson', 'GeoJSON region',
                supported_formats=[Format('application/vnd.geo+json')],
                abstract="GeoJson",
                mode=MODE.SIMPLE, max_occurs=1
            ),
            LiteralInput(
                'ranged', 'Ranged Value',
                abstract="""
                Sample of allowed_value usage
                """,
                data_type='integer',
                allowed_values=AllowedValue(
                    allowed_type=ALLOWEDVALUETYPE.RANGE,
                    minval=0, maxval=100
                ),
                max_occurs=1
            )
        ]
        outputs = [
            LiteralOutput(
                'none',
                'Nothing',
                data_type='string',
                abstract="""
                Empty ouput.
                """,
            )
        ]

        super(InputDemos, self).__init__(
            identifier='input_demos',
            abstract="""
            Input demonstrators.
            """,
            version='0.1',
            title="Input Demos",
            profile='',
            metadata=[Metadata('Sample'), Metadata('Input')],
            inputs=inputs,
            outputs=outputs,
        )

    def get_command(self, request, response):
        return [
            "echo", "sample"
        ]

    def set_output(self, request, response):
        """Set the output from the WPS request."""
        response.outputs['chain'].data = "done"
