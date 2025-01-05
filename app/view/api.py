"""Sel value API"""

from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config

from pyramid_app_caseinterview.models.depthseries import Depthseries
from pyramid_app_caseinterview.models.timeseries import Timeseries

from pyramid.httpexceptions import HTTPBadRequest
from pyramid_app_caseinterview.utils.request_validator import RequestValidator

from . import View


class API(View):
    """API endpoints"""

    @view_config(
        route_name="timeseries",
        permission=NO_PERMISSION_REQUIRED,
        renderer="json",
        request_method="GET",
    )
    def timeseries_api(self):

        params = RequestValidator(
            self.request, start_date="date", end_date="date"
        ).validate()

        if (
            params["start_date"]
            and params["end_date"]
            and params["start_date"] > params["end_date"]
        ):
            raise HTTPBadRequest("start_date cannot be later than end_date")

        query = self.session.query(Timeseries)

        if params["start_date"]:
            query = query.filter(Timeseries.datetime >= params["start_date"])

        if params["end_date"]:
            query = query.filter(Timeseries.datetime <= params["end_date"])

        query = self.session.query(Timeseries)
        return [
            {
                "id": str(q.id),
                "datetime": q.datetime,
                "value": q.value,
            }
            for q in query.all()
        ]

    @view_config(
        route_name="depthseries",
        permission=NO_PERMISSION_REQUIRED,
        renderer="json",
        request_method="GET",
    )
    def depthseries_api(self):

        query = self.session.query(Depthseries).distinct(Depthseries.depth).filter(Depthseries.value.isnot(None))

        return [
            {
                "id": str(q.id),
                "depth": q.depth,
                "value": q.value,
            }
            for q in query.all()
        ]
