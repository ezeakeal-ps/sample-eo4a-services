"""Basic sentinelsat WPS implemenation."""
from pywps import EO4AProcess  # Import the EO4AProcess class
from pywps import ComplexInput, LiteralInput, LiteralOutput, BoundingBoxInput
from pywps.inout.literaltypes import AllowedValue
from pywps.validator.allowed_value import ALLOWEDVALUETYPE
from pywps.app.Common import Metadata
from pywps import UOM
import os

# WPS Format validation
from pywps import Format
from pywps.validator.mode import MODE

__author__ = 'dvagg'


class SentinelDownload(EO4AProcess):
    """Basic SentinelSat download WPS service.

    Parameters
    ----------
    search_polygon: GeoJson region
    cloud_percentage: Max percentage of cloud
    start_date: Start date YYYYMMDD
    end_date: End date YYYYMMDD

    Returns
    ----------
    output_dir: The path to the downloaded sentinel products
    """

    def __init__(self):
        """Sample."""
        inputs = [
            ComplexInput(
                'search_polygon', 'GeoJSON region',
                supported_formats=[Format('application/vnd.geo+json')],
                abstract="GeoJson of region to search",
                mode=MODE.SIMPLE, max_occurs=1
            ),
            # BoundingBoxInput(
                # 'search_box', 'Sample BBox input',
                # abstract="""
                # Sample usage of BoundingBox inputs for WPS
                # """,
                # crss=['EPSG:4326'],
                # dimensions=2
            # ),
            LiteralInput(
                'cloud_percentage', 'Max cloud Percentage',
                abstract="""
                Maximum cloud cover in percentage (e.g. 30)
                """,
                data_type='integer',
                allowed_values=AllowedValue(
                    allowed_type=ALLOWEDVALUETYPE.RANGE,
                    minval=0, maxval=100
                ),
                max_occurs=1
            ),
            LiteralInput(
                'start_date', 'Start date',
                abstract="""
                Datestamp in format YYYYMMDD
                """,
                data_type='integer',
                max_occurs=1
            ),
            LiteralInput(
                'end_date', 'End date',
                abstract="""
                Datestamp in format YYYYMMDD
                """,
                data_type='integer',
                max_occurs=1
            )
        ]
        outputs = [
            LiteralOutput(
                'output_dir',
                'Workflow data volume path',
                data_type='string',
                abstract="""
                Path to a directory within the Workflow Data volume.
                The service will store all outputs in this dir, then
                provide a reference to the directory which other services
                can use.
                """,
            )
        ]

        super(SentinelDownload, self).__init__(
            identifier='acquisition:sentinelsat',
            abstract="""
            Use sentinelsat python module to download sentinel data
            """,
            version='0.1',
            title="Sentinel 2 Data acquisition",
            metadata=[Metadata('Sample'), Metadata('Test')],
            profile='',
            inputs=inputs,
            outputs=outputs,
        )

    def get_command(self, request, response):
        """The service command. Do not do any processing here."""
        inputs = request.inputs
        self.sen2_dir = os.path.join(self.output_dir, "sen2")
        self.mkdir_p(self.sen2_dir)

        return "sentinel search --sentinel 2 -d --cloud %s -s %s -e %s -p %s ezeakeal Saqql890 %s" % (
                inputs['cloud_percentage'][0].source,
                inputs['start_date'][0].source,
                inputs['end_date'][0].source,
                self.sen2_dir,
                inputs['search_polygon'][0].file
        )

    def set_output(self, request, response):
        """Set the output from the WPS request."""
        # We use get_workflow_disk_path to get the path that other services
        # can read from. /data_service is local to each service, but a read-
        # only version exists in the workflow directory
        workflow_disk_result_path = self.get_workflow_disk_path(
            self.sen2_dir
        )
        response.outputs['output_dir'].data = workflow_disk_result_path
        response.outputs['output_dir'].uom = UOM('unity')
