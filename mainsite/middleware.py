# middleware.py


import time
from django.utils.deprecation import MiddlewareMixin

class ResponseTimeMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response_times = []

    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        # Calculate response time
        if hasattr(request, 'start_time'):
            response_time = time.time() - request.start_time
            self.response_times.append(response_time)

            # Check if we have 10 response times
            if len(self.response_times) == 10:
                self.output_and_clear_response_times()

        return response

    def output_and_clear_response_times(self):
        # Output the 10 response times
        print("Response times:", self.response_times)
        # Clear the list
        self.response_times = []

    
# # middleware.py

# import time
# import logging

# logger = logging.getLogger(__name__)

# class ResponseTimeMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.log_format = "Response Time: %(response_time).2f seconds"

#     def __call__(self, request):
#         start_time = time.time()
#         response = self.get_response(request)
#         end_time = time.time()
#         duration = end_time - start_time
#         extra_data = {
#             'response_time': duration
#         }
#         logger.info(self.log_format, extra=extra_data)
#         return response