def get_user_id_from_request(request) -> int:
    return request.query_params.get('user_id')