from conftest import db_query, get_response


def test_get_request(check_the_first_stable_user, get_response, db_query):
    get_response.get_query()
    get_response.check_response(check_the_first_stable_user)
    get_response.check_one_user_with_db_and_query(check_the_first_stable_user)

def test_post_request(get_new_user, db_query, get_response):
    get_new_user.create_new_user()
    get_new_user.check_response_status()
    get_new_user.check_created_user()
    get_response.get_query()
    get_response.check_one_user_with_db_and_query(get_new_user.created_user)

def test_put_request(get_random_user, db_query, change_user, get_response):
    get_response.get_query()
    get_response.check_response(get_random_user)
    get_response.check_one_user_with_db_and_query(get_random_user)
    change_user.change_the_user_params(get_random_user)
    change_user.check_response_status()
    change_user.check_changed_user()
    get_response.get_query()
    get_response.check_one_user_with_db_and_query(change_user.changed_user)


def test_delete_request(get_random_user, delete_user, db_query, get_response):
    get_response.get_query()
    get_response.check_response(get_random_user)
    get_response.check_one_user_with_db_and_query(get_random_user)
    delete_user.delete_user(get_random_user)
    delete_user.check_response_status()
    delete_user.check_deleted_user_message()
    get_response.get_query()
    get_response.check_response_with_deleted_user(delete_user.user_dict)
    get_response.check_one_user_with_db_and_query(delete_user.user_dict)