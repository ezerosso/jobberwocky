from flask import Blueprint
from app.common.dtos.job_dto import CreateJobDTO, JobSearchDTO, SubscriberDTO
from app.common.response.api_response import ApiResponse
from app.common.decorators.validations import validate_request
from app.services.job_service import JobService
from app.services.subscriber_service import SubscriberService

class JobRoutes:
    def __init__(self, job_service: JobService, subscriber_service: SubscriberService):
        self.job_service = job_service
        self.job_routes = Blueprint("job_routes", __name__)
        self.subscriber_service = subscriber_service
        self._register_routes()

    def _register_routes(self):
        self.job_routes.add_url_rule("/jobs/create", view_func=self.create_job, methods=["POST"])
        self.job_routes.add_url_rule("/jobs/search", view_func=self.search_jobs, methods=["POST"])
        self.job_routes.add_url_rule("/jobs/subscriber", view_func=self.subscriber_jobs, methods=["POST"])

    @validate_request(CreateJobDTO)
    def create_job(self, validated_data):
        jobId = self.job_service.create_internal_jobs(validated_data)
        return ApiResponse.success({"id": jobId}, 201)
    
    @validate_request(JobSearchDTO)
    def search_jobs(self, validated_data):
        jobs = self.job_service.search_jobs(validated_data)
        return ApiResponse.success([job.__dict__ for job in jobs], 200)
    
    @validate_request(SubscriberDTO)
    def subscriber_jobs(self, validated_data):
        self.subscriber_service.subscribe(validated_data)
        return ApiResponse.success(None, 200)
