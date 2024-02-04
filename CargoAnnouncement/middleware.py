from django.http import HttpResponseBadRequest

class BlockSpecialCharsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # چک کردن وجود کاراکترهای خاص در URL
        forbidden_chars = ['@', '%40']
        full_path = request.get_full_path()
        print(full_path)

        for char in forbidden_chars:
            if char in full_path:
                print(char)
                return HttpResponseBadRequest("Bad Request: Invalid character in URL")

        # ادامه به middleware یا ویو بعدی
        response = self.get_response(request)
        return response
