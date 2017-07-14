from pywps import EO4AProcess  # Import the EO4AProcess class
from pywps import LiteralInput, LiteralOutput  # Import supported WPS IO
from pywps import UOM
from pywps.app.Common import Metadata
import os

__author__ = 'dvagg'


class Sleep(EO4AProcess):
    
    def __init__(self):
        """Sample."""
        inputs = [
            LiteralInput(
                'sleep_sec',
                'Seconds to sleep for',
                data_type='integer',
                abstract="""
                Seconds to sleep for.
                """,
            ),
            LiteralInput(
                'chain_node',
                'Allow chaining.',
                data_type='string',
                abstract="""
                Allows chaining without an actual dependency.
                """,
                min_occurs=0
            )
        ]
        outputs = [
            LiteralOutput(
                'chain',
                'Nothing',
                data_type='string',
                abstract="""
                Empty ouput that can help chain processes.
                """,
            )
        ]

        super(Sleep, self).__init__(
            identifier='sleep',
            abstract="""
            Sleeps for a few seconds
            """,
            version='0.1',
            title="Sleeper",
            profile='',
            metadata=[Metadata('Sample'), Metadata('Test')],
            inputs=inputs,
            outputs=outputs,
        )

    def get_command(self, request, response):
        """The service command. Do not do any processing here."""
        inputs = request.inputs
        return [
            "bash", "sleep_script.sh",
            str(inputs['sleep_sec'][0].source)
        ]

    def set_output(self, request, response):
        """Set the output from the WPS request."""
        response.outputs['chain'].data = "okay"
