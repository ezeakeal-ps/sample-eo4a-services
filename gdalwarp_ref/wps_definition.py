"""Sample WPS process using Workflow data volume references.

The Workflow data volume is a volume shared between all services
in a workflow. This helps for sharing directories of data, or for
preventing unnecessary encoding/copying of large data products.

This example service can be useful for the following common scenario:
---------
Service A (Sentinel data acquisition):
    Acquires sentinel data given a bounding box and some other attributes.

    Given a region and other query parameters, will download all sentinel data
    matching the query to a location on disk.

    It outputs the path to disk, rather than ComplexOutputs (as WPS expecteds)

Service B (Atmospheric correction):
    Performs some correction of all sentinel products in a directory

    Given correction parameters, and a location on disk (shared between all
    services in a workflow), will iterate over all data-products,
    and perform atmospheric correction.

    Will output a path to disk containing the corrected data

Service C (Transfer data):
    Transfers data products from the execution environment to another location

    Given a location on disk, destination identifier, and perhaps a pattern,
    will locate data matching the given pattern and transfer it to another
    data-centre.
    For example:
        1) data could be transferred to S3 given a users credentials
        2) data could be transferred to the EO4A platform in AWS for storage
            This data can then be used for mapping, or sharing in the platform
"""
from pywps import EO4AProcess  # Import the EO4AProcess class
from pywps import LiteralInput, LiteralOutput  # Import supported WPS IO
from pywps import UOM
from pywps.app.Common import Metadata
import os

__author__ = 'dvagg'


class GdalWarpRef(EO4AProcess):
    """Sample."""

    def __init__(self):
        """Sample."""
        inputs = [
            LiteralInput(
                'input_dir',
                'Workflow data volume path',
                data_type='string',
                abstract="""
                Path to a directory within the Workflow Data volume.
                The service will locate all files within this directory
                and warp them.
                """,
                min_occurs=1,
                max_occurs=2
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

        super(GdalWarpRef, self).__init__(
            identifier='gdalwarp_ref',
            abstract="""
            The process warps an input raster.
            Locates all tiff files within the input_dir and creates a warped
            version in the output_dir location.
            <a href="http://gdal.org/gdalwarp.html">man page</a>
            """,
            version='0.1',
            metadata=[Metadata('Sample'), Metadata('Test')],
            title="GDAL Sample Process",
            profile='',
            inputs=inputs,
            outputs=outputs,
        )

    def get_command(self, request, response):
        """The service command. Do not do any processing here."""
        inputs = request.inputs
        self.output_resized_dir = os.path.join(self.output_dir, "resized")
        return [
            "bash", "gdalwarp_script.sh",
            inputs['input_dir'][0].source,
            self.output_resized_dir
        ]

    def set_output(self, request, response):
        """Set the output from the WPS request."""
        # We use get_workflow_disk_path to get the path that other services
        # can read from. /data_service is local to each service, but a read-
        # only version exists in the workflow directory
        workflow_disk_result_path = self.get_workflow_disk_path(
            self.output_resized_dir
        )
        response.outputs['output_dir'].data = workflow_disk_result_path
        response.outputs['output_dir'].uom = UOM('unity')
